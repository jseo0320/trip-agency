from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.schemas.traffic import TrafficResponse
from app.services.traffic_service import TrafficService
from app.services.tourism_service import TourismService
router = APIRouter(prefix="/traffic",tags=["traffic"])

@router.get("/current",response_model=TrafficResponse)
async def current(city: str = "busan", place_id: int | None = None, session: AsyncSession = Depends(get_session)) -> TrafficResponse:
    if place_id is not None:
        city = (await TourismService(session).get(place_id)).city
    return await TrafficService(session).current(city)
