from pydantic_settings import BaseSettings, SettingsConfigDict

from app.common.enums import Environment


class Settings(BaseSettings):
    app_name: str = "Student Study Assistant"
    debug: bool = True
    environment: Environment = Environment.DEVELOPMENT

    api_v1_prefix: str = "/api/v1"
    log_level: str = "INFO"

    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="SSA_",
        extra="ignore",
    )

    database_host: str = "localhost"
    database_port: int = 5432
    database_name: str = "student_study_assistant"
    test_database_name: str = "student_study_assistant_test"
    database_user: str = "ssa_user"
    database_password: str = ""

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg_async://"
            f"{self.database_user}:"
            f"{self.database_password}@"
            f"{self.database_host}:"
            f"{self.database_port}/"
            f"{self.database_name}"
        )

    @property
    def test_database_url(self) -> str:
        return (
            f"postgresql+psycopg_async://"
            f"{self.database_user}:"
            f"{self.database_password}@"
            f"{self.database_host}:"
            f"{self.database_port}/"
            f"{self.test_database_name}"
        )


settings = Settings()  # type: ignore[call-arg]
