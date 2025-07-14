# RAG Orchestrating Workflows

A comprehensive Retrieval-Augmented Generation (RAG) system built with Apache Airflow for workflow orchestration, Weaviate as the vector database, and FastEmbed for generating embeddings.

## 🎯 Project Overview

This project demonstrates how to build and orchestrate a complete RAG pipeline using modern tools. It processes book descriptions, generates vector embeddings, stores them in a vector database, and provides intelligent search capabilities through Airflow DAGs.

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Book Data     │───▶│   FastEmbed     │───▶│   Weaviate      │
│   (JSON/TXT)    │    │   Embeddings    │    │ Vector Database │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
┌─────────────────┐    ┌─────────────────┐             │
│   User Query    │───▶│  Vector Search  │◀────────────┘
│                 │    │ & Retrieval     │
└─────────────────┘    └─────────────────┘
          All orchestrated by Apache Airflow
```

## 🚀 Features

- **📚 Data Processing**: Automated ingestion of book descriptions from text/JSON files
- **🔢 Vector Embeddings**: Uses FastEmbed (BAAI/bge-small-en-v1.5) for high-quality embeddings
- **🗄️ Vector Storage**: Weaviate database for efficient similarity search
- **🔍 Intelligent Search**: Semantic search capabilities for book recommendations
- **⚙️ Workflow Orchestration**: Complete pipeline automation with Apache Airflow
- **🐳 Containerized**: Docker-based setup for easy deployment

## 📁 Project Structure

```
RAG_Orchestrating_Workflows/
├── airflow/
│   ├── dags/
│   │   ├── hello_world.py              # Test DAG
│   │   ├── rag_data_ingestion.py       # Data processing pipeline
│   │   └── rag_query_dag.py            # Query and search pipeline
│   ├── include/
│   │   ├── data/                       # Book description files
│   │   ├── src/                        # Source code modules
│   │   ├── config/                     # Configuration files
│   │   └── utils/                      # Utility functions
│   └── logs/                           # Airflow execution logs
├── src/
│   ├── data_generator.py               # Generate book data
│   ├── data_loader.py                  # Data loading utilities
│   ├── embedding_service.py            # Embedding generation
│   └── vector_store.py                 # Weaviate operations
├── notebooks/                          # Learning notebooks
├── docker-compose.yml                  # Weaviate service
├── docker-compose-airflow.yml          # Airflow services
└── README.md
```

## 🛠️ Technology Stack

- **Orchestration**: Apache Airflow 2.8.1
- **Vector Database**: Weaviate 1.23.7
- **Embeddings**: FastEmbed (BAAI/bge-small-en-v1.5)
- **Containerization**: Docker & Docker Compose
- **Language**: Python 3.8+
- **Data Processing**: Pandas, NumPy

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.8+
- 8GB+ RAM recommended

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/RAG_Orchestrating_Workflows.git
cd RAG_Orchestrating_Workflows
```

### 2. Start Weaviate

```bash
docker-compose up -d
```

### 3. Start Airflow

```bash
docker-compose -f docker-compose-airflow.yml up -d
```

### 4. Access the Services

- **Airflow UI**: http://localhost:8081 (username: `airflow`, password: `airflow`)
- **Weaviate API**: http://localhost:8080

### 5. Run the Pipeline

1. Open Airflow UI
2. Enable the `rag_data_ingestion_dag`
3. Trigger the DAG to process book data
4. Enable and trigger `rag_query_dag` to test search functionality

## 📊 Available DAGs

### 1. Data Ingestion DAG (`rag_data_ingestion_dag`)
- Loads book descriptions from JSON files
- Validates data structure
- Generates vector embeddings using FastEmbed
- Creates Weaviate collection schema
- Stores books with embeddings in vector database
- Verifies successful storage

### 2. Query DAG (`rag_query_dag`)
- Processes user search queries
- Generates query embeddings
- Performs similarity search in Weaviate
- Returns ranked book recommendations
- Formats results for user consumption

## 🔍 Example Usage

### Search for Books
```python
# The query DAG will process queries like:
"science fiction adventure"
"philosophical books about consciousness"
"mystery detective novels"
```

### Expected Output
```
🔍 Search Query: "science fiction adventure"
📚 Found 5 relevant books:

1. Dune (1965)
   📝 Author: Frank Herbert
   ⭐ Similarity: 0.892
   📖 Description: A epic science fiction novel set on the desert planet...
```

## 🎓 Learning Resources

The `notebooks/` directory contains educational Jupyter notebooks:
- `L2.ipynb`: RAG Prototype development
- `L4.ipynb`: Converting notebooks to Airflow pipelines
- `L5.ipynb`: Scheduling and DAG parameters

## 🔧 Configuration

### Custom Package Installation
The Airflow containers automatically install:
- `fastembed==0.2.6`
- `weaviate-client==4.4.1`
- `numpy==1.24.4`
- `pandas==1.5.3`

### Environment Variables
Key configurations in `docker-compose-airflow.yml`:
- Database connection strings
- Weaviate endpoint configuration
- Custom package requirements

## 🧪 Testing

### Verify Setup
```bash
# Check if Weaviate is ready
curl http://localhost:8080/v1/.well-known/ready

# Check if data is stored
curl "http://localhost:8080/v1/objects?class=Books&limit=3"
```

## 📈 Monitoring

- **Airflow UI**: Monitor DAG executions, task logs, and pipeline health
- **Task Dependencies**: Visual representation of workflow dependencies
- **Error Handling**: Automatic retries and failure notifications

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Based on DeepLearning.AI's "Orchestrating Workflows for GenAI" course
- Uses open-source tools: Apache Airflow, Weaviate, FastEmbed
- Inspired by modern RAG architecture patterns

## 📞 Support

If you encounter any issues:
1. Check the Airflow logs in the UI
2. Verify Docker containers are running
3. Ensure all required ports are available
4. Review the troubleshooting section in notebooks

---

**Happy RAG Building!** 🚀📚🤖