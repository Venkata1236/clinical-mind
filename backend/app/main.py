from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from loguru import logger

from app.core.config import get_settings
from app.database.connection import init_db
from app.rag.embedder import load_faiss_index
from app.rag.retriever import FAISSRetriever
from app.agents.crew import ClinicalMindCrew
from app.routes.eligibility import router as eligibility_router
from app.models.schemas import HealthResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    logger.info("Starting ClinicalMind API...")

    # Try DB init but don't crash if it fails locally
    try:
        await init_db()
    except Exception as e:
        logger.warning(f"DB init skipped (no local PostgreSQL): {e}")

    # FAISS index load
    try:
        vectorstore = load_faiss_index(settings.faiss_index_path)
        retriever = FAISSRetriever(vectorstore)
        app.state.crew = ClinicalMindCrew(retriever)
        logger.info("FAISS index loaded. Crew initialized. API ready.")
    except Exception as e:
        logger.warning(f"FAISS index not found yet: {e}")
        app.state.crew = None

    yield

    logger.info("ClinicalMind API shutting down")


app = FastAPI(
    title="ClinicalMind API",
    description="Clinical trial patient eligibility matching via RAG + CrewAI",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://clinical-mind.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(eligibility_router, prefix="/api/v1", tags=["eligibility"])


@app.get("/health", response_model=HealthResponse)
async def health(request: Request):
    return HealthResponse(
        status="ok",
        environment=get_settings().environment,
        faiss_index_loaded=hasattr(request.app.state, "crew"),
    )