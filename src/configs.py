from typing import List, Literal
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DEBUG: bool = True
    APP_ENV: Literal["development", "production"] = "development"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    GCP_SERVICE_ACCOUNT_FILENAME: str = "skilled-curve-416214-597aa10b7cc4.json"
    GEMINI_PROJECT_NAME: str = "skilled-curve-416214"
    GEMINI_REGIONS: List[str] = ["us-central1", "us-east4", "us-west1", "us-west4"]

config: Config = Config()
