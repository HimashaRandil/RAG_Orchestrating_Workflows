from typing import List
import numpy as np
from fastembed import TextEmbedding
from config.settings import Config
from utils.logger.logging import logger as logger


class EmbeddingService:
    """
    Handles text-to-vector embedding operations using FastEmbed.
    """

    def __init__(self):
        """
        Initialize the embedding model.
        """
        self.model = None
        self.model_name = Config.EMBEDDING_MODEL_NAME
        self.load_model()

    def load_model(self):
        """
        Load the embedding model.
        """
        try:
            logger.info(f"Loading embedding model: {self.model_name}")
            self.model = TextEmbedding(model_name=self.model_name)
            logger.info("Embedding model loaded successfully.")
            return True

        except Exception as e:
            logger.error(
                f"Failed to load embedding model: {self.model_name}. Error: {str(e)}"
            )
            return False

    def embed_single_text(self, text: str) -> List[float]:
        """
        Convert a single text into an embedding vector.

        Args:
            text (str): Text to embed

        Returns:
            List[float]: Embedding vector
        """

        try:
            if not self.model:
                logger.error("Embedding model is not loaded.")
                raise ValueError("Embedding model is not loaded.")

            embeddings = list(self.model.embed([text]))

            if embeddings:
                return embeddings[0].tolist()
            else:
                logger.warning("No embeddings returned for the provided text.")
                return []

        except Exception as e:
            logger.error(f"Error embedding text: {text}. Error: {str(e)}")
            return []

    def embed_batch_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Convert multiple texts into embedding vectors.

        Args:
            texts (List[str]): List of texts to embed

        Returns:
            List[List[float]]: List of embedding vectors
        """

        try:
            if not self.model:
                logger.error("Embedding model is not loaded")
                raise ValueError("Embedding model is not loaded.")

            logger.info(f"Embedding {len(texts)} texts.")
            embeddings = list(self.model.embed(texts))

            embedding_lists = [emb.tolist() for emb in embeddings]

            logger.info(f"Successfully embedded {len(embedding_lists)} texts.")
            return embedding_lists

        except Exception as e:
            logger.error(f"Error embedding texts: {texts}. Error: {str(e)}")
            return []

    def embed_book_description(self, book_data: List[dict]) -> List[List[float]]:
        """
        Generate embeddings specifically for book descriptions.

        Args:
            books_data (List[dict]): List of book dictionaries

        Returns:
            List[List[float]]: List of embedding vectors
        """
        try:

            descriptions = [book.get("description", "") for book in book_data]

            logger.info(f"Embedding {len(descriptions)} book descriptions.")

            embeddings = self.embed_batch_texts(descriptions)

            return embeddings

        except Exception as e:
            logger.error(
                f"Error embedding book descriptions: {book_data}. Error: {str(e)}"
            )
            return []

    def get_embedding_dimension(self) -> int:
        """Get the dimension of the embedding vectors."""
        try:
            test_embedding = self.embed_single_text("test")
            return len(test_embedding) if test_embedding else 0

        except Exception as e:
            logger.error(f"Error getting embedding dimension: {str(e)}")
            return 0

    def calculate_similarity(
        self, embedding1: List[float], embedding2: List[float]
    ) -> float:
        """
        Calculate cosine similarity between two embeddings.

        Args:
            embedding1, embedding2: Two embedding vectors

        Returns:
            float: Similarity score between 0 and 1
        """
        try:
            # Convert to  numpy arrays
            vec1 = np.array(embedding1)
            vec2 = np.array(embedding2)

            # Calculate cosine similarity
            dot_product = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)

            if norm1 == 0 or norm2 == 0:
                logger.warning(
                    "One of the vectors is zero, returning similarity of 0.0"
                )
                return 0.0

            similarity = dot_product / (norm1 * norm2)
            return float(similarity)

        except Exception as e:
            logger.error(f"Error calculating similarity: {str(e)}")
            return 0.0


if __name__ == "__main__":

    logger.info("Embedding Service Module Loaded")

    embedding_service = EmbeddingService()

    if embedding_service.model:
        logger.info("Embedding service initialized successfully.")
        test_text = "A philosophical book about the meaning of life"
        embedding = embedding_service.embed_single_text(test_text)

        if embedding:
            logger.info(f"Embedding for '{test_text}': {embedding}")
        else:
            logger.error("Failed to generate embedding.")

    # Test batch embedding
    logger.info("Testing batch embedding...")
    test_texts = [
        "A science fiction novel about space travel",
        "A romantic story set in Victorian England",
        "A mystery thriller with unexpected twists",
    ]

    batch_embeddings = embedding_service.embed_batch_texts(test_texts)

    if batch_embeddings:
        for i, text in enumerate(test_texts):
            logger.info(f"Embedding for '{text}': {batch_embeddings[i]}")

    # Test similarity calculation
    logger.info("Testing similarity calculation...")
    if len(batch_embeddings) >= 2:
        similarity = embedding_service.calculate_similarity(
            batch_embeddings[0], batch_embeddings[1]
        )
        logger.info(
            f"Similarity between '{test_texts[0]}' and '{test_texts[1]}': {similarity}"
        )

    logger.info("Embedding Service Module Test Completed")
