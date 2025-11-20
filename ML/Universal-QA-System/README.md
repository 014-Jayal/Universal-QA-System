# 🌐 Universal Q&A System (RAG + NL-to-SQL)

An intelligent Question & Answer system that bridges the gap between unstructured data (Documents) and structured data (Databases). This application allows users to chat with PDFs using **RAG (Retrieval-Augmented Generation)** and query SQL databases using **Natural Language**.

## 🚀 Features

### 1. Document Q&A (RAG Engine)
- **Upload & Chat:** Support for PDF, DOCX, and TXT files.
- **Local LLM Support:** Uses **Ollama (Llama 3)** for privacy-focused, offline inference.
- **Vector Search:** Utilizes **FAISS** and **HuggingFace Embeddings** for accurate context retrieval.

### 2. Database Q&A (NL-to-SQL Engine)
- **Natural Language Queries:** Convert English questions (e.g., *"How many users are above age 25?"*) into executable SQL queries.
- **Smart Schema Awareness:** Automatically detects table schemas and columns.
- **Fuzzy Matching:** Handles typos in column names gracefully.
- **Data Visualization:** Displays results in interactive tables with CSV download options.

## 🛠️ Tech Stack
- **Frontend:** Streamlit
- **LLM Integration:** Ollama, LangChain
- **Embeddings:** Sentence-Transformers (HuggingFace)
- **Vector Store:** FAISS
- **Data Processing:** Pandas, PyPDF, Docx2txt

## 📂 Project Structure
```bash
Universal-QA-System/
├── modules/
│   ├── rag_engine.py    # Handles Embeddings, Vector Store, and LLM calls
│   └── sql_engine.py    # Handles Natural Language to SQL conversion
├── utils/
│   └── file_loader.py   # parsers for PDF/DOCX/TXT
├── app.py               # Main Streamlit Interface
└── requirements.txt     # Dependencies