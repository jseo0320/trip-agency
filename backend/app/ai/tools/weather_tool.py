from sqlalchemy.ext.asyncio import AsyncSession
from app.services.weather_service import WeatherService
from app.schemas.weather import WeatherResponse

async def weather_tool(session: AsyncSession, city: str) -> WeatherResponse:
    """관광 도메인 서비스에 접근하는 agent용 어댑터."""
    return await WeatherService(session).current(city)
