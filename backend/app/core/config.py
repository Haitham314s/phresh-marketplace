from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    project_name: str = "Phresh Marketplace"
    project_version: str = "1.0.0"

    secret_key: str

    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: str
    postgres_db: str
    test: str = "false"

    model_config = SettingsConfigDict(env_file=".env.test")


config = Settings()


DB_NAME = f"{config.postgres_db}_test" if config.test == "true" else config.postgres_db
DATABASE_URL = f"postgres://{config.postgres_user}:{config.postgres_password}@{config.postgres_host}:{config.postgres_port}/{DB_NAME}"
print(f"DATABASE_URL: {DATABASE_URL}")
