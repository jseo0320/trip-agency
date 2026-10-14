from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.concurrency import run_in_threadpool
from app.core.exceptions import AppError
from app.core.security import password_hasher
from app.models.user import User, AuthSession
from app.models.profile import UserPreferences, FavoritePlace
from app.schemas.profile import TravelPreferences, ChangePasswordRequest
from app.schemas.tourism import TouristPlaceResponse
from app.services.tourism_service import TourismService


class ProfileService:
    def __init__(self, session: AsyncSession, user_id: int) -> None:
        self.session,self.user_id=session,user_id

    async def preferences(self) -> TravelPreferences:
        row=await self.session.get(UserPreferences,self.user_id)
        return TravelPreferences.model_validate(row.settings) if row else TravelPreferences()

    async def save_preferences(self, body: TravelPreferences) -> TravelPreferences:
        statement=insert(UserPreferences).values(user_id=self.user_id,settings=body.model_dump())
        await self.session.execute(statement.on_conflict_do_update(index_elements=["user_id"],set_={"settings":body.model_dump()}))
        await self.session.commit()
        return body

    async def locked_user(self) -> User:
        user=await self.session.scalar(select(User).where(User.id==self.user_id).with_for_update().execution_options(populate_existing=True))
        if not user:
            raise AppError("UNAUTHORIZED","로그인이 필요합니다.",401)
        return user

    async def rename_user(self,name: str) -> User:
        user=await self.locked_user()
        user.name=name
        await self.session.commit()
        return user

    async def change_password(self,body: ChangePasswordRequest) -> None:
        user=await self.locked_user()
        if not await run_in_threadpool(password_hasher.verify,body.current_password,user.password_hash):
            raise AppError("INVALID_PASSWORD","현재 비밀번호가 올바르지 않습니다.",400)
        user.password_hash=await run_in_threadpool(password_hasher.hash,body.new_password)
        await self.session.execute(delete(AuthSession).where(AuthSession.user_id==self.user_id))
        await self.session.commit()

    async def favorites(self) -> list[TouristPlaceResponse]:
        rows=await self.session.scalars(select(FavoritePlace).where(FavoritePlace.user_id==self.user_id).order_by(FavoritePlace.created_at.desc()))
        return [TouristPlaceResponse.model_validate(row.place) for row in rows]

    async def add_favorite(self,place_id: int) -> TouristPlaceResponse:
        place=await TourismService(self.session).get(place_id)
        statement=insert(FavoritePlace).values(user_id=self.user_id,place_id=place.id,place=place.model_dump(mode="json"))
        await self.session.execute(statement.on_conflict_do_nothing(index_elements=["user_id","place_id"]))
        await self.session.commit()
        return place

    async def remove_favorite(self,place_id: int) -> None:
        await self.session.execute(delete(FavoritePlace).where(FavoritePlace.user_id==self.user_id,FavoritePlace.place_id==place_id))
        await self.session.commit()
