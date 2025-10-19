"""Application configuration module.

Centralizes environment-driven settings for models and external services.
"""

import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    """Simple container for environment-backed settings."""

    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY")
    PINECONE_ENVIRONMENT: str = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")

    # Database and Storage
    UPLOAD_DIRECTORY: str = os.getenv("UPLOAD_DIRECTORY", "uploads/")
    DATASET_DIRECTORY: str = os.getenv("DATASET_DIRECTORY", "datasets/")

    # Model Configuration
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    GENAI_MODEL: str = os.getenv("GENAI_MODEL", "gpt2")

    # Pinecone Configuration
    PINECONE_INDEX_NAME: str = os.getenv("PINECONE_INDEX_NAME", "furniture-products")
    EMBEDDING_DIMENSION: int = int(os.getenv("EMBEDDING_DIMENSION", "384"))

    # Recommendation Settings
    DEFAULT_TOP_K: int = int(os.getenv("DEFAULT_TOP_K", "5"))
    SIMILARITY_THRESHOLD: float = float(os.getenv("SIMILARITY_THRESHOLD", "0.3"))


settings = Settings()

