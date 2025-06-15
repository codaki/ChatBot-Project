import os
import logging
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import CHROMA_DIR, EMBEDDING_MODEL_NAME, CHUNK_SIZE, CHUNK_OVERLAP
from loaders import load_all_documents
from utils import file_hash

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HASH_DB_FILE = "file_hashes.txt"

def get_existing_hashes():
    if not os.path.exists(HASH_DB_FILE):
        return set()
    with open(HASH_DB_FILE, "r") as f:
        return set(line.strip() for line in f.readlines())

def save_hash(hash_value):
    with open(HASH_DB_FILE, "a") as f:
        f.write(f"{hash_value}\n")

def ingest():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    db = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

    existing_hashes = get_existing_hashes()
    all_documents = load_all_documents()

    logger.info(f"Loaded {len(all_documents)} documents")

    new_chunks = []

    for doc in all_documents:
        source = doc.metadata.get("source", "unknown")

        if source != "unknown" and os.path.exists(source):
            hash_value = file_hash(source)
            if hash_value in existing_hashes:
                logger.info(f"Skipping already ingested file: {source}")
                continue
            save_hash(hash_value)

        chunks = text_splitter.split_documents([doc])
        for chunk in chunks:
            if source != "unknown":
                chunk.metadata["source"] = source
        new_chunks.extend(chunks)

    logger.info(f"Adding {len(new_chunks)} new chunks to ChromaDB")
    db.add_documents(new_chunks)

    logger.info("✅ Ingestion complete!")

if __name__ == "__main__":
    ingest()
