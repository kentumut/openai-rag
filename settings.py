# settings.py
from pydantic_settings import BaseSettings
from fastapi.middleware.cors import CORSMiddleware

class Settings(BaseSettings):
    cors: dict = {
        "allow_origins": [
            "https://kentumut.com",
            "https://www.kentumut.com",
        ],
        "allow_credentials": True,
        "allow_methods": ["*"],
        "allow_headers": ["*"],
    }
    rate_limit: str = "5/hour"
    qdrant_path: str = "./qdrant_data"

settings = Settings()
