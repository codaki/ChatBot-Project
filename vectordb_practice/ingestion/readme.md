# Document Ingestion System

A system for processing and indexing documents into a vector database for RAG (Retrieval-Augmented Generation) applications.

## 📋 Overview

This ingestion module processes various document types (PDF, TXT, SQL database records) and stores them as vector embeddings in ChromaDB for semantic search and retrieval. It includes deduplication through file hashing to avoid reprocessing already ingested documents.

## 🔧 Components

- **ingest.py**: Main script for document processing and vector storage
- **loaders.py**: Document loading utilities for different file types
- **config.py**: Configuration settings for the ingestion process
- **utils.py**: Helper functions (e.g., file hashing)

## ⚙️ Configuration

The system can be configured through environment variables or a `.env` file:

| Variable       | Description               | Default        |
| -------------- | ------------------------- | -------------- |
| `CHROMA_DIR`   | ChromaDB storage location | `../chroma_db` |
| `DATA_DIR`     | Source documents location | `../data`      |
| `DATABASE_URL` | Optional SQL database URL | None           |

Additional configuration in `config.py`:

- `EMBEDDING_MODEL_NAME`: "all-MiniLM-L6-v2"
- `CHUNK_SIZE`: 500
- `CHUNK_OVERLAP`: 50

## 🚀 Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
