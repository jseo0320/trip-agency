from langchain_ollama import ChatOllama
from app.core.config import get_settings

def get_llm(timeout: float = 20) -> ChatOllama:
    settings = get_settings()
    return ChatOllama(base_url=settings.ollama_base_url, model=settings.ollama_model, temperature=0,
        reasoning=False, num_predict=1536, client_kwargs={"timeout":timeout})
