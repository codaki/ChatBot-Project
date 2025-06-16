# RAG Chatbot UI

A **modern web-based chatbot interface** that uses **Retrieval-Augmented Generation (RAG)** to answer questions based on your document database.

## 🚀 Overview

This application provides a conversational interface where users can ask questions about documents stored in a vector database. The system retrieves relevant context from the database and uses a Large Language Model (LLM) to generate accurate, contextual responses.

<p align="center">
  <img src="./public/screenshot.png" alt="RAG Chatbot Screenshot" width="500" />
</p>

---

## ✨ Features

- **Conversational UI**: Clean, responsive chat interface with typing animations
- **RAG Architecture**: Combines document retrieval with LLM-based response generation
- **Markdown Support**: Bot responses support markdown formatting
- **Real-time Typing Effect**: Bot responses appear character-by-character for a natural conversational experience

---

## 🛠️ Technologies Used

**Frontend:**

- Vanilla HTML, CSS & JavaScript
- **Marked.js**: Renders markdown in bot responses

**Backend:**

- **Flask**: Python web server framework
- **LangChain**: Framework for building LLM applications
- **ChromaDB**: Vector database for document embeddings
- **HuggingFace Embeddings**: `all-MiniLM-L6-v2` for generating vector representations
- **Ollama**: Local LLM serving platform
- **Llama3.1**: The Large Language Model used for generating responses

---

## ⚙️ Requirements

- Python 3.8+
- [Ollama](https://ollama.com/) installed and running locally
- ChromaDB with ingested documents

---

## 📦 Setup & Installation

1. **Clone the repository:**

```bash
git clone https://github.com/your-username/rag-chatbot-ui.git
cd rag-chatbot-ui
```

2. **Install Python dependencies:**

```bash
pip install -r requirements.txt
```

3. **Ensure Ollama is installed and running:**

```bash
# Check if Ollama is running
curl http://localhost:11434/api/version

# If not running, start Ollama and pull the model
ollama run llama3.1
```

4. **Ingest documents into ChromaDB (if not done yet):**

```bash
python ingest.py
```

---

## ▶️ Running the Application

1. **Start the Flask server:**

```bash
cd ui/server
python server.py
```

2. **Open the application in your browser:**

```
http://localhost:5000
```

---

## 💬 Usage

1. Type your question in the chat input box.
2. Press **Enter** or click **Send**.
3. The chatbot retrieves relevant context and generates a response.
4. Continue the conversation naturally.

---

## 🎨 Customization

- Modify `/ui/frontend/css/style.css` to change the appearance.
- Adjust parameters in `server.py`, such as:

  - `k`: Number of retrieved documents
  - `temperature`: Generation randomness
  - **Model**: Choose another LLM
  - **Prompt template**: Customize instruction context for the model

---

## 📁 Project Structure

```
ui/
├── readme.md                # Project documentation
├── frontend/                # Frontend code
│   ├── chat.html            # Main HTML page
│   ├── chat.js              # Chat logic (JavaScript)
│   └── css/
│       └── style.css        # Styling (CSS)
└── server/                  # Backend code
    └── server.py            # Flask server with RAG logic
```

---

## 🤝 Contributing

Contributions are welcome! Please open an [issue](https://github.com/codaki/rag-chatbot-ui/issues) or submit a pull request for improvements or feature suggestions.

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 📚 References

- [LangChain Documentation](https://python.langchain.com/)
- [Ollama](https://ollama.com/)
- [ChromaDB](https://www.trychroma.com/)
- [Hugging Face Embeddings](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
