import argparse
from app.ai.rag.loader import load_documents
from app.ai.rag.splitter import split_documents
from app.ai.rag.vectorstore import get_vectorstore

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("directory")
    args = parser.parse_args()
    documents = split_documents(load_documents(args.directory))
    if documents:
        get_vectorstore().add_documents(documents)

if __name__ == "__main__":
    main()
