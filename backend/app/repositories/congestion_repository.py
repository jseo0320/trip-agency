from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.congestion import CongestionRecord

class CongestionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def latest(self, value: int) -> CongestionRecord | None:
        statement = select(CongestionRecord).where(CongestionRecord.place_id == value).order_by(CongestionRecord.timestamp.desc()).limit(1)
        return await self.session.scalar(statement)
