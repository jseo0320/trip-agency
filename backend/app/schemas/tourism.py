from datetime import time
from pydantic import BaseModel, ConfigDict

class TouristPlaceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    city: str
    category: str
    address: str
    latitude: float
    longitude: float
    description: str
    opening_time: time
    closing_time: time
    average_stay_minutes: int
    source: str
