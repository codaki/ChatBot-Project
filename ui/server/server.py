import requests
import json
import os
import re
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Constants
CHROMA_DIR = "../../vectordb_practice/chroma_db"
OLLAMA_BASE_URL = "http://localhost:11434"
MODEL_NAME = "llama3.1"

class OllamaLLM:
    def __init__(self, base_url=OLLAMA_BASE_URL, model=MODEL_NAME):
        self.base_url = base_url
        self.model = model
    def _remove_thinking(self, text):
        """Remove content between <think> and </think> tags"""
        return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
       
    def generate(self, prompt, temperature=0.8, max_tokens=2000):
        """Generate text using Ollama"""
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            raw_response = response.json()["response"]
            # Remove thinking sections before returning
            processed_response = self._remove_thinking(raw_response)
            return processed_response
        except Exception as e:
            print(f"Error generating response: {e}")
            return f"Error: {str(e)}"

def get_relevant_documents(query, db, k=3):
    """Retrieve relevant documents from vector store"""
    docs = db.similarity_search(query, k=k)
    return docs

def format_docs(docs):
    """Format documents into a single string"""
    return "\n\n".join([doc.page_content for doc in docs])

# Create Flask app
app = Flask(__name__, static_folder="../frontend")
CORS(app)  # Enable CORS for all routes

# Initialize global components
embeddings = None
db = None
llm = None
prompt = None

def initialize_rag():
    """Initialize RAG components"""
    global embeddings, db, llm, prompt
    
    # Initialize embedding model for ChromaDB
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Load the persisted ChromaDB database
    if not os.path.exists(CHROMA_DIR):
        print(f"Error: ChromaDB directory '{CHROMA_DIR}' not found.")
        print("Please run ingest.py first to create the vector database.")
        return False
    
    db = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
    
    # Initialize Ollama client
    llm = OllamaLLM()
    
    # Create RAG prompt template
    rag_template = """
    You are an expert AI assistant. Use the provided context to give **direct**, **clear**, and **confident** answers to the question at the end. Avoid hedging expressions like "It seems" or "According to the context." Write the answer naturally as if you already know it, based on the context provided.

    - If you do not have enough information **from the context** to answer, say: "I don't have enough information to answer that."
    - If the question is **unrelated** to the context, answer based on your general knowledge.
    - Do **NOT** use phrases like "Based on the context," "It seems," or "In summary." Write the answer as **factual**.
    - Your tone should be **professional**, **friendly**, and **confident**.
    - Use relevant details from the context to **support** your answer, but **affirm** what the context says.
    - Avoid **repetition** and **redundancy** in your answers.
    - Avoid using **in summary** or **in conclusion** phrases.
    - If the question is **ambiguous**, ask for clarification instead of guessing.

    Context:
    {context}

    Question: {question}

    Answer:
    """

    prompt = PromptTemplate(
        template=rag_template,
        input_variables=["context", "question"]
    )
    
    return True

# API endpoint for chat
@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        # Get message from request
        data = request.json
        query = data.get("message", "")
        
        # 1. Retrieve relevant documents
        docs = get_relevant_documents(query, db)
        context = format_docs(docs)
        
        # 2. Format the prompt with context and query
        full_prompt = prompt.format(context=context, question=query)
        
        # 3. Generate response using Ollama
        response = llm.generate(full_prompt)
        
        return jsonify({"response": response})
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"response": f"Sorry, an error occurred: {str(e)}"}), 500

# Serve static files
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path == "" or path == "/":
        return send_from_directory("../frontend", "chat.html")
    return send_from_directory("../frontend", path)

if __name__ == "__main__":
    print("Initializing RAG system...")
    if initialize_rag():
        print("RAG system initialized successfully.")
        print("Starting server on http://localhost:5000")
        app.run(host="0.0.0.0", port=5000, debug=True)
    else:
        print("Failed to initialize RAG system. Exiting.")