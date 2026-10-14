from datetime import datetime
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User, AuthSession


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def by_email(self, email: str) -> User | None:
        return await self.session.scalar(select(User).where(User.email == email))

    async def get(self, user_id: int) -> User | None:
        return await self.session.get(User, user_id)

    async def add(self, email: str, name: str, password_hash: str) -> User:
        user = User(email=email, name=name, password_hash=password_hash)
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user

    async def add_session(self, user_id: int, session_id: str, expires_at: datetime) -> None:
        self.session.add(AuthSession(id=session_id, user_id=user_id, expires_at=expires_at))

    async def get_session(self, session_id: str) -> AuthSession | None:
        return await self.session.get(AuthSession, session_id)

    async def revoke(self, session_id: str) -> None:
        await self.session.execute(delete(AuthSession).where(AuthSession.id == session_id))

    async def remove_expired(self, now: datetime) -> None:
        await self.session.execute(delete(AuthSession).where(AuthSession.expires_at <= now))
