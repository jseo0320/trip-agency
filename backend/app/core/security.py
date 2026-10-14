from datetime import datetime, timedelta, timezone
from secrets import token_urlsafe
from typing import Any
import jwt
from pwdlib import PasswordHash
from app.core.config import get_settings
from app.core.exceptions import AppError

password_hasher = PasswordHash.recommended()
COOKIE_NAME = "trip_agency_access"


def require_jwt_secret() -> str:
    secret = get_settings().jwt_secret_key
    if len(secret.encode("utf-8")) < 32:
        raise RuntimeError("JWT_SECRET_KEY must contain at least 32 bytes. Set it in backend/.env.")
    return secret


def issue_token(user_id: int) -> tuple[str, str, datetime]:
    settings = get_settings()
    now = datetime.now(timezone.utc)
    expires = now + timedelta(minutes=settings.jwt_expire_minutes)
    session_id = token_urlsafe(32)
    token = jwt.encode({"sub": str(user_id), "jti": session_id, "iat": now,
        "exp": expires, "iss": settings.jwt_issuer, "aud": settings.jwt_audience,
        "type": "access"}, require_jwt_secret(), algorithm="HS256")
    return token, session_id, expires


def decode_token(token: str) -> dict[str, Any]:
    settings = get_settings()
    try:
        claims = jwt.decode(token, require_jwt_secret(), algorithms=["HS256"],
            issuer=settings.jwt_issuer, audience=settings.jwt_audience,
            options={"require": ["sub", "jti", "iat", "exp", "iss", "aud", "type"]})
        if claims["type"] != "access" or not isinstance(claims["jti"], str):
            raise ValueError("Invalid token type")
        int(claims["sub"])
        return claims
    except (jwt.InvalidTokenError, ValueError, TypeError) as exc:
        raise AppError("UNAUTHORIZED", "로그인이 만료되었거나 인증 정보가 올바르지 않습니다.", 401) from exc
