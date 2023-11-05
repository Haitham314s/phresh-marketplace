from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    project_name: str = "Phresh Marketplace"
    project_version: str = "1.0.0"
    api_prefix: str = "/api"

    secret_key: str
    access_token_expire_minutes: int
    jwt_algorithm: str = "HS256"
    jwt_audience: str = "phresh:auth"
    jwt_token_prefix: str = "Bearer"

    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: str
    postgres_db: str

    model_config = SettingsConfigDict(env_file=".env")


config = Settings()

DATABASE_URL = (
    f"postgres://{config.postgres_user}:{config.postgres_password}@{config.postgres_host}:"
    f"{config.postgres_port}/{config.postgres_db}"
)
print(f"DATABASE_URL: {DATABASE_URL}")
