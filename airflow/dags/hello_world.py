from airflow.decorators import dag, task
from datetime import datetime


@dag(
    start_date=datetime(2025, 7, 14),
    schedule="@daily",
    catchup=False,
    description="A simple Hello World DAG",
)
def hello_world_dag():

    @task
    def print_hello():
        """Simple function to print hello"""
        print("Hello from Airflow!")
        print("RAG Orchestration is working!")
        return "success"

    @task
    def check_weaviate():
        """Check if Weaviate is accessible"""
        import requests

        try:
            response = requests.get("http://weaviate:8080/v1/.well-known/ready")
            print(f"Weaviate status: {response.status_code}")
            print(f"Weaviate ready: {response.json()}")
            return "Weaviate is accessible!"
        except Exception as e:
            print(f"Error connecting to Weaviate: {e}")
            return "Weaviate connection failed"

    # Set task dependencies
    hello_result = print_hello()
    weaviate_result = check_weaviate()

    hello_result >> weaviate_result


hello_world_dag()
