from datetime import time
from app.schemas.recommendation import TravelRequest, RouteStop
from app.schemas.tourism import TouristPlaceResponse
from app.repositories.mock_data import PREFERENCE_ALIASES
from app.optimizer.distance import estimate_travel_minutes, haversine
from app.optimizer.score import route_cost

def minutes(value: time) -> int:
    return value.hour * 60 + value.minute

def clock(value: int) -> str:
    return f"{value // 60:02d}:{value % 60:02d}"

def optimize_route(places: list[TouristPlaceResponse], request: TravelRequest, scores: dict[int, float], start: tuple[float,float]) -> list[RouteStop]:
    remaining = [p for p in places if p.name not in request.excluded_places]
    preferences = {PREFERENCE_ALIASES.get(p,p) for p in request.preferences}
    current, end = minutes(request.start_time), minutes(request.end_time)
    position = start
    route: list[RouteStop] = []
    while remaining:
        feasible = []
        for place in remaining:
            travel = estimate_travel_minutes(position,(place.latitude,place.longitude),request.transportation)
            arrival = max(current+travel,minutes(place.opening_time))
            departure = arrival + place.average_stay_minutes
            if request.indoor_from is not None and departure > minutes(request.indoor_from) and place.category not in {"museum", "aquarium", "gallery", "indoor"}:
                continue
            if departure > min(end,minutes(place.closing_time)):
                continue
            cost = route_cost(travel, scores[place.id] if request.avoid_congestion else 0,
                0 if not preferences or place.category in preferences else 100, arrival-current-travel)
            cost += haversine(position,(place.latitude,place.longitude))*{"low":2,"normal":1,"high":.5}[request.walking_preference]
            feasible.append((0 if place.name in request.must_visit else 1,cost,place.id,place,travel,arrival,departure))
        if not feasible:
            break
        _,_,_,place,travel,arrival,departure = min(feasible,key=lambda x:x[:3])
        route.append(RouteStop(order=len(route)+1,place_id=place.id,place=place.name,latitude=place.latitude,longitude=place.longitude,
            arrival_time=clock(arrival),departure_time=clock(departure),stay_minutes=place.average_stay_minutes,
            travel_minutes=travel,congestion_score=scores[place.id],reason="이동시간, 운영시간, 관심사를 고려한 방문 순서입니다."))
        current,position = departure,(place.latitude,place.longitude)
        remaining.remove(place)
    return route
