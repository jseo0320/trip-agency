from pydantic import BaseModel

class CongestionValue(BaseModel):
    score: float
    level: str

class Forecast(BaseModel):
    hour: int
    score: float

class CongestionResponse(BaseModel):
    place_id: int
    place_name: str
    current: CongestionValue
    forecast: list[Forecast]
    source: str
