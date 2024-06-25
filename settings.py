from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


@lru_cache
def get_settings():
    return Settings()


class Settings(BaseSettings):
    host: str = 'localhost'
    port: int = 8080
    debug: bool = False

    # Database configs
    db_host: str = 'localhost'
    db_port: int = 5432
    db_user: str = 'postgres'
    db_pass: str
    db_name: str = 'postgres'

    # Authentication configs
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(env_file=".env")
