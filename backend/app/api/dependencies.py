from dataclasses import dataclass
from datetime import datetime, timezone
from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import get_settings
from app.core.database import get_session
from app.core.exceptions import AppError
from app.core.security import COOKIE_NAME, decode_token
from app.models.user import User
from app.repositories.user_repository import UserRepository

bearer = HTTPBearer(auto_error=False)


def check_origin(request: Request) -> None:
    origin = request.headers.get("origin")
    if origin and origin not in get_settings().cors_origins:
        raise AppError("INVALID_ORIGIN", "허용되지 않은 요청 출처입니다.", 403)


@dataclass
class AuthenticatedUser:
    user: User
    session_id: str


async def current_user(request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
    session: AsyncSession = Depends(get_session)) -> AuthenticatedUser:
    token = credentials.credentials if credentials else request.cookies.get(COOKIE_NAME)
    if not token:
        raise AppError("UNAUTHORIZED", "로그인이 필요합니다.", 401)
    if not credentials and request.method not in ("GET", "HEAD", "OPTIONS"):
        check_origin(request)
        if not request.headers.get("origin"):
            raise AppError("INVALID_ORIGIN", "쿠키 인증 요청에는 Origin이 필요합니다.", 403)
    claims = decode_token(token)
    repository = UserRepository(session)
    active = await repository.get_session(claims["jti"])
    if not active or active.user_id != int(claims["sub"]) or active.expires_at <= datetime.now(timezone.utc):
        raise AppError("UNAUTHORIZED", "로그인이 만료되었습니다. 다시 로그인하세요.", 401)
    user = await repository.get(active.user_id)
    if not user:
        raise AppError("UNAUTHORIZED", "사용자를 찾을 수 없습니다.", 401)
    return AuthenticatedUser(user=user, session_id=active.id)
