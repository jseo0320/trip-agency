from fastapi import APIRouter, Depends
from app.api.dependencies import current_user, AuthenticatedUser
from app.core.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import reply_to_chat
router = APIRouter(prefix="/ai",tags=["ai"], dependencies=[Depends(current_user)])

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, session: AsyncSession = Depends(get_session),
    auth: AuthenticatedUser = Depends(current_user)) -> ChatResponse:
    return await reply_to_chat(request, session, auth.user.id)
