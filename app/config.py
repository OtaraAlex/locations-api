from pydantic import ValidationError, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Kenya Locations API"
    app_version: str = "1.0.0"
    database_url: str
    default_page_size: int = 20
    max_page_size: int = 100

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("DATABASE_URL cannot be empty.")
        if normalized.startswith("postgresql://"):
            return normalized.replace("postgresql://", "postgresql+psycopg://", 1)
        if normalized.startswith("postgres://"):
            return normalized.replace("postgres://", "postgresql+psycopg://", 1)
        return normalized

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

try:
    settings = Settings()
except ValidationError as exc:
    raise RuntimeError(
        "DATABASE_URL is required. Set it in .env or your deployment environment before starting the app."
    ) from exc
