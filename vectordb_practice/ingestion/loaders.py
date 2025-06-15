import os
from langchain_community.document_loaders import (
    PyPDFLoader, DirectoryLoader, UnstructuredFileLoader
)
from langchain_community.document_loaders.sql_database import SQLDatabaseLoader
from langchain_community.utilities.sql_database import SQLDatabase
from config import DATA_DIR, DATABASE_URL

def load_pdfs():
    loader = DirectoryLoader(DATA_DIR, glob="**/*.pdf", loader_cls=PyPDFLoader)
    return loader.load()

def load_txt_docs():
    loader = DirectoryLoader(DATA_DIR, glob="**/*.txt", loader_cls=UnstructuredFileLoader)
    return loader.load()

def load_sql_documents(query="SELECT id, title, content FROM documents"):
    if DATABASE_URL is None:
        return []
    sql_db = SQLDatabase.from_uri(DATABASE_URL)
    loader = SQLDatabaseLoader(sql_db, query=query)
    return loader.load()

def load_all_documents():
    return load_pdfs() + load_txt_docs() + load_sql_documents()
