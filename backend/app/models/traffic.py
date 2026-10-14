from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base, TimestampMixin

class TrafficRecord(TimestampMixin, Base):
    __tablename__ = "traffic_records"
    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str]
    location_name: Mapped[str]
    link_id: Mapped[str]
    latitude: Mapped[float]
    longitude: Mapped[float]
    timestamp: Mapped[datetime]
    avg_speed: Mapped[float]
    traffic_volume: Mapped[int]
    pedestrian_count: Mapped[int]
    queue_length: Mapped[int]
    travel_time: Mapped[float]
