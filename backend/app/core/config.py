from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Career Copilot"
    # nvidia_nim_api_key: str
    database_url: str
    secret_key: str
    algorithm: str
    groq_api_key: str
    access_token_expire_minutes: int
    langsmith_tracing: bool = False
    langsmith_api_key: str | None
    langsmith_project: str = "ai-career-copilot"
    langsmith_endpoint: str = "https://api.smith.langsmith.com"
    model_config = SettingsConfigDict(
        env_file=".env"
    )


settings = Settings()