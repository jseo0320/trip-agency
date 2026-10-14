from math import radians, sin, cos, atan2, sqrt

def haversine(a: tuple[float, float], b: tuple[float, float]) -> float:
    lat1, lon1, lat2, lon2 = map(radians, (*a, *b))
    value = sin((lat2-lat1)/2)**2 + cos(lat1)*cos(lat2)*sin((lon2-lon1)/2)**2
    value = min(1.0, max(0.0, value))
    return 6371 * 2 * atan2(sqrt(value), sqrt(1-value))

def estimate_travel_minutes(a: tuple[float, float], b: tuple[float, float], transportation: str) -> int:
    speed = 25 if transportation == "public" else 40
    return max(5, round(haversine(a, b) * 1.35 / speed * 60 + (10 if transportation == "public" else 5)))
