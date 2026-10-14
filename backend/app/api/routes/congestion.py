from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.schemas.congestion import CongestionResponse
from app.services.congestion_service import CongestionService
router = APIRouter(prefix="/congestion",tags=["congestion"])

@router.get("/{place_id}",response_model=CongestionResponse)
async def get_congestion(place_id: int, session: AsyncSession = Depends(get_session)) -> CongestionResponse:
    return await CongestionService(session).get(place_id)
