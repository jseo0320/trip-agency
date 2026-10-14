from langchain_ollama import OllamaEmbeddings
from app.core.config import get_settings

def get_embeddings() -> OllamaEmbeddings:
    settings = get_settings()
    return OllamaEmbeddings(base_url=settings.ollama_base_url, model=settings.ollama_embedding_model)
