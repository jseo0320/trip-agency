from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import get_settings
from app.models.tourist_place import TouristPlace
from app.repositories.mock_data import PLACES, CITY_ALIASES, PREFERENCE_ALIASES
from app.schemas.tourism import TouristPlaceResponse

class TourismRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_places(self, city: str | None = None, category: str | None = None) -> list[TouristPlaceResponse]:
        city = CITY_ALIASES.get(city, city)
        category = PREFERENCE_ALIASES.get(category, category)
        if get_settings().use_mock_data:
            return [p for p in PLACES if (not city or p.city == city) and (not category or p.category == category)]
        statement = select(TouristPlace)
        if city:
            statement = statement.where(TouristPlace.city == city)
        if category:
            statement = statement.where(TouristPlace.category == category)
        result = await self.session.scalars(statement.order_by(TouristPlace.id))
        return [TouristPlaceResponse.model_validate(p) for p in result.all()]

    async def get(self, place_id: int) -> TouristPlaceResponse | None:
        if get_settings().use_mock_data:
            return next((p for p in PLACES if p.id == place_id), None)
        place = await self.session.get(TouristPlace, place_id)
        return TouristPlaceResponse.model_validate(place) if place else None
