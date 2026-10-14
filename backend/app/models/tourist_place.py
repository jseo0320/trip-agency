from datetime import datetime, time
from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base, TimestampMixin

class TouristPlace(TimestampMixin, Base):
    __tablename__ = "tourist_places"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    city: Mapped[str] = mapped_column(String(30), index=True)
    category: Mapped[str] = mapped_column(String(50))
    address: Mapped[str] = mapped_column(String(300))
    latitude: Mapped[float]
    longitude: Mapped[float]
    description: Mapped[str] = mapped_column(Text)
    opening_time: Mapped[time]
    closing_time: Mapped[time]
    average_stay_minutes: Mapped[int]
    source: Mapped[str] = mapped_column(String(100))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
