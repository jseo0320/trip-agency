import json
from app.ai.llm import get_llm
from app.ai.prompts.trip_agency_prompt import SYSTEM_PROMPT
from app.schemas.recommendation import RouteStop

async def explain_route(route: list[RouteStop]) -> str:
    response = await get_llm().ainvoke([("system", SYSTEM_PROMPT), ("human", json.dumps([s.model_dump() for s in route],ensure_ascii=False))])
    return str(response.content)
