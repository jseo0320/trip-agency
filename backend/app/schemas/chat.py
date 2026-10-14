from typing import Literal
from pydantic import BaseModel, Field, model_validator
from datetime import time
from app.schemas.recommendation import RecommendationResponse


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=6000)


class ChatRequest(BaseModel):
    # Retain compatibility with the original single-message endpoint.
    message: str | None = Field(default=None, min_length=1, max_length=4000)
    messages: list[ChatMessage] = Field(default_factory=list, max_length=20)

    @model_validator(mode="after")
    def check_history(self) -> "ChatRequest":
        if self.message is not None and self.messages:
            raise ValueError("message와 messages 중 하나만 전달하세요.")
        if self.message is not None:
            self.messages = [ChatMessage(role="user", content=self.message)]
        if not self.messages or self.messages[-1].role != "user":
            raise ValueError("마지막 메시지는 사용자 메시지여야 합니다.")
        if sum(len(m.content) for m in self.messages) > 24000:
            raise ValueError("대화가 너무 깁니다. 새 대화를 시작하세요.")
        return self


class ChatResponse(BaseModel):
    message: str
    model: str
    current_plan: RecommendationResponse | None = None
    proposed_plan: RecommendationResponse | None = None


class RevisionIntent(BaseModel):
    revise: bool = Field(description="현재 코스에 대해 관광지 대체, 제외, 시간 조정 등 변경을 요청하면 true. 단순 정보 질문이면 false.")
    change_from: str | None = Field(default=None, description="변경 시작 시각 HH:MM. 저녁=18:00, 오후=13:00, 오전=09:00. 전 일정 변경이면 null.")
    indoor_only: bool = Field(default=False, description="비나 날씨를 피해 실내 장소로 대체하라는 요청이면 true.")
    excluded_places: list[str] = Field(default_factory=list, max_length=20, description="사용자가 명시적으로 제외 요청한 관광지의 정확한 이름만.")
    must_visit: list[str] = Field(default_factory=list, max_length=20, description="이번 변경에서 사용자가 명시적으로 새로 방문 요청한 관광지 이름만.")

    @model_validator(mode="after")
    def check_time(self) -> "RevisionIntent":
        if self.change_from is not None:
            value = time.fromisoformat(self.change_from)
            self.change_from = value.strftime("%H:%M")
        return self
