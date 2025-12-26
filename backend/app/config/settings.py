from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # Cohere API configuration
    cohere_api_key: str

    # Qdrant configuration
    qdrant_url: str
    qdrant_api_key: Optional[str] = None

    # Neon Postgres configuration
    neon_db_url: Optional[str] = None

    # Application settings
    app_name: str = Field(default="Physical AI RAG Backend")
    app_version: str = Field(default="1.0.0")
    debug: bool = Field(default=False)

    # CORS settings
    frontend_origin: str = Field(default="http://localhost:3000")

    # Performance settings
    max_tokens: int = Field(default=200)
    timeout_seconds: int = Field(default=30)
    max_question_length: int = Field(default=1000)
    min_selection_length: int = Field(default=10)
    max_selection_length: int = Field(default=5000)

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


# Create a single instance of settings
settings = Settings()