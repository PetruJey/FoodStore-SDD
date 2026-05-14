from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    database_url: str = Field(
        default="postgresql+asyncpg://user:password@localhost:5432/foodstore",
        validation_alias="DATABASE_URL",
    )
    secret_key: str = Field(
        default="cambia-esto-por-una-clave-de-64-caracteres-minimo",
        validation_alias="SECRET_KEY",
    )
    algorithm: str = Field(default="HS256", validation_alias="ALGORITHM")
    access_token_expire_minutes: int = Field(
        default=30, validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES"
    )
    refresh_token_expire_days: int = Field(
        default=7, validation_alias="REFRESH_TOKEN_EXPIRE_DAYS"
    )
    cors_origins: list[str] = Field(
        default=["http://localhost:5173"], validation_alias="CORS_ORIGINS"
    )
    mp_access_token: str = Field(
        default="", validation_alias="MP_ACCESS_TOKEN"
    )
    mp_public_key: str = Field(
        default="", validation_alias="MP_PUBLIC_KEY"
    )
    mp_notification_url: str = Field(
        default="", validation_alias="MP_NOTIFICATION_URL"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
