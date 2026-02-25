import os
from pydantic_settings import BaseSettings
from .constant import MAX_FILE_SIZE , MAX_TOTAL_SIZE , ALLOWED_TYPES


class Settings(BaseSettings):

    LLM_API_KEY: str = os.environ["GH_OPENAI_TOKEN"]

    MAX_FILE_SIZE: int = MAX_FILE_SIZE
    MAX_TOTAL_SIZE: int = MAX_TOTAL_SIZE
    ALLOWED_TYPES: tuple = ALLOWED_TYPES

    CHROMA_DB_PATH: str ="./chroma_db"
    CHROMA_COLLECTION_NAME: str = "documents"

    WEAVIATE_DB_PATH: str ="./weaviate_data"

    VECTOR_SEARCH_K:int =10
    HYBRID_RETRIEVER_WEIGHTS: list = [0.4, 0.6]

    # Logging settings
    LOG_LEVEL: str = "INFO"

    # New cache settings with type annotations
    CACHE_DIR: str = "_cache"
    CACHE_EXPIRE_DAYS: int = 7

    # class Config:
    #     env_file = ".env"
    #     env_file_encoding = "utf-8"

settings = Settings()