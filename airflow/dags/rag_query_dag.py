from airflow.decorators import dag, task
from datetime import datetime
import sys

sys.path.append("/opt/airflow/include")


@dag(
    start_date=datetime(2025, 7, 14),
    schedule=None,  # Manual trigger
    catchup=False,
    description="RAG Query Pipeline - Search Books",
    tags=["rag", "query", "search"],
)
def rag_query_dag():

    @task
    def process_user_query(query: str = "science fiction adventure"):
        """Process user query and generate embedding"""
        from fastembed import TextEmbedding

        print(f"🔍 Processing query: '{query}'")

        # Generate query embedding
        embedding_model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
        query_embedding = list(embedding_model.embed([query]))[0].tolist()

        print(f"✓ Generated query embedding (dimension: {len(query_embedding)})")

        return {
            "query": query,
            "embedding": query_embedding,
            "timestamp": datetime.now().isoformat(),
        }

    @task
    def search_similar_books(query_data, limit: int = 5):
        """Search for similar books using vector similarity"""
        import weaviate

        client = weaviate.Client("http://weaviate:8080")

        print(f"🔍 Searching for books similar to: '{query_data['query']}'")

        # Perform vector search
        response = (
            client.query.get(
                "Books", ["title", "author", "year", "description", "book_id"]
            )
            .with_near_vector({"vector": query_data["embedding"]})
            .with_limit(limit)
            .with_additional(["distance"])
            .do()
        )

        books = response["data"]["Get"]["Books"]

        print(f"✓ Found {len(books)} similar books:")
        for i, book in enumerate(books, 1):
            distance = book["_additional"]["distance"]
            print(
                f"  {i}. {book['title']} by {book['author']} (similarity: {1-distance:.3f})"
            )

        return {
            "query": query_data["query"],
            "results": books,
            "result_count": len(books),
        }

    @task
    def generate_recommendations(search_results):
        """Generate formatted recommendations"""
        recommendations = []

        print(f"📚 Generating recommendations for: '{search_results['query']}'")

        for i, book in enumerate(search_results["results"], 1):
            similarity_score = 1 - book["_additional"]["distance"]

            recommendation = {
                "rank": i,
                "title": book["title"],
                "author": book["author"],
                "year": book["year"],
                "description": (
                    book["description"][:200] + "..."
                    if len(book["description"]) > 200
                    else book["description"]
                ),
                "similarity_score": round(similarity_score, 3),
                "book_id": book["book_id"],
            }
            recommendations.append(recommendation)

        # Generate summary
        summary = {
            "query": search_results["query"],
            "total_recommendations": len(recommendations),
            "best_match": recommendations[0] if recommendations else None,
            "recommendations": recommendations,
        }

        print(f"✓ Generated {len(recommendations)} recommendations")
        print(
            f"📖 Best match: '{recommendations[0]['title']}' by {recommendations[0]['author']}"
        )

        return summary

    @task
    def format_response(recommendation_summary):
        """Format final response for user"""
        query = recommendation_summary["query"]
        recs = recommendation_summary["recommendations"]

        response = f"""
🔍 **Search Query**: "{query}"
📚 **Found {len(recs)} relevant books:**

"""

        for rec in recs:
            response += f"""
**{rec['rank']}. {rec['title']}** ({rec['year']})
   📝 Author: {rec['author']}
   ⭐ Similarity: {rec['similarity_score']}
   📖 Description: {rec['description']}

"""

        print("=" * 50)
        print("🎯 FINAL RAG RESPONSE:")
        print("=" * 50)
        print(response)
        print("=" * 50)

        return {
            "formatted_response": response,
            "metadata": {
                "query": query,
                "result_count": len(recs),
                "processing_timestamp": datetime.now().isoformat(),
            },
        }

    # Define the RAG query workflow
    query_data = process_user_query()
    search_results = search_similar_books(query_data)
    recommendations = generate_recommendations(search_results)
    final_response = format_response(recommendations)

    return final_response


rag_query_dag()
