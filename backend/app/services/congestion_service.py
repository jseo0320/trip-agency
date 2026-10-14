from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import get_settings
from app.core.exceptions import AppError
from app.repositories.congestion_repository import CongestionRepository
from app.schemas.congestion import CongestionResponse, CongestionValue, Forecast
from app.services.tourism_service import TourismService
from app.services.traffic_service import TrafficService
from app.services.weather_service import WeatherService
from app.optimizer.score import congestion_score, congestion_level

class CongestionService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, place_id: int) -> CongestionResponse:
        place = await TourismService(self.session).get(place_id)
        if not get_settings().use_mock_data:
            row = await CongestionRepository(self.session).latest(place_id)
            if row is None:
                raise AppError("DATA_NOT_FOUND", "해당 관광지의 혼잡도 데이터가 없습니다.", 404)
            return CongestionResponse(place_id=place.id, place_name=place.name,
                current=CongestionValue(score=row.congestion_score, level=row.congestion_level),
                forecast=[Forecast(hour=h, score=s) for h,s in enumerate([row.predicted_1h,row.predicted_2h,row.predicted_3h],1) if s is not None], source="database")
        traffic = await TrafficService(self.session).current(place.city)
        weather = await WeatherService(self.session).current(place.city)
        score = congestion_score(max(0,100-traffic.avg_speed*2), min(100,traffic.pedestrian_count/5), 35, min(100,weather.rainfall*10))
        return CongestionResponse(place_id=place.id, place_name=place.name,
            current=CongestionValue(score=score,level=congestion_level(score)), forecast=[], source="mock_rule_based_no_forecast")
