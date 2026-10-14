from datetime import time
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import AppError
from app.models.travel_plan import TravelPlan
from app.optimizer.route_optimizer import optimize_route, minutes
from app.repositories.mock_data import CITY_ALIASES
from app.schemas.chat import RevisionIntent
from app.schemas.recommendation import TravelRequest, RecommendationResponse
from app.services.congestion_service import CongestionService
from app.services.plan_service import PlanService
from app.services.recommendation_service import STARTS
from app.services.tourism_service import TourismService
from app.utils.datetime import now_korea

# Only explicit indoor categories qualify; a cafe street is not an indoor venue.
INDOOR_CATEGORIES = {"museum", "aquarium", "gallery", "indoor"}


async def revise_plan(session: AsyncSession, user_id: int, plan: TravelPlan,
    intent: RevisionIntent) -> RecommendationResponse:
    if plan.result["travel_date"] < now_korea().date().isoformat():
        raise AppError("PAST_TRAVEL", "지난 여행은 조회할 수 있지만 날짜를 지난 상태로 다시 계산할 수 없습니다. 새 여행 날짜로 코스를 만들어 주세요.", 409)
    request = TravelRequest.model_validate(plan.request)
    original = RecommendationResponse.model_validate(plan.result)
    boundary = time.fromisoformat(intent.change_from) if intent.change_from else request.start_time
    boundary_minutes = minutes(boundary)
    if boundary >= request.end_time:
        raise AppError("INVALID_CHANGE_TIME", "변경 시작 시각이 여행 종료시간 이후입니다.")
    excluded = set(request.excluded_places) | set(intent.excluded_places)
    # Keep only visits fully finished before the change boundary. Crossing visits are replanned.
    prefix = [stop for stop in original.route if minutes(time.fromisoformat(stop.departure_time)) <= boundary_minutes]
    if any(stop.place in excluded for stop in prefix):
        raise AppError("CHANGE_CONFLICT", "제외하려는 장소가 유지 구간에 있습니다. 변경 시작 시각을 더 이르게 지정하세요.")
    if prefix:
        start = (prefix[-1].latitude, prefix[-1].longitude)
        start_time = time.fromisoformat(prefix[-1].departure_time)
    else:
        start = (request.start_latitude,request.start_longitude) if request.start_latitude is not None else STARTS.get(request.start_location)
        start_time = request.start_time
    if start is None:
        raise AppError("UNKNOWN_START_LOCATION", "출발 위치를 확인하세요.")
    start_time = max(start_time, boundary)
    cities = {CITY_ALIASES.get(city, city) for city in request.cities}
    visited = {stop.place_id for stop in prefix}
    places = [place for place in await TourismService(session).list_places()
        if place.city in cities and place.id not in visited and place.name not in excluded
        and (not intent.indoor_only or place.category in INDOOR_CATEGORIES)]
    if not places:
        raise AppError("NO_ALTERNATIVE", "조건에 맞는 대체 관광지가 없습니다. 변경 시간을 앞당기거나 다른 지역·조건을 알려주세요.", 409)
    must_visit = list(dict.fromkeys(request.must_visit + intent.must_visit))
    tail_request = request.model_copy(update={"start_time":start_time,
        "excluded_places":sorted(excluded), "must_visit":[name for name in must_visit if name not in {stop.place for stop in prefix}]})
    indoor_from = request.indoor_from
    if intent.indoor_only:
        indoor_from = min(indoor_from, boundary) if indoor_from else boundary
    tail_request = tail_request.model_copy(update={"indoor_from":indoor_from})
    scores = {place.id:(await CongestionService(session).get(place.id)).current.score for place in places}
    tail = optimize_route(places, tail_request, scores, start)
    if not tail:
        raise AppError("NO_ALTERNATIVE", "남은 시간과 운영시간에 맞는 대체 코스가 없습니다. 변경 시간을 앞당겨 주세요.", 409)
    route = prefix + [stop.model_copy(update={"order":len(prefix)+index,
        "reason":"요청한 변경 조건과 운영시간·이동시간을 고려한 대체 장소입니다."}) for index,stop in enumerate(tail,1)]
    warnings = ["이동시간은 직선거리 기반 추정치입니다.", "날씨 조건은 사용자가 알려준 내용을 반영했으며 실제 예보를 조회하지 않았습니다."]
    if original.source == "mock":
        warnings.append("관광지 운영시간·혼잡도는 시연용 샘플입니다. 방문 전 실제 정보를 확인하세요.")
    missing = set(must_visit)-{stop.place for stop in route}
    if missing:
        warnings.append("포함하지 못한 필수 관광지: "+", ".join(sorted(missing)))
    if route == original.route:
        raise AppError("NO_CHANGE", "현재 일정이 이미 요청 조건에 맞습니다.", 409)
    updated_request = request.model_copy(update={"excluded_places":sorted(excluded), "must_visit":must_visit,"indoor_from":indoor_from})
    result = RecommendationResponse(travel_date=request.travel_date, route=route,source=original.source,
        summary=f"{intent.change_from or request.start_time.strftime('%H:%M')} 이후 일정을 요청에 맞춰 다시 구성했습니다. 앞선 일정은 유지합니다.", warnings=warnings)
    return await PlanService(session,user_id).save(updated_request,result,parent_id=plan.id)
