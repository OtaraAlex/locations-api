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
        if not value.strip():
            raise ValueError("DATABASE_URL cannot be empty.")
        return value

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
