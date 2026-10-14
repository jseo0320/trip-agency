from sqlalchemy.ext.asyncio import AsyncSession
from app.services.congestion_service import CongestionService
from app.schemas.congestion import CongestionResponse

async def congestion_tool(session: AsyncSession, place_id: int) -> CongestionResponse:
    """관광 도메인 서비스에 접근하는 agent용 어댑터."""
    return await CongestionService(session).get(place_id)
