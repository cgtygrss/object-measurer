import os
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "Object Measurer API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    DATABASE_URL: str = "sqlite+aiosqlite:///./measurer.db"
    SECRET_KEY: str = "change-me-in-production"

    UPLOAD_DIR: str = "./uploads"
    RESULTS_DIR: str = "./results"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB

    CORS_ORIGINS: List[str] = [
        "http://localhost:8081",
        "http://localhost:19006",
        "http://localhost:3000",
    ]

    # Grid interval for measurement
    DEFAULT_INTERVAL: int = 20
    MIN_CONTOUR_DISTANCE: int = 25

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

# Ensure directories exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.RESULTS_DIR, exist_ok=True)
