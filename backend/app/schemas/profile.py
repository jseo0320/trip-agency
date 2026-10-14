from typing import Literal
from pydantic import BaseModel, Field, field_validator


class TravelPreferences(BaseModel):
    preferences: list[Literal["바다","카페","역사","맛집","자연","사진"]] = Field(default_factory=lambda:["바다"],max_length=6)
    transportation: Literal["public","car"] = "public"
    walking_preference: Literal["low","normal","high"] = "normal"
    avoid_congestion: bool = True

    @field_validator("preferences")
    @classmethod
    def unique_preferences(cls, value: list[str]) -> list[str]:
        return list(dict.fromkeys(value))


class UpdateProfileRequest(BaseModel):
    name: str = Field(min_length=1,max_length=80)

    @field_validator("name")
    @classmethod
    def clean_name(cls,value: str) -> str:
        value=value.strip()
        if not value:
            raise ValueError("이름을 입력하세요.")
        return value


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(min_length=1,max_length=128)
    new_password: str = Field(min_length=10,max_length=128)
