import pandas as pd

FEATURES = ["city", "place_id", "month", "day", "hour", "weekday", "weekend", "holiday", "temperature", "rainfall", "humidity", "wind_speed", "avg_speed", "traffic_volume", "pedestrian_count", "queue_length", "previous_congestion", "previous_1h", "previous_2h"]

def prepare_features(frame: pd.DataFrame) -> pd.DataFrame:
    result = frame[FEATURES].copy()
    result["city"] = result["city"].map({"busan":0,"ulsan":1,"gyeongju":2}).fillna(-1)
    return result.fillna(0)
