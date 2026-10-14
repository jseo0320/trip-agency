import logging
from typing import Any
import httpx
from app.core.exceptions import AppError
logger = logging.getLogger(__name__)

class ExternalClient:
    """공공 API별 URL·파라미터·응답 매핑을 연결하는 비동기 인터페이스."""
    def __init__(self, base_url: str, api_key: str = "") -> None:
        self.base_url, self.api_key = base_url, api_key

    async def fetch(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        if not self.base_url:
            raise AppError("EXTERNAL_API_NOT_CONFIGURED", "공공 API 주소와 응답 매핑 설정이 필요합니다.",503)
        try:
            async with httpx.AsyncClient(base_url=self.base_url,timeout=15) as client:
                response = await client.get(path,params={**(params or {}),"serviceKey":self.api_key})
                response.raise_for_status()
                payload = response.json()
                if not isinstance(payload,dict):
                    raise ValueError("Expected object response")
                return payload
        except (httpx.HTTPError, ValueError) as exc:
            logger.warning("External provider request failed")
            raise AppError("EXTERNAL_API_ERROR","외부 정보를 가져올 수 없습니다. 저장 데이터 사용이 필요합니다.",502) from exc
