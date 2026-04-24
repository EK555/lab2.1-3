from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_NAME: str = "spa_db"
    DB_HOST: str = "127.0.0.1"
    DB_PORT: str = "5432"
    PORT: int = 8000
    APP_NAME: str = "SPA Salon API"
    ENVIRONMENT: str = "development"

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"
        case_sensitive = True

    # Настройки для JWT
    JWT_ACCESS_SECRET: str
    JWT_REFRESH_SECRET: str
    JWT_ACCESS_EXPIRES_MINUTES: int = 15
    JWT_REFRESH_EXPIRES_DAYS: int = 7
    
    # Настройки для OAuth
    YANDEX_CLIENT_ID: Optional[str] = None
    YANDEX_CLIENT_SECRET: Optional[str] = None
    YANDEX_CALLBACK_URL: Optional[str] = None
    O_AUTH_STATE_SECRET: Optional[str] = None
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()