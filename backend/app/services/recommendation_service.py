import logging
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import get_settings
from app.core.exceptions import AppError
from app.repositories.mock_data import CITY_ALIASES
from app.schemas.recommendation import TravelRequest, RecommendationResponse
from app.services.tourism_service import TourismService
from app.services.congestion_service import CongestionService
from app.optimizer.route_optimizer import optimize_route

logger = logging.getLogger(__name__)
STARTS = {"부산역": (35.1151,129.0414), "울산역": (35.5514,129.1386), "경주역": (35.7982,129.1388)}

class RecommendationService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def recommend(self, request: TravelRequest) -> RecommendationResponse:
        cities = {CITY_ALIASES.get(c,c) for c in request.cities}
        places = [p for p in await TourismService(self.session).list_places() if p.city in cities]
        if not places:
            raise AppError("DATA_NOT_FOUND", "선택한 지역의 관광지가 없습니다.", 404)
        warnings = ["이동시간은 직선거리 기반 추정치이며 실제 대중교통 노선을 반영하지 않습니다.", "미래 혼잡도 모델은 학습 데이터 확보 후 연결합니다."]
        warnings.append("선택한 날짜의 날씨·혼잡도·휴무일 정보는 아직 연동되지 않았습니다. 현재 저장 정보로 일정을 구성합니다.")
        if request.start_latitude is not None and request.start_longitude is not None:
            start = (request.start_latitude,request.start_longitude)
        elif request.start_location in STARTS:
            start = STARTS[request.start_location]
        else:
            raise AppError("UNKNOWN_START_LOCATION", "부산역·울산역·경주역을 입력하거나 출발 좌표를 지정하세요.")
        scores = {p.id: (await CongestionService(self.session).get(p.id)).current.score for p in places}
        route = optimize_route(places,request,scores,start)
        missing = set(request.must_visit) - {s.place for s in route}
        if missing:
            warnings.append("일정에 포함하지 못한 필수 관광지: " + ", ".join(sorted(missing)))
        if not route:
            warnings.append("주어진 시간에 방문 가능한 관광지가 없습니다.")
        summary = "운영시간과 이동시간, 취향을 고려한 Trip Agency 추천 일정입니다."
        if get_settings().use_mock_data:
            warnings.append("현재 관광지 운영시간·교통·날씨·혼잡도는 시연용 샘플입니다.")
        if get_settings().enable_llm and route:
            try:
                from app.ai.agents.trip_agency_agent import explain_route
                summary = await explain_route(route)
            except Exception:
                logger.warning("Ollama unavailable; returning optimized route", exc_info=True)
                warnings.append("AI 설명을 가져오지 못해 기본 설명을 표시합니다.")
        return RecommendationResponse(travel_date=request.travel_date, summary=summary, route=route, warnings=warnings,source="mock" if get_settings().use_mock_data else "database")
