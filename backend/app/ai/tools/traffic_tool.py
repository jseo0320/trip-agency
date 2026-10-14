from sqlalchemy.ext.asyncio import AsyncSession
from app.services.traffic_service import TrafficService
from app.schemas.traffic import TrafficResponse

async def traffic_tool(session: AsyncSession, city: str) -> TrafficResponse:
    """관광 도메인 서비스에 접근하는 agent용 어댑터."""
    return await TrafficService(session).current(city)
