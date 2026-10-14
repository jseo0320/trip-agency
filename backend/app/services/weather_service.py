from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import get_settings
from app.core.exceptions import AppError
from app.repositories.weather_repository import WeatherRepository
from app.repositories.mock_data import CITY_ALIASES
from app.schemas.weather import WeatherResponse

class WeatherService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = WeatherRepository(session)

    async def current(self, city: str) -> WeatherResponse:
        city = CITY_ALIASES.get(city, city)
        if get_settings().use_mock_data:
            return WeatherResponse(city=city, timestamp=datetime.now(timezone.utc), temperature=22, rainfall=0, humidity=60, wind_speed=2.3, sky_condition="맑음", source="mock")
        record = await self.repository.latest(city)
        if record is None:
            raise AppError("DATA_NOT_FOUND", "수집된 weather 데이터가 없습니다.", 404)
        return WeatherResponse.model_validate(record)
