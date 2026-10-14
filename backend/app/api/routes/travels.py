from fastapi import APIRouter, Depends, Query
from typing import Literal
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import AuthenticatedUser, current_user
from app.core.database import get_session
from app.schemas.travel import SavedTravel, SavedTravelList, RenameTravelRequest
from app.schemas.recommendation import RecommendationResponse
from app.services.plan_service import PlanService

router = APIRouter(prefix="/travels", tags=["my travels"])


@router.get("",response_model=SavedTravelList)
async def list_travels(offset: int = Query(default=0,ge=0),limit: int = Query(default=12,ge=1,le=50),period: Literal["upcoming","past","all"] = "upcoming",
    session: AsyncSession = Depends(get_session),auth: AuthenticatedUser = Depends(current_user)) -> SavedTravelList:
    return await PlanService(session,auth.user.id).list_saved(offset,limit,period)


@router.get("/{plan_id}",response_model=SavedTravel)
async def get_travel(plan_id: str,session: AsyncSession = Depends(get_session),
    auth: AuthenticatedUser = Depends(current_user)) -> SavedTravel:
    service = PlanService(session,auth.user.id)
    return service.present(await service.get_saved(plan_id))


@router.patch("/{plan_id}",response_model=SavedTravel)
async def rename_travel(plan_id: str,body: RenameTravelRequest,session: AsyncSession = Depends(get_session),
    auth: AuthenticatedUser = Depends(current_user)) -> SavedTravel:
    return await PlanService(session,auth.user.id).rename(plan_id,body.title)


@router.post("/{plan_id}/select",response_model=RecommendationResponse)
async def select_travel(plan_id: str,session: AsyncSession = Depends(get_session),
    auth: AuthenticatedUser = Depends(current_user)) -> RecommendationResponse:
    return await PlanService(session,auth.user.id).select_saved(plan_id)
