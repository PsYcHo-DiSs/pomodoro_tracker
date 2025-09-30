from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GOOGLE_TOKEN_ID: str = "sgffigasd265167217898975"

    class Config:
        env_file = ".env"

