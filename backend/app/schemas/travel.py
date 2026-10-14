from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from app.schemas.recommendation import RecommendationResponse


class RenameTravelRequest(BaseModel):
    title: str = Field(min_length=1, max_length=80)

    @field_validator("title")
    @classmethod
    def strip_title(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("여행 이름을 입력하세요.")
        return value


class SavedTravel(BaseModel):
    id: str
    title: str
    created_at: datetime
    is_current: bool
    is_revision: bool
    result: RecommendationResponse


class SavedTravelList(BaseModel):
    items: list[SavedTravel]
    total: int
