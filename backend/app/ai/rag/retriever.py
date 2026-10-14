from langchain_core.documents import Document
from app.ai.rag.vectorstore import get_vectorstore

async def retrieve(query: str) -> list[Document]:
    return await get_vectorstore().as_retriever(search_kwargs={"k":4}).ainvoke(query)
