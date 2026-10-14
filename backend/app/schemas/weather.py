from datetime import datetime
from pydantic import BaseModel, ConfigDict

class WeatherResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    city: str
    timestamp: datetime
    temperature: float
    rainfall: float
    humidity: float
    wind_speed: float
    sky_condition: str
    source: str = "database"
