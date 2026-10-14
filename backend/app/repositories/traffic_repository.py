from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.traffic import TrafficRecord

class TrafficRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def latest(self, value: str) -> TrafficRecord | None:
        statement = select(TrafficRecord).where(TrafficRecord.city == value).order_by(TrafficRecord.timestamp.desc()).limit(1)
        return await self.session.scalar(statement)
