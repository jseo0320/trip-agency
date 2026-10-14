from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
import logging
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import router
from app.api.routes.health import router as health_router
from app.core.config import get_settings
from app.core.database import create_tables, create_auth_tables, engine
from app.core.exceptions import AppError, app_error_handler
from app.core.logging import configure_logging
configure_logging()
settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    from app.core.security import require_jwt_secret
    require_jwt_secret()
    await create_auth_tables()
    if not settings.use_mock_data:
        await create_tables()
    yield
    await engine.dispose()

app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.add_exception_handler(AppError, app_error_handler)

@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(status_code=422,content={"error":{"code":"VALIDATION_ERROR","message":"입력값을 확인하세요.","details":[{"field":".".join(map(str,e["loc"])),"message":e["msg"]} for e in exc.errors()]}})

@app.exception_handler(Exception)
async def unexpected_handler(request: Request, exc: Exception) -> JSONResponse:
    logging.getLogger(__name__).exception("Unhandled request error")
    return JSONResponse(status_code=500,content={"error":{"code":"INTERNAL_ERROR","message":"요청 처리 중 오류가 발생했습니다."}})

app.include_router(router)
app.include_router(health_router)
