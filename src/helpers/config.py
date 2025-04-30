from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    APP_NAME: str = "MiniRAGapp"
    APP_VERSION: str = "1.0.0"
    OPENAI_API_KEY: str = ""
    DEBUG: bool = False
    FILE_ALLOWED_TYPES: list
    FILE_MAX_SIZE: int
    FILE_DEFAULT_CHANUK_SIZE: int
    MONGO_URI: str
    MONGO_DB: str
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parents[2] / ".env")

    # class Config:
    #     env_file = ".env"


def get_settings():
    return Settings()
