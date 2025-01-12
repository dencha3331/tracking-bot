from pathlib import Path

from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

BASE_DIR = Path(__file__).parent.parent


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class TelegramConfig(BaseModel):
    token: str


class RedisConfig(BaseModel):
    host: str
    port: int


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=("../.env.template", "../.env", ".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="BOT_CONFIG__",
        extra="ignore",
    )
    db: DatabaseConfig
    telegram: TelegramConfig
    redis: RedisConfig


settings = Settings()
