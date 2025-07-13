# Quick test script
import requests


def test_weaviate():
    try:
        # Test ready endpoint
        response = requests.get(
            "http://localhost:8080/v1/.well-known/ready", timeout=10
        )
        print(f"Ready endpoint - Status: {response.status_code}")
        print(f"Response: {response.text}")

        # Test main API
        response2 = requests.get("http://localhost:8080/v1", timeout=10)
        print(f"Main API - Status: {response2.status_code}")
        print(f"Response: {response2.text[:200]}...")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    test_weaviate()
