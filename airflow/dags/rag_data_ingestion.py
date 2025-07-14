from airflow.decorators import dag, task
from datetime import datetime
import sys

# Add src to path to import your existing modules
sys.path.append("/opt/airflow/include")


@dag(
    start_date=datetime(2025, 7, 14),
    schedule=None,  # Manual trigger
    catchup=False,
    description="RAG Data Ingestion Pipeline - Using Existing Components",
    tags=["rag", "weaviate", "embeddings"],
)
def rag_data_ingestion_dag():

    @task
    def load_book_data():
        """Load book descriptions from JSON file"""
        import json

        file_path = "/opt/airflow/include/data/book_descriptions.json"

        with open(file_path, "r", encoding="utf-8") as f:
            books = json.load(f)

        print(f"✓ Loaded {len(books)} books from {file_path}")
        return books

    @task
    def validate_book_data(books_data):
        """Validate book data has required fields"""
        required_fields = ["id", "title", "author", "year", "description"]

        for i, book in enumerate(books_data):
            for field in required_fields:
                if field not in book or not book[field]:
                    raise ValueError(f"Book {i} missing/empty field: {field}")

        print(f"✓ Validation passed for {len(books_data)} books")
        return books_data

    @task
    def generate_embeddings(books_data):
        """Generate embeddings using your existing EmbeddingService"""
        from fastembed import TextEmbedding

        # Initialize the embedding model (same as your EmbeddingService)
        print("Loading embedding model: BAAI/bge-small-en-v1.5")
        embedding_model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")

        # Extract descriptions
        descriptions = [book.get("description", "") for book in books_data]

        print(f"Generating embeddings for {len(descriptions)} descriptions...")
        embeddings = list(embedding_model.embed(descriptions))

        # Convert to lists
        embedding_lists = [emb.tolist() for emb in embeddings]

        print(f"✓ Generated {len(embedding_lists)} embeddings")
        return embedding_lists

    @task
    def setup_weaviate_collection():
        """Create Weaviate collection with proper schema"""
        import weaviate

        # Connect to Weaviate
        client = weaviate.Client("http://weaviate:8080")

        collection_name = "Books"

        # Check if collection exists
        try:
            existing_schema = client.schema.get()
            existing_classes = [cls["class"] for cls in existing_schema["classes"]]

            if collection_name in existing_classes:
                print(f"✓ Collection '{collection_name}' already exists")
                return collection_name
        except weaviate.exceptions.UnexpectedStatusCodeException:
            pass

        # Create collection schema
        schema = {
            "class": collection_name,
            "properties": [
                {"name": "title", "dataType": ["text"]},
                {"name": "author", "dataType": ["text"]},
                {"name": "year", "dataType": ["int"]},
                {"name": "description", "dataType": ["text"]},
                {"name": "book_id", "dataType": ["int"]},
            ],
            "vectorizer": "none",
        }

        client.schema.create_class(schema)
        print(f"✓ Created collection '{collection_name}'")
        return collection_name

    @task
    def store_in_weaviate(books_data, embeddings, collection_name):
        """Store books and embeddings in Weaviate"""
        import weaviate

        client = weaviate.Client("http://weaviate:8080")

        print(
            f"Storing {len(books_data)} books in Weaviate collection '{collection_name}'"
        )

        stored_count = 0
        failed_count = 0

        # Store each book with its embedding
        for book, embedding in zip(books_data, embeddings):
            try:
                client.data_object.create(
                    data_object={
                        "title": book["title"],
                        "author": book["author"],
                        "year": book["year"],
                        "description": book["description"],
                        "book_id": book["id"],
                    },
                    class_name=collection_name,
                    vector=embedding,
                )
                stored_count += 1

                if stored_count % 10 == 0:
                    print(f"Stored {stored_count}/{len(books_data)} books...")

            except Exception as e:
                print(f"Failed to store book '{book['title']}': {e}")
                failed_count += 1

        result = {
            "stored": stored_count,
            "failed": failed_count,
            "total": len(books_data),
        }

        print(f"✓ Storage complete: {stored_count} stored, {failed_count} failed")
        return result

    @task
    def verify_storage(storage_result):
        """Verify data was stored correctly"""
        import weaviate

        client = weaviate.Client("http://weaviate:8080")

        try:
            # Get count of objects in collection
            result = client.query.aggregate("Books").with_meta_count().do()
            count = result["data"]["Aggregate"]["Books"][0]["meta"]["count"]

            print(f"✓ Verification: {count} objects in Weaviate")
            print(f"Expected: {storage_result['stored']}")

            # Test a simple query
            test_query = (
                client.query.get("Books", ["title", "author"]).with_limit(3).do()
            )
            sample_books = test_query["data"]["Get"]["Books"]

            print("Sample stored books:")
            for book in sample_books:
                print(f"  - {book['title']} by {book['author']}")
            return {"verification_count": count, "sample_books": sample_books}

        except Exception as e:
            print(f"Verification failed: {e}")
            return {"error": str(e)}

    # Define the DAG workflow
    books = load_book_data()
    validated_books = validate_book_data(books)
    embeddings = generate_embeddings(validated_books)
    collection_name = setup_weaviate_collection()
    storage_result = store_in_weaviate(validated_books, embeddings, collection_name)
    verification = verify_storage(storage_result)

    # Set dependencies (automatic with task flow)
    return verification


rag_data_ingestion_dag()
