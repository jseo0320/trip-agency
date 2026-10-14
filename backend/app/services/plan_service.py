from uuid import uuid4
from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import AppError
from app.models.travel_plan import TravelPlan
from app.models.user import User
from app.schemas.recommendation import TravelRequest, RecommendationResponse
from app.schemas.travel import SavedTravel, SavedTravelList
from app.utils.datetime import now_korea


class PlanService:
    def __init__(self, session: AsyncSession, user_id: int) -> None:
        self.session, self.user_id = session, user_id

    async def current(self) -> TravelPlan | None:
        return await self.session.scalar(select(TravelPlan).where(
            TravelPlan.user_id == self.user_id, TravelPlan.status == "active").order_by(TravelPlan.created_at.desc()).limit(1))

    async def lock_user(self) -> None:
        await self.session.execute(select(User.id).where(User.id == self.user_id).with_for_update())

    async def save(self, request: TravelRequest, result: RecommendationResponse,
        parent_id: str | None = None) -> RecommendationResponse:
        await self.lock_user()
        if parent_id is None:
            await self.session.execute(update(TravelPlan).where(TravelPlan.user_id == self.user_id,
                TravelPlan.status == "active").values(status="superseded"))
        else:
            current = await self.current()
            if not current or current.id != parent_id:
                raise AppError("PLAN_CHANGED", "현재 코스가 변경되었습니다. 다시 요청하세요.", 409)
        plan_id = uuid4().hex
        title = request.title.strip()
        if parent_id:
            title = self.present(current).title
        if not title:
            city_names = {"busan":"부산", "ulsan":"울산", "gyeongju":"경주"}
            title = f"{request.travel_date.isoformat()} {' · '.join(city_names.get(city,city) for city in request.cities)} 여행"
        title = title[:80]
        result = result.model_copy(update={"plan_id": plan_id,"title":title})
        request = request.model_copy(update={"title":title})
        self.session.add(TravelPlan(id=plan_id, user_id=self.user_id, parent_id=parent_id,
            status="draft" if parent_id else "active", request=request.model_dump(mode="json"),
            result=result.model_dump(mode="json")))
        await self.session.commit()
        return result

    async def apply(self, plan_id: str) -> RecommendationResponse:
        await self.lock_user()
        draft = await self.session.scalar(select(TravelPlan).where(
            TravelPlan.id == plan_id, TravelPlan.user_id == self.user_id))
        if not draft:
            raise AppError("DATA_NOT_FOUND", "변경안을 찾을 수 없습니다.", 404)
        current = await self.current()
        if draft.status == "active" and current and current.id == draft.id:
            return RecommendationResponse.model_validate(draft.result)
        if draft.status != "draft" or not current or current.id != draft.parent_id:
            raise AppError("PLAN_CHANGED", "이 변경안은 이전 코스를 기준으로 합니다. 새 변경안을 요청하세요.", 409)
        current.status = "superseded"
        draft.status = "active"
        await self.session.commit()
        return RecommendationResponse.model_validate(draft.result)

    def present(self, plan: TravelPlan) -> SavedTravel:
        result = RecommendationResponse.model_validate(plan.result)
        title = result.title or f"{result.travel_date.isoformat()} 여행"
        result = result.model_copy(update={"title":title,"plan_id":plan.id})
        return SavedTravel(id=plan.id,title=title,created_at=plan.created_at,
            is_current=plan.status == "active",is_revision=plan.parent_id is not None,result=result)

    async def get_saved(self, plan_id: str) -> TravelPlan:
        plan = await self.session.scalar(select(TravelPlan).where(TravelPlan.id == plan_id,
            TravelPlan.user_id == self.user_id,TravelPlan.status.in_(["active","superseded"])))
        if not plan:
            raise AppError("DATA_NOT_FOUND", "저장된 여행을 찾을 수 없습니다.", 404)
        return plan

    async def list_saved(self, offset: int, limit: int, period: str = "upcoming") -> SavedTravelList:
        filters = [TravelPlan.user_id == self.user_id,TravelPlan.status.in_(["active","superseded"])]
        today=now_korea().date().isoformat()
        if period == "upcoming":
            filters.append(TravelPlan.result["travel_date"].as_string() >= today)
        elif period == "past":
            filters.append(TravelPlan.result["travel_date"].as_string() < today)
        total = await self.session.scalar(select(func.count()).select_from(TravelPlan).where(*filters))
        plans = await self.session.scalars(select(TravelPlan).where(*filters)
            .order_by(TravelPlan.created_at.desc(),TravelPlan.id.desc()).offset(offset).limit(limit))
        return SavedTravelList(items=[self.present(plan) for plan in plans],total=total or 0)

    async def rename(self, plan_id: str, title: str) -> SavedTravel:
        await self.lock_user()
        plan = await self.get_saved(plan_id)
        plan.result = {**plan.result,"title":title}
        plan.request = {**plan.request,"title":title}
        # Outstanding proposals inherit the current travel's name too.
        drafts = await self.session.scalars(select(TravelPlan).where(TravelPlan.user_id == self.user_id,
            TravelPlan.parent_id == plan.id,TravelPlan.status == "draft"))
        for draft in drafts:
            draft.result = {**draft.result,"title":title}
            draft.request = {**draft.request,"title":title}
        await self.session.commit()
        return self.present(plan)

    async def select_saved(self, plan_id: str) -> RecommendationResponse:
        await self.lock_user()
        plan = await self.get_saved(plan_id)
        await self.session.execute(update(TravelPlan).where(TravelPlan.user_id == self.user_id,
            TravelPlan.status == "active").values(status="superseded"))
        plan.status = "active"
        await self.session.commit()
        return self.present(plan).result
