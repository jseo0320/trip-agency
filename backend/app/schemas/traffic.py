from datetime import datetime
from pydantic import BaseModel, ConfigDict

class TrafficResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    city: str
    timestamp: datetime
    avg_speed: float
    traffic_volume: int
    pedestrian_count: int
    queue_length: int
    source: str = "database"
