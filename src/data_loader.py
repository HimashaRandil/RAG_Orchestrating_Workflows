import json
from typing import List, Dict, Any
from pathlib import Path
from config.settings import Config
from src.embedding_service import EmbeddingService
from src.vector_store import WeaviateVectorStore
from utils.logger.logging import logger as logger


class DataLoader:
    """
    Loads book data, generates embeddings, and stores them in Weaviate.
    """

    def __init__(self):
        """Initialize the data loader with required services."""
        self.config = Config()
        self.embedding_service = EmbeddingService()
        self.vector_store = WeaviateVectorStore()

    def load_book_data(self, file_path: Path = None) -> List[Dict[str, Any]]:
        """
        Load book data from JSON file.

        Args:
            file_path (Path, optional): Path to book data file. Defaults to config path.

        Returns:
            List[Dict[str, Any]]: List of book dictionaries
        """
        if file_path is None:
            file_path = self.config.BOOK_DATA_FILE

        try:
            logger.info(f"Loading book data from {file_path}")

            if not file_path.exists():
                logger.error(f"Book data file not found: {file_path}")
                raise FileNotFoundError(f"Book data file not found: {file_path}")
                return []

            with open(file_path, "r", encoding="utf-8") as f:
                books_data = json.load(f)

            logger.info(f"Loaded {len(books_data)} books from {file_path}")
            return books_data

        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON from {file_path}: {e}")
            raise e
            return []
        except Exception as e:
            logger.error(f"Unexpected error loading book data: {e}")
            raise e
            return []

    def validate_book_data(self, books_data: List[Dict[str, Any]]) -> bool:
        """
        Validate that book data has required fields.

        Args:
            books_data (List[Dict[str, Any]]): List of book dictionaries

        Returns:
            bool: True if data is valid, False otherwise
        """
        required_fields = ["id", "title", "author", "year", "description"]

        for i, book in enumerate(books_data):
            for field in required_fields:
                if field not in book:
                    logger.error(f"Book {i} missing required field: {field}")
                    return False

                if not book[field]:  # Check for empty values
                    logger.error(f"Book {i} has empty value for field: {field}")
                    return False

        logger.info("✓ Book data validation passed")
        return True

    def process_and_store_books(self, books_data: List[Dict[str, Any]]) -> bool:
        """
        Generate embeddings for books and store them in Weaviate.

        Args:
            books_data (List[Dict[str, Any]]): List of book dictionaries

        Returns:
            bool: True if successful, False otherwise
        """

        try:
            # Validate data first
            if not self.validate_book_data(books_data):
                logger.error("Book data validation failed")
                return False

            # Generate embeddings for book descriptions
            logger.info("Generating embeddings for book descriptions...")
            embeddings = self.embedding_service.embed_book_description(books_data)

            if not embeddings:
                logger.error("Failed to generate embeddings")
                return False

            if len(embeddings) != len(books_data):
                logger.error(
                    f"Mismatch: {len(books_data)} books but {len(embeddings)} embeddings"
                )
                return False

            # Create collection in Weaviate
            logger.info("Creating Weaviate collection...")
            if not self.vector_store.create_collection():
                logger.error("Failed to create Weaviate collection")
                return False

            # Store books and embeddings in Weaviate
            logger.info("Storing books in Weaviate...")
            if not self.vector_store.insert_books(books_data, embeddings):
                logger.error("Failed to store books in Weaviate")
                return False

            logger.info("✓ Successfully processed and stored all books!")
            return True

        except Exception as e:
            logger.error(f"Error processing and storing books: {e}")
            return False

    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the stored collection."""
        try:
            stats = self.vector_store.get_collection_info()
            logger.info(f"Collection stats: {stats}")
            return stats
        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            return {"status": "error", "error": str(e)}

    def load_and_process_all(self) -> bool:
        """
        Complete workflow: load data, generate embeddings, store in Weaviate.

        Returns:
            bool: True if entire process successful
        """
        logger.info("Starting complete data loading workflow...")

        try:
            # Step 1: Load book data
            books_data = self.load_book_data()
            if not books_data:
                logger.error("No book data loaded")
                return False

            # Step 2: Process and store
            if not self.process_and_store_books(books_data):
                logger.error("Failed to process and store books")
                return False

            # Step 3: Get final stats
            stats = self.get_collection_stats()
            logger.info(f"Final collection stats: {stats}")

            logger.info("Complete data loading workflow finished successfully!")
            return True

        except Exception as e:
            logger.error(f"Error in complete workflow: {e}")
            return False
        finally:
            # Clean up connections
            self.vector_store.close()

    def reset_collection(self) -> bool:
        """Delete and recreate the collection (useful for testing)."""
        try:
            logger.warning("Resetting collection - all data will be lost!")

            # Delete existing collection
            self.vector_store.delete_collection()

            # Recreate collection
            success = self.vector_store.create_collection()

            if success:
                logger.info("Collection reset successfully")
            else:
                logger.error("Failed to reset collection")

            return success

        except Exception as e:
            logger.error(f"Error resetting collection: {e}")
            return False


def main():
    """Main function to run the data loading process."""
    logger.info("=" * 60)
    logger.info("STARTING RAG DATA LOADING PROCESS")
    logger.info("=" * 60)

    # Initialize data loader
    data_loader = DataLoader()

    # Check if we need to reset (optional)
    reset = input("Do you want to reset the collection first? (y/N): ").lower().strip()
    if reset == "y":
        data_loader.reset_collection()

    # Run the complete workflow
    success = data_loader.load_and_process_all()

    if success:
        logger.success("Data loading process completed successfully!")
    else:
        logger.error("Data loading process failed!")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
