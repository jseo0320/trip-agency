from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.schemas.weather import WeatherResponse
from app.services.weather_service import WeatherService
from app.services.tourism_service import TourismService
router = APIRouter(prefix="/weather",tags=["weather"])

@router.get("/current",response_model=WeatherResponse)
async def current(city: str = "busan", place_id: int | None = None, session: AsyncSession = Depends(get_session)) -> WeatherResponse:
    if place_id is not None:
        city = (await TourismService(session).get(place_id)).city
    return await WeatherService(session).current(city)
