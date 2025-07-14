import weaviate
from typing import List, Dict, Any
from weaviate.classes.data import DataObject
from weaviate.classes.config import Configure, Property, DataType
from config.settings import config
from utils.logger.logging import logger as logger


class WeaviateVectorStore:
    """
    Handles all Weaviate vector database operations.
    """

    def __init__(self):
        """
        Initialize connection to Weaviate.
        """
        self.client = None
        self.collection = None
        self.connect()

    def connect(self):
        """
        Connects to Weaviate Instance.
        """
        try:
            logger.info("Connecting to Weaviate at localhost:8080...")

            # Use a more reliable connection method
            self.client = weaviate.connect_to_local(
                host="localhost",
                port=8080,
                grpc_port=50051,
                skip_init_checks=True,  # Skip problematic health checks
                additional_config=weaviate.classes.init.AdditionalConfig(
                    timeout=weaviate.classes.init.Timeout(
                        init=60, query=60, insert=120  # Longer timeout for init
                    )
                ),
            )

            # Simple ready check
            if self.client.is_ready():
                logger.info("✓ Connected to Weaviate successfully")
                return True
            else:
                logger.error("✗ Weaviate client not ready")
                self.client = None
                return False

        except Exception as e:
            logger.error(f"✗ Error connecting to Weaviate: {e}")

            # Try fallback connection method
            try:
                logger.info("Trying alternative connection method...")
                self.client = weaviate.Client("http://localhost:8080")

                # Test with a simple operation
                self.client.schema.get()
                logger.info("✓ Connected to Weaviate with fallback method")
                return True

            except Exception as e2:
                logger.error(f"✗ Fallback connection also failed: {e2}")
                self.client = None
                return False

    def create_collection(self):
        """
        Creates the book collection with proper Schema
        """

        try:
            existing_collections = self.client.collections.list_all()

            if config.COLLECTION_NAME in existing_collections:  # If exists
                logger.info(f"Collection '{config.COLLECTION_NAME}' already exists")
                self.collection = self.client.collections.get(config.COLLECTION_NAME)
                return True

            logger.info(f"Creating collection: {config.COLLECTION_NAME}")

            self.collection = self.client.collections.create(
                name=config.COLLECTION_NAME,
                properties=[
                    Property(name="title", data_type=DataType.TEXT),
                    Property(name="author", data_type=DataType.TEXT),
                    Property(name="year", data_type=DataType.INT),
                    Property(name="description", data_type=DataType.TEXT),
                    Property(name="book_id", data_type=DataType.INT),
                ],
                # Configure vector settings
                vectorizer_config=Configure.Vectorizer.none(),
            )
            logger.info(f"Collection {config.COLLECTION_NAME} created successfully.")
            return True

        except Exception as e:
            logger.error(f"Error creating collection: {e}")
            return False

    def get_collection_info(self) -> Dict[str, Any]:
        """
        Get information about the collection.
        """
        try:
            if not self.collection:
                self.collection = self.client.collections.get(config.COLLECTION_NAME)

            total_objects = self.collection.aggregate.over_all(total_count=True)

            return {
                "name": config.COLLECTION_NAME,
                "total_objects": total_objects.total_count,
                "status": "ready",
            }

        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            return {
                "name": config.COLLECTION_NAME,
                "total_objects": 0,
                "status": "error",
            }

    def insert_books(
        self, books_data: List[Dict], embeddings: List[List[float]]
    ) -> bool:
        """
        Inserts books data into the collection with their embeddings.
        """
        try:
            if not self.collection:
                self.collection = self.client.collections.get(config.COLLECTION_NAME)
                logger.info(f"Connected to collection: {config.COLLECTION_NAME}")

            logger.info(
                f"Inserting {len(books_data)} books into collection: {config.COLLECTION_NAME}"
            )

            objects_to_insert = []

            for book, embedding in zip(books_data, embeddings):
                data_object = DataObject(
                    properties={
                        "title": book["title"],
                        "author": book["author"],
                        "year": book["year"],
                        "description": book["description"],
                        "book_id": book["id"],
                    },
                    vector=embedding,
                )
                objects_to_insert.append(data_object)

            # Batch insert
            response = self.collection.data.insert_many(objects_to_insert)

            # Check if the insert was successful
            if response.has_errors:
                logger.error(f"Error inserting books: {response.errors}")
                for error in response.errors:
                    logger.error(f"Error: {error.message}")
                return False

            logger.info(f"Inserted {len(objects_to_insert)} books successfully.")
            return True

        except Exception as e:
            logger.error(f"Error inserting books: {e}")
            return False

    def search_books(self, query_vector: List[float], limit: int = 5) -> List[Dict]:
        """Search for books using vector similarity."""
        try:
            if not self.collection:
                self.collection = self.client.collections.get(config.COLLECTION_NAME)
                logger.info(f"Connected to collection: {config.COLLECTION_NAME}")

            logger.info(
                f"Searching for books similar to the query vector with limit {limit}"
            )

            response = self.collection.query.near_vector(
                vector=query_vector, limit=limit, return_metadata=["distance"]
            )

            # Format the results
            results = []
            for obj in response.objects:
                result = {
                    "title": obj.properties.get("title"),
                    "author": obj.properties.get("author"),
                    "year": obj.properties.get("year"),
                    "description": obj.properties.get("description"),
                    "book_id": obj.properties.get("book_id"),
                    "similarity_score": 1 - obj.metadata.distance,
                }
                results.append(result)

            return results

        except Exception as e:
            logger.error(f"Error searching for books: {e}")
            return []

    def delete_collection(self) -> bool:
        """
        Deletes the collection.
        """
        try:

            logger.info(f"Deleting collection: {config.COLLECTION_NAME}")
            self.client.collections.delete(config.COLLECTION_NAME)
            logger.info(f"Collection {config.COLLECTION_NAME} deleted successfully.")
            return True

        except Exception as e:
            logger.error(f"Error deleting collection: {e}")
            return False

    def close(self):
        """
        Closes the connection to Weaviate.
        """
        if self.client:
            self.client.close()
            logger.info("Weaviate connection closed.")
        else:
            logger.warning("No active Weaviate connection to close.")


# Test the vector store
if __name__ == "__main__":
    vector_store = WeaviateVectorStore()

    if vector_store.client and vector_store.client.is_ready():
        logger.info("Testing collection creation...")
        vector_store.create_collection()

        # Get collection info
        info = vector_store.get_collection_info()
        logger.info(f"Collection info: {info}")

        vector_store.close()
    else:
        logger.info("Cannot test - Weaviate connection failed")
