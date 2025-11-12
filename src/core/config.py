from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    DB_NAME: str = os.getenv("DB_NAME", "cinecheck")
    CORS_ORIGINS: List[str] = os.getenv("CORS_ORIGINS", "http://localhost:4200").split(",")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "your-secret-key")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

    class Config:
        env_file = ".env"

settings = Settings()