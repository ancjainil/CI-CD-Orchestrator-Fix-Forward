from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="SLO_", case_sensitive=False)

    env: str = "local"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    log_level: str = "INFO"

    github_app_id: str = "local-app"
    github_app_private_key: str = "changeme"
    github_webhook_secret: str = "dev-secret"
    github_installation_id: int | None = None
    github_oauth_client_id: str | None = None
    github_oauth_client_secret: str | None = None

    jwt_secret: str = "dev-jwt-secret"
    jwt_algorithm: str = "HS256"

    database_url: str = "postgresql+psycopg_async://postgres:postgres@postgres:5432/slo"
    redis_url: str = "redis://redis:6379/0"

    prom_base_url: str = "http://prometheus:9090"
    prom_mock: bool = True

    otlp_endpoint: str | None = None


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
