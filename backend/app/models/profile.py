from sqlalchemy import ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base, TimestampMixin


class UserPreferences(Base):
    __tablename__ = "user_preferences"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    settings: Mapped[dict] = mapped_column(JSON)


class FavoritePlace(TimestampMixin, Base):
    __tablename__ = "favorite_places"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    place_id: Mapped[int] = mapped_column(primary_key=True)
    place: Mapped[dict] = mapped_column(JSON)
