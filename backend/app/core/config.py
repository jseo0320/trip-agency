from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    app_name: str = "Trip Agency"
    app_env: str = "development"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/trip_agency"
    use_mock_data: bool = True
    cors_origins: list[str] = ["http://localhost:5173"]
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen3:8b"
    ollama_embedding_model: str = "qwen3-embedding:0.6b"
    enable_llm: bool = False
    chroma_path: str = "./data/chroma"
    busan_traffic_api_key: str = ""
    busan_intersection_api_key: str = ""
    busan_bus_api_key: str = ""
    ulsan_traffic_api_key: str = ""
    ulsan_bus_api_key: str = ""
    gyeongju_tour_api_key: str = ""
    tour_api_key: str = ""
    weather_api_key: str = ""
    holiday_api_key: str = ""
    jwt_secret_key: str = ""
    jwt_issuer: str = "trip-agency"
    jwt_audience: str = "trip-agency-web"
    jwt_expire_minutes: int = Field(default=30, ge=1, le=1440)
    auth_cookie_secure: bool = False

@lru_cache
def get_settings() -> Settings:
    return Settings()
