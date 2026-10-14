from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.schemas.recommendation import TravelRequest, RecommendationResponse
from app.services.recommendation_service import RecommendationService
from app.api.dependencies import current_user, AuthenticatedUser
from app.services.plan_service import PlanService
router = APIRouter(tags=["recommendations"])

@router.post("/recommendations", response_model=RecommendationResponse, dependencies=[Depends(current_user)])
async def recommend(request: TravelRequest, session: AsyncSession = Depends(get_session),
    auth: AuthenticatedUser = Depends(current_user)) -> RecommendationResponse:
    result = await RecommendationService(session).recommend(request)
    return await PlanService(session, auth.user.id).save(request, result)

@router.get("/recommendations/current", response_model=RecommendationResponse | None)
async def current_plan(session: AsyncSession = Depends(get_session),
    auth: AuthenticatedUser = Depends(current_user)) -> RecommendationResponse | None:
    plan = await PlanService(session, auth.user.id).current()
    return PlanService(session,auth.user.id).present(plan).result if plan else None

@router.post("/recommendations/{plan_id}/apply", response_model=RecommendationResponse)
async def apply_plan(plan_id: str, session: AsyncSession = Depends(get_session),
    auth: AuthenticatedUser = Depends(current_user)) -> RecommendationResponse:
    return await PlanService(session, auth.user.id).apply(plan_id)
