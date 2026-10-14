from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.schemas.tourism import TouristPlaceResponse
from app.services.tourism_service import TourismService
router = APIRouter(prefix="/tourism", tags=["tourism"])

@router.get("/places", response_model=list[TouristPlaceResponse])
async def list_places(city: str | None = None, category: str | None = None, session: AsyncSession = Depends(get_session)) -> list[TouristPlaceResponse]:
    return await TourismService(session).list_places(city,category)

@router.get("/places/{place_id}", response_model=TouristPlaceResponse)
async def get_place(place_id: int, session: AsyncSession = Depends(get_session)) -> TouristPlaceResponse:
    return await TourismService(session).get(place_id)
