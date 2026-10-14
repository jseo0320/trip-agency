from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.concurrency import run_in_threadpool
from app.core.config import get_settings
from app.core.exceptions import AppError
from app.core.security import issue_token, password_hasher
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, UserResponse

# Unknown-email login attempts still run Argon2 verification.
DUMMY_HASH = password_hasher.hash("not-a-real-user-password")


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repository = UserRepository(session)

    async def register(self, body: RegisterRequest) -> TokenResponse:
        if await self.repository.by_email(str(body.email)):
            raise AppError("EMAIL_ALREADY_EXISTS", "이미 사용 중인 이메일입니다.", 409)
        hashed = await run_in_threadpool(password_hasher.hash, body.password)
        try:
            user = await self.repository.add(str(body.email), body.name, hashed)
            return await self.start_session(user)
        except IntegrityError as exc:
            await self.session.rollback()
            raise AppError("EMAIL_ALREADY_EXISTS", "이미 사용 중인 이메일입니다.", 409) from exc

    async def login(self, body: LoginRequest) -> TokenResponse:
        user = await self.repository.by_email(str(body.email))
        valid = await run_in_threadpool(password_hasher.verify, body.password, user.password_hash if user else DUMMY_HASH)
        if not user or not valid:
            raise AppError("INVALID_CREDENTIALS", "이메일 또는 비밀번호가 올바르지 않습니다.", 401)
        return await self.start_session(user)

    async def start_session(self, user: User) -> TokenResponse:
        token, session_id, expires_at = issue_token(user.id)
        await self.repository.remove_expired(datetime.now(timezone.utc))
        await self.repository.add_session(user.id, session_id, expires_at)
        await self.session.commit()
        return TokenResponse(access_token=token, expires_in=get_settings().jwt_expire_minutes * 60,
            user=UserResponse.model_validate(user))
