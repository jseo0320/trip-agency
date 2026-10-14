from pathlib import Path
from langchain_core.documents import Document

def load_documents(directory: str) -> list[Document]:
    return [Document(page_content=p.read_text(encoding="utf-8"),metadata={"source":str(p)}) for p in Path(directory).glob("*.md")]
