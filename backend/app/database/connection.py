from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from loguru import logger

from app.core.config import get_settings

Base = declarative_base()

engine = None
AsyncSessionLocal = None


async def init_db():
    global engine, AsyncSessionLocal

    settings = get_settings()
    engine = create_async_engine(
        settings.database_url,
        echo=settings.environment == "development",
    )
    AsyncSessionLocal = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info("Database initialized and tables created")


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session