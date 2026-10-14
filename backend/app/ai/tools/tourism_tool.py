from sqlalchemy.ext.asyncio import AsyncSession
from app.services.tourism_service import TourismService
from app.schemas.tourism import TouristPlaceResponse

async def tourism_tool(session: AsyncSession, city: str) -> list[TouristPlaceResponse]:
    """관광 도메인 서비스에 접근하는 agent용 어댑터."""
    return await TourismService(session).list_places(city)
