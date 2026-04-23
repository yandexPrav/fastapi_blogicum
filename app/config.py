"""Настройки приложения (Pydantic Settings).

Все переменные окружения читаются из .env или из окружения процесса.
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Конфигурация приложения Blogicum."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_name: str = Field(default="Blogicum API")
    app_version: str = Field(default="1.0.0")
    debug: bool = Field(default=False)

    database_url: str = Field(
        default="sqlite:///./blogicum.db",
        description=(
            "SQLAlchemy URL базы данных. "
            "Пример: postgresql+psycopg2://user:pass@host:5432/db"
        ),
    )

    secret_key: str = Field(
        default="change_me_for_production_super_secret_key",
        description="Секрет для подписи JWT.",
    )
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=60)

    log_level: str = Field(default="INFO")
    log_file: str = Field(
        default="logs/blogicum.log",
        description="Путь к файлу логов действий пользователя.",
    )


@lru_cache
def get_settings() -> Settings:
    """Кэшированный доступ к объекту настроек."""
    return Settings()


settings = get_settings()
