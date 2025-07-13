# import os
from pathlib import Path
from typing import Dict, Any

# from utils.logger.logging import logger as logger


class Config:
    """
    Configuraton settings for the application.
    """

    # Project Paths
    PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent
    DATA_DIR = PROJECT_ROOT / "data"
    BOOK_DATA_FILE = DATA_DIR / "book_descriptions.json"

    # Weaviate Settings
    WEAVIATE_URL: str = "http://localhost:8080"
    COLLECTION_NAME: str = "Books"

    # Embedding Model Settings
    EMBEDDING_MODEL_NAME = (
        "BAAI/bge-small-en-v1.5"  # 384-dimensional dense vector space
    )

    # Search Settings
    DEFAULT_SEARCH_LIMIT = 10

    # Environment Variable
    # WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY", None)
    # if not WEAVIATE_API_KEY:
    #     logger.error("WEAVIATE_API_KEY environment variable is not set.")
    #     raise ValueError("WEAVIATE_API_KEY environment variable is not set.")

    @classmethod
    def get_weaviate_config(cls) -> Dict[str, Any]:
        """
        Get Weaviate connection configuration.
        """
        config = {
            "url": cls.WEAVIATE_URL,
        }

        if cls.WEAVIATE_API_KEY:
            config["auth_client_secret"] = cls.WEAVIATE_API_KEY

        return config

    @classmethod
    def validate_paths(cls) -> bool:
        """Validate that required paths exist."""
        if not cls.DATA_DIR.exists():
            print(f"Creating data directory: {cls.DATA_DIR}")
            cls.DATA_DIR.mkdir(parents=True, exist_ok=True)

        return cls.DATA_DIR.exists()

    @classmethod
    def print_config(cls):
        """Print current configuration."""
        print("=" * 50)
        print("WEAVIATE RAG PROJECT CONFIGURATION")
        print("=" * 50)
        print(f"Project Root: {cls.PROJECT_ROOT}")
        print(f"Data Directory: {cls.DATA_DIR}")
        print(f"Book Data File: {cls.BOOK_DATA_FILE}")
        print(f"Weaviate URL: {cls.WEAVIATE_URL}")
        print(f"Collection Name: {cls.COLLECTION_NAME}")
        print(f"Embedding Model: {cls.EMBEDDING_MODEL_NAME}")
        print(f"Default Search Limit: {cls.DEFAULT_SEARCH_LIMIT}")
        print("=" * 50)


# Create a default config instance
config = Config()

if __name__ == "__main__":
    # Test configuration
    config.print_config()
    config.validate_paths()
    print("Configuration loaded successfully!")
