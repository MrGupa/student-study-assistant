from pydantic_settings import BaseSettings, SettingsConfigDict

from app.common.enums import Environment


class Settings(BaseSettings):
    app_name: str = "Student Study Assistant"
    debug: bool = True
    environment: Environment = Environment.DEVELOPMENT

    api_v1_prefix: str = "/api/v1"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="SSA_",
    )


settings = Settings()
