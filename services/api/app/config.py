"""Type-safe configuration using Pydantic Settings.

All environment variables are validated at startup.
Missing required vars cause a clear error, not a runtime crash.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings


class DatabaseConfig(BaseSettings):
    database_url: str = "postgresql://rideshala:rideshala@localhost:5432/rideshala"
    redis_url: str = "redis://localhost:6379"
    qdrant_url: str = "http://localhost:6333"
    meili_url: str = "http://localhost:7700"
    meili_master_key: str = ""

    model_config = {"env_prefix": "", "case_sensitive": False}


class LLMConfig(BaseSettings):
    vllm_base_url: str = "http://localhost:8000/v1"
    vllm_api_key: str = "dummy"
    vllm_model: str = "mistralai/Mistral-7B-Instruct-v0.3"
    embedding_base_url: str = "http://localhost:8001/v1"
    embedding_model: str = "nomic-ai/nomic-embed-text-v1.5"

    # Optional paid providers (not loaded if empty)
    anthropic_api_key: str = ""
    claude_model: str = "claude-sonnet-4-20250514"
    groq_api_key: str = ""
    groq_model: str = "llama-3.1-70b-versatile"

    model_config = {"env_prefix": "", "case_sensitive": False}


class AuthConfig(BaseSettings):
    auth_secret_key: str = "dev-secret-change-in-production"
    auth_algorithm: str = "HS256"
    auth_access_token_expire_minutes: int = 1440

    model_config = {"env_prefix": "", "case_sensitive": False}


class AppConfig(BaseSettings):
    app_env: str = "development"
    app_port: int = 8080
    cors_origins: str = "http://localhost:3000"
    log_level: str = "INFO"
    rate_limit_anonymous_chat: int = 10
    rate_limit_auth_chat: int = 30

    model_config = {"env_prefix": "", "case_sensitive": False}


class Settings(BaseSettings):
    """Root settings — combines all config sections."""

    db: DatabaseConfig = DatabaseConfig()
    llm: LLMConfig = LLMConfig()
    auth: AuthConfig = AuthConfig()
    app: AppConfig = AppConfig()


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance. Call once at startup."""
    return Settings()
