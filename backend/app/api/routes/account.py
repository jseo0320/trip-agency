from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import AuthenticatedUser,current_user
from app.core.database import get_session
from app.core.config import get_settings
from app.core.security import COOKIE_NAME
from app.schemas.auth import UserResponse
from app.schemas.profile import TravelPreferences,UpdateProfileRequest,ChangePasswordRequest
from app.schemas.tourism import TouristPlaceResponse
from app.services.profile_service import ProfileService

router=APIRouter(prefix="/account",tags=["account"])


@router.get("/preferences",response_model=TravelPreferences)
async def get_preferences(session: AsyncSession=Depends(get_session),auth: AuthenticatedUser=Depends(current_user)) -> TravelPreferences:
    return await ProfileService(session,auth.user.id).preferences()


@router.put("/preferences",response_model=TravelPreferences)
async def set_preferences(body: TravelPreferences,session: AsyncSession=Depends(get_session),auth: AuthenticatedUser=Depends(current_user)) -> TravelPreferences:
    return await ProfileService(session,auth.user.id).save_preferences(body)


@router.patch("/profile",response_model=UserResponse)
async def update_profile(body: UpdateProfileRequest,session: AsyncSession=Depends(get_session),auth: AuthenticatedUser=Depends(current_user)) -> UserResponse:
    return UserResponse.model_validate(await ProfileService(session,auth.user.id).rename_user(body.name))


@router.post("/password",status_code=204)
async def change_password(body: ChangePasswordRequest,session: AsyncSession=Depends(get_session),auth: AuthenticatedUser=Depends(current_user)) -> Response:
    await ProfileService(session,auth.user.id).change_password(body)
    response=Response(status_code=204)
    response.delete_cookie(COOKIE_NAME,path="/api/v1",secure=get_settings().auth_cookie_secure,httponly=True,samesite="lax")
    return response


@router.get("/favorites",response_model=list[TouristPlaceResponse])
async def favorites(session: AsyncSession=Depends(get_session),auth: AuthenticatedUser=Depends(current_user)) -> list[TouristPlaceResponse]:
    return await ProfileService(session,auth.user.id).favorites()


@router.put("/favorites/{place_id}",response_model=TouristPlaceResponse)
async def add_favorite(place_id: int,session: AsyncSession=Depends(get_session),auth: AuthenticatedUser=Depends(current_user)) -> TouristPlaceResponse:
    return await ProfileService(session,auth.user.id).add_favorite(place_id)


@router.delete("/favorites/{place_id}",status_code=204)
async def remove_favorite(place_id: int,session: AsyncSession=Depends(get_session),auth: AuthenticatedUser=Depends(current_user)) -> Response:
    await ProfileService(session,auth.user.id).remove_favorite(place_id)
    return Response(status_code=204)
