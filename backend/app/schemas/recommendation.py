from datetime import date, time
from typing import Literal
from pydantic import BaseModel, Field, model_validator
from app.utils.datetime import now_korea

class TravelRequest(BaseModel):
    title: str = Field(default="", max_length=80)
    travel_date: date = Field(default_factory=lambda: now_korea().date())
    start_location: str = Field(default="부산역", min_length=1, max_length=200)
    start_latitude: float | None = Field(default=None, ge=-90, le=90)
    start_longitude: float | None = Field(default=None, ge=-180, le=180)
    start_time: time = time(10)
    end_time: time = time(21)
    indoor_from: time | None = None
    cities: list[Literal["busan", "ulsan", "gyeongju", "부산", "울산", "경주"]] = Field(default_factory=lambda: ["busan"], min_length=1)
    preferences: list[str] = Field(default_factory=list)
    avoid_congestion: bool = True
    transportation: Literal["public", "car"] = "public"
    walking_preference: Literal["low", "normal", "high"] = "normal"
    must_visit: list[str] = Field(default_factory=list)
    excluded_places: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def check_schedule(self) -> "TravelRequest":
        if self.travel_date < now_korea().date():
            raise ValueError("여행 날짜는 오늘 이후로 선택하세요.")
        if self.end_time <= self.start_time:
            raise ValueError("종료시간은 출발시간 이후여야 합니다. 당일 일정만 지원합니다.")
        if (self.start_latitude is None) != (self.start_longitude is None):
            raise ValueError("출발 좌표는 위도와 경도를 함께 입력하세요.")
        return self

class RouteStop(BaseModel):
    order: int
    place_id: int
    place: str
    latitude: float
    longitude: float
    arrival_time: str
    departure_time: str
    stay_minutes: int
    travel_minutes: int
    congestion_score: float
    reason: str

class RecommendationResponse(BaseModel):
    title: str = ""
    plan_id: str | None = None
    travel_date: date
    summary: str
    route: list[RouteStop]
    warnings: list[str] = Field(default_factory=list)
    source: str
