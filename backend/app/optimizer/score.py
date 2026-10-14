def congestion_score(traffic: float, pedestrian: float, visitor: float, weather: float) -> float:
    return round(min(100, max(0, traffic * .35 + pedestrian * .25 + visitor * .25 + weather * .15)), 1)

def congestion_level(score: float) -> str:
    return "여유" if score <= 25 else "보통" if score <= 50 else "혼잡" if score <= 75 else "매우 혼잡"

def route_cost(travel_minutes: float, congestion: float, preference_penalty: float, opening_penalty: float) -> float:
    return travel_minutes * .35 + congestion * .35 + preference_penalty * .20 + opening_penalty * .10
