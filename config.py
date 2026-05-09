from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_env: Literal["dev", "prod"] = "dev"
    app_debug: bool = True
    log_level: str = "INFO"

    postgres_db: str = "assistant_db"
    postgres_user: str = "assistant"
    postgres_password: str = "assistant_password"
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    database_url: str = (
        "postgresql+psycopg://assistant:assistant_password@localhost:5432/assistant_db"
    )
    pgvector_connection_string: str = (
        "postgresql+psycopg://assistant:assistant_password@localhost:5432/assistant_db"
    )

    llm_provider: str = "ollama"
    llm_model: str = "qwen3:8b"
    embedding_model: str = "nomic-embed-text"
    llm_base_url: str = "http://localhost:11434"

    memory_top_k: int = Field(default=5, ge=1, le=50)
    memory_score_threshold: float = Field(default=0.75, ge=0.0, le=1.0)

    temperature: float = Field(default=0.7, ge=0.0, le=1.0)

    telegram_bot_token: str = ""
    allowed_telegram_ids: set[int] = set()

    llm_extractor_model: str = "llama3.2:1b"

    llm_vision_model: str = "ollama:llava_llama3"

    @property
    def is_dev(self) -> bool:
        return self.app_env == "development"

    @property
    def is_prod(self) -> bool:
        return self.app_env == "production"

    @field_validator("allowed_telegram_ids", mode="before")
    @classmethod
    def parse_telegram_ids(cls, v):
        if not v:
            return set()
        if isinstance(v, str):
            return {int(x.strip()) for x in v.split(",") if x.strip()}
        if isinstance(v, int):
            return {v}
        return v


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
