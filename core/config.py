import os
from dotenv import load_dotenv
from pathlib import Path

import cloudinary

env_path = Path('.') / '.env'

load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_NAME: str = "Job Board"
    PROJECT_VERSION: str = "1.0.0"

    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", 5432)
    POSTGRES_DATABASE: str = os.getenv("POSTGRES_DATABASE")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{5432}/{POSTGRES_DATABASE}"
    cloudinary.config(
        cloud_name=os.getenv("CLOUD_NAME"),
        api_key=os.getenv("API_KEY"),
        api_secret=os.getenv("API_SECRET"),

    )


settings = Settings()

