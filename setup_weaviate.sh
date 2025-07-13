#!/bin/bash

echo "Starting local Weaviate instance..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker and try again."
    exit 1
fi

# Start Weaviate with Docker Compose
echo "Starting Weaviate container..."
docker-compose up -d

# Wait for Weaviate to be ready
echo "Waiting for Weaviate to be ready..."
timeout=60
counter=0

while [ $counter -lt $timeout ]; do
    if curl -s http://localhost:8080/v1/.well-known/ready > /dev/null 2>&1; then
        echo "✓ Weaviate is ready!"
        break
    fi
    echo "Waiting... ($counter/$timeout)"
    sleep 2
    counter=$((counter + 2))
done

if [ $counter -ge $timeout ]; then
    echo "✗ Timeout waiting for Weaviate to start"
    exit 1
fi

echo "Weaviate is running at: http://localhost:8080"
echo "You can check the status at: http://localhost:8080/v1/.well-known/ready"