from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Secure API"
    APP_ENV: str = "dev"
    APP_PORT: int = 8000
    DEBUG: bool = True

    class Config:
        env_file = ".env"


settings = Settings()