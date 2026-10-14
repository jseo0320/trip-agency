from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import AppError
from app.repositories.tourism_repository import TourismRepository
from app.schemas.tourism import TouristPlaceResponse

class TourismService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = TourismRepository(session)

    async def list_places(self, city: str | None = None, category: str | None = None) -> list[TouristPlaceResponse]:
        return await self.repository.list_places(city, category)

    async def get(self, place_id: int) -> TouristPlaceResponse:
        place = await self.repository.get(place_id)
        if place is None:
            raise AppError("DATA_NOT_FOUND", "관광지를 찾을 수 없습니다.", 404)
        return place
