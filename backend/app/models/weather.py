from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base, TimestampMixin

class WeatherRecord(TimestampMixin, Base):
    __tablename__ = "weather_records"
    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str]
    latitude: Mapped[float]
    longitude: Mapped[float]
    timestamp: Mapped[datetime]
    temperature: Mapped[float]
    rainfall: Mapped[float]
    humidity: Mapped[float]
    wind_speed: Mapped[float]
    sky_condition: Mapped[str]
