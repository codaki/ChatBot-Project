import requests
import json
import os
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate

# Constants
CHROMA_DIR = "./chroma_db"
OLLAMA_BASE_URL = "http://localhost:11434"
MODEL_NAME = "llama3.1:8b"

class OllamaLLM:
    def __init__(self, base_url=OLLAMA_BASE_URL, model=MODEL_NAME):
        self.base_url = base_url
        self.model = model
        
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
            return response.json()["response"]
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

def main():
    # Initialize embedding model for ChromaDB
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Load the persisted ChromaDB database
    if not os.path.exists(CHROMA_DIR):
        print(f"Error: ChromaDB directory '{CHROMA_DIR}' not found.")
        print("Please run ingest.py first to create the vector database.")
        return
    
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
    - Avoid using ** in summary** or **in conclusion** phrases.
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
    
    print("RAG System with Llama3.1 and ChromaDB")
    print("Type 'exit' to quit")
    print("-" * 50)
    
    # Interactive Q&A loop
    while True:
        query = input("\nEnter your question: ")
        if query.lower() == 'exit':
            break
        
        # 1. Retrieve relevant documents
        print("Retrieving context...")
        docs = get_relevant_documents(query, db)
        context = format_docs(docs)
        
        # 2. Format the prompt with context and query
        full_prompt = prompt.format(context=context, question=query)
        
        # 3. Generate response using Ollama
        print("Generating response...")
        response = llm.generate(full_prompt)
        
        print("\nAnswer:")
        print(response)

if __name__ == "__main__":
    main()