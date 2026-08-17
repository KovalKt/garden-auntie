import glob
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

load_dotenv()

DOCS_PATH = "data/docs"
CHROMA_PATH = "chroma_db"


def load_documents(path: str):
    docs = []

    for pdf_path in glob.glob(f"{path}/**/*.pdf", recursive=True):
        print(f"Loading PDF: {pdf_path}")
        loader = PyPDFLoader(pdf_path)
        docs.extend(loader.load())

    for txt_path in glob.glob(f"{path}/**/*.txt", recursive=True):
        print(f"Loading TXT: {txt_path}")
        loader = TextLoader(txt_path, encoding="utf-8")
        docs.extend(loader.load())

    print(f"\nLoaded {len(docs)} pages/documents total.")
    return docs


def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", " ", ""],
    )
    chunks = splitter.split_documents(docs)
    print(f"Split into {len(chunks)} chunks.")
    return chunks


def ingest():
    print("--- Garden Auntie: Ingesting documents ---\n")

    docs = load_documents(DOCS_PATH)
    if not docs:
        print("No documents found! Add files to data/docs/ first.")
        return

    chunks = split_documents(docs)

    print("\nCreating embeddings and storing in ChromaDB...")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH,
    )

    print(f"\nDone! {len(chunks)} chunks stored in '{CHROMA_PATH}/'.")
    print("Run this script again any time you add new documents.")

    return vectorstore


if __name__ == "__main__":
    ingest()
