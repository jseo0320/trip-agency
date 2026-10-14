from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.weather import WeatherRecord

class WeatherRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def latest(self, value: str) -> WeatherRecord | None:
        statement = select(WeatherRecord).where(WeatherRecord.city == value).order_by(WeatherRecord.timestamp.desc()).limit(1)
        return await self.session.scalar(statement)
