from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base, TimestampMixin

class CongestionRecord(TimestampMixin, Base):
    __tablename__ = "congestion_records"
    id: Mapped[int] = mapped_column(primary_key=True)
    place_id: Mapped[int] = mapped_column(ForeignKey("tourist_places.id"), index=True)
    timestamp: Mapped[datetime]
    traffic_score: Mapped[float]
    pedestrian_score: Mapped[float]
    weather_score: Mapped[float]
    visitor_score: Mapped[float]
    congestion_score: Mapped[float]
    congestion_level: Mapped[str]
    predicted_1h: Mapped[float | None]
    predicted_2h: Mapped[float | None]
    predicted_3h: Mapped[float | None]
