from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    openai_api_key: str
    database_url: str
    faiss_index_path: str = "faiss_index/"
    openai_model: str = "gpt-4o-mini"
    embedding_model: str = "text-embedding-ada-002"
    environment: str = "development"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()