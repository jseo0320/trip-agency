from fastapi import APIRouter
from app.core.config import get_settings
router = APIRouter(tags=["health"])

@router.get("/health")
async def health() -> dict[str, str]:
    return {"status":"ok", "service":"Trip Agency", "mode":"mock" if get_settings().use_mock_data else "database"}
