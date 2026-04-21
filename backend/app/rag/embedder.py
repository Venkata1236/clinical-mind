from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from loguru import logger
import os

from app.core.config import get_settings


def build_faiss_index(chunks: list[Document]) -> FAISS:
    """
    Embed all chunks using OpenAI and build FAISS index.
    text-embedding-ada-002 → 1536-dim vectors.
    """
    settings = get_settings()

    logger.info(f"Building FAISS index with {len(chunks)} chunks...")

    embeddings = OpenAIEmbeddings(
        model=settings.embedding_model,
        openai_api_key=settings.openai_api_key,
    )

    vectorstore = FAISS.from_documents(chunks, embeddings)
    logger.info("FAISS index built successfully")
    return vectorstore


def save_faiss_index(vectorstore: FAISS, path: str = None) -> None:
    settings = get_settings()
    save_path = path or settings.faiss_index_path
    os.makedirs(save_path, exist_ok=True)
    vectorstore.save_local(save_path)
    logger.info(f"FAISS index saved to: {save_path}")


def load_faiss_index(path: str = None) -> FAISS:
    settings = get_settings()
    load_path = path or settings.faiss_index_path

    embeddings = OpenAIEmbeddings(
        model=settings.embedding_model,
        openai_api_key=settings.openai_api_key,
    )

    vectorstore = FAISS.load_local(
        load_path,
        embeddings,
        allow_dangerous_deserialization=True,  # required by LangChain for local FAISS
    )
    logger.info(f"FAISS index loaded from: {load_path}")
    return vectorstore


def build_and_save_index() -> FAISS:
    """
    One-time pipeline: load docs → chunk → embed → save.
    Run this once manually before starting the API.
    """
    from app.rag.loader import load_trial_documents, chunk_documents

    documents = load_trial_documents()
    if not documents:
        raise RuntimeError("No trial documents found in data/trials/. Add .txt files first.")

    chunks = chunk_documents(documents)
    vectorstore = build_faiss_index(chunks)
    save_faiss_index(vectorstore)
    return vectorstore