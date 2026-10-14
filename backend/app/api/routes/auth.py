from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import AuthenticatedUser, check_origin, current_user
from app.core.config import get_settings
from app.core.database import get_session
from app.core.security import COOKIE_NAME
from app.repositories.user_repository import UserRepository
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, UserResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"], dependencies=[Depends(check_origin)])


def set_login_cookie(response: Response, token: TokenResponse) -> None:
    response.headers["Cache-Control"] = "no-store"
    response.set_cookie(COOKIE_NAME, token.access_token, max_age=token.expires_in,
        httponly=True, secure=get_settings().auth_cookie_secure, samesite="lax", path="/api/v1")


@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(body: RegisterRequest, response: Response,
    session: AsyncSession = Depends(get_session)) -> TokenResponse:
    token = await AuthService(session).register(body)
    set_login_cookie(response, token)
    return token


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, response: Response,
    session: AsyncSession = Depends(get_session)) -> TokenResponse:
    token = await AuthService(session).login(body)
    set_login_cookie(response, token)
    return token


@router.get("/me", response_model=UserResponse)
async def me(response: Response, auth: AuthenticatedUser = Depends(current_user)) -> UserResponse:
    response.headers["Cache-Control"] = "no-store"
    return UserResponse.model_validate(auth.user)


@router.post("/logout", status_code=204)
async def logout(auth: AuthenticatedUser = Depends(current_user),
    session: AsyncSession = Depends(get_session)) -> Response:
    await UserRepository(session).revoke(auth.session_id)
    await session.commit()
    response = Response(status_code=204, headers={"Cache-Control": "no-store"})
    response.delete_cookie(COOKIE_NAME, path="/api/v1", secure=get_settings().auth_cookie_secure, httponly=True, samesite="lax")
    return response
