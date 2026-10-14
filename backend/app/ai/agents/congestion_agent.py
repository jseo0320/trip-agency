from app.schemas.congestion import CongestionResponse

def describe_congestion(value: CongestionResponse) -> str:
    return f"{value.place_name}: {value.current.level} ({value.current.score}), 출처: {value.source}"
