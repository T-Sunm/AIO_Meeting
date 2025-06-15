from pydantic_settings import BaseSettings
from pydantic import SecretStr
from typing import Any
import os
from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))

# Connect the path with your '.env' file name
load_dotenv(os.path.join(BASEDIR, "../.env"))


class Settings(BaseSettings):
    """Settings for the application."""

    ROOT_PATH: str = ""
    API_V1_STR: str = "/v1"
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # OpenAI API key
    OPENAI_API_KEY: SecretStr
    OPENAI_TEMPERATURE: float = 0.7
    
    # Milvus configuration
    MILVUS_HOST: str = "localhost"
    MILVUS_PORT: str = "19530"
    MILVUS_COLLECTION: str = "langchain_docs"


SETTINGS = Settings()  # type: ignore

APP_CONFIGS: dict[str, Any] = {
    "title": "Lesson 3 - RAG - API Layer",
    "root_path": SETTINGS.ROOT_PATH,
}
