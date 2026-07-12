from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from typing import Literal



class Settings(BaseSettings):
    APP_NAME: str = "gov-support-rag-chatbot"
    APP_VERSION: str = "0.0.1"
    DATABASE_URL: SecretStr
    EMBEDDING_MODEL_NAME: str
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"
    LLM_API_KEY: SecretStr
    LOG_LEVEL: Literal["debug", "info", "warning", "error"] = "debug"
    MONGO_DB_URI: SecretStr
    MONGO_DB_NAME: str
    PINECONE_API_KEY: SecretStr
    PINECONE_INDEX_NAME: str
    RATE_LIMIT_PER_MINUTE: int = 5
    


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()