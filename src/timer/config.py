from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from os import getenv

load_dotenv()

class Settings(BaseSettings):
    GOOGLE_TOKEN_ID: str = "sgffigasd265167217898975"
    DATABASE_URL: str = getenv("DATABASE_URL")

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()