from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_documents(documents: list[Document]) -> list[Document]:
    return RecursiveCharacterTextSplitter(chunk_size=800,chunk_overlap=100).split_documents(documents)
