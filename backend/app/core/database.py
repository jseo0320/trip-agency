from collections.abc import AsyncIterator
from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from app.core.config import get_settings

class Base(DeclarativeBase):
    pass

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

engine = create_async_engine(get_settings().database_url, pool_pre_ping=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_session() -> AsyncIterator[AsyncSession]:
    async with SessionLocal() as session:
        yield session

async def create_tables() -> None:
    from app.models import tourist_place, traffic, weather, congestion, recommendation, user
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

async def create_auth_tables() -> None:
    from app.models.user import User, AuthSession
    from app.models.travel_plan import TravelPlan
    from app.models.profile import UserPreferences, FavoritePlace
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all, tables=[User.__table__, AuthSession.__table__, TravelPlan.__table__, UserPreferences.__table__, FavoritePlace.__table__])
