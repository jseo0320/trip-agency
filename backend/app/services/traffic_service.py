from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import get_settings
from app.core.exceptions import AppError
from app.repositories.traffic_repository import TrafficRepository
from app.repositories.mock_data import CITY_ALIASES
from app.schemas.traffic import TrafficResponse

class TrafficService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = TrafficRepository(session)

    async def current(self, city: str) -> TrafficResponse:
        city = CITY_ALIASES.get(city, city)
        if get_settings().use_mock_data:
            return TrafficResponse(city=city, timestamp=datetime.now(timezone.utc), avg_speed=28, traffic_volume=650, pedestrian_count=120, queue_length=8, source="mock")
        record = await self.repository.latest(city)
        if record is None:
            raise AppError("DATA_NOT_FOUND", "수집된 traffic 데이터가 없습니다.", 404)
        return TrafficResponse.model_validate(record)
