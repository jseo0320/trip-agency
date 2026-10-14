from fastapi import APIRouter
from app.api.routes import tourism, traffic, weather, congestion, recommendation, health, ai, auth, travels, account
router = APIRouter(prefix="/api/v1")
for module in [tourism,traffic,weather,congestion,recommendation,health,ai,auth,travels,account]:
    router.include_router(module.router)
