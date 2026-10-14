from langchain_chroma import Chroma
from app.core.config import get_settings
from app.ai.rag.embeddings import get_embeddings

def get_vectorstore() -> Chroma:
    return Chroma(collection_name="trip_agency",embedding_function=get_embeddings(),persist_directory=get_settings().chroma_path)
