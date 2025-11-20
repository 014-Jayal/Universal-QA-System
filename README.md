# Universal Q&A System

## Overview
The Universal Q&A System is a unified interface designed to interact seamlessly with both unstructured data (documents) and structured data (databases). It incorporates Retrieval-Augmented Generation (RAG) for document-based question answering and a Natural Language to SQL (NL2SQL) engine for querying databases through plain English instructions.

This system provides a powerful, local, privacy-preserving solution using Ollama-based LLMs and efficient vector retrieval mechanisms.

---

## Key Features

### Document Intelligence (RAG)
- Multi-format document ingestion including PDF, DOCX, and TXT.
- Local, privacy-first inference using Ollama (Llama 3).
- FAISS vector store with HuggingFace MiniLM embeddings.
- High-accuracy contextual retrieval to minimize hallucinations.

### Database Intelligence (Text-to-SQL)
- Automatic schema extraction from uploaded CSV/SQLite files.
- Intelligent fuzzy matching for column names and user typos.
- Supports aggregations such as COUNT, SUM, AVG, MAX, MIN, GROUP BY.
- Handles conditional filters and dynamic SQL generation.
- Displays results using interactive dataframes with export support.

---

## Architecture

### RAG Pipeline
1. Document uploaded.
2. Text preprocessing and splitting.
3. Embedding generation using HuggingFace models.
4. Indexing with FAISS vector store.
5. Retrieval of relevant chunks.
6. Response generation using local LLM (Ollama).

### SQL Generation Pipeline
1. User question parsed and normalized.
2. Schema-aware keyword extraction and fuzzy column matching.
3. SQL query construction.
4. Execution on SQLite engine.
5. Results returned as an interactive dataframe.

---

## Project Structure
Universal-QA-System/
├── modules/
│   ├── __init__.py
│   ├── rag_engine.py       # Embeddings, vector DB, and RAG logic
│   └── sql_engine.py       # NL2SQL parsing, SQL construction, query execution
├── utils/
│   ├── __init__.py
│   └── file_loader.py      # PDF, DOCX, TXT parsing utilities
├── temp_files/             # Temporary uploaded files
├── app.py                  # Streamlit application
├── requirements.txt        # Dependencies
└── README.md               # Documentation

---

## Installation & Setup

### Prerequisites
- Python 3.10 or higher
- Ollama installed and running locally

### Step 1: Clone the Repository
git clone https://github.com/YOUR_USERNAME/Universal-QA-System.git
cd Universal-QA-System

### Step 2: Create and Activate Virtual Environment
Windows:
python -m venv venv
venv\Scripts\activate

macOS/Linux:
python3 -m venv venv
source venv/bin/activate

### Step 3: Install Dependencies
pip install -r requirements.txt

### Step 4: Pull LLM Model via Ollama
ollama pull llama3.1

### Step 5: Run the Application
streamlit run app.py

---

## Usage Guide

### Document Q&A
1. Navigate to the Document Q&A tab.
2. Upload a PDF or DOCX file.
3. Wait for indexing to complete.
4. Enter questions such as:
   - "What are the objectives of this policy?"
   - "Summarize the key findings."

### Database Q&A
1. Navigate to the Database Q&A tab.
2. Upload a CSV or SQLite database file.
3. Select a table from the schema.
4. Ask questions like:
   - "How many employees are in the dataset?"
   - "Show me the top 10 products by revenue."
   - "What is the average age by department?"

---

## Roadmap
- Multi-document RAG support
- Automated chart generation for SQL outputs
- Session-based chat history
- Docker-based deployment

---

## Contributing
Contributions are welcome. To contribute:
1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Open a pull request.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.
