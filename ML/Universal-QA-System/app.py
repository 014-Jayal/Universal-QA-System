import os
import shutil
import sqlite3
import pandas as pd
import streamlit as st
from modules.rag_engine import create_vector_store, query_ollama
from modules.sql_engine import natural_language_to_sql, execute_sql_query
from utils.file_loader import load_document

# -------------------------
# App Config
# -------------------------
st.set_page_config(page_title="Universal Q&A System", layout="wide")
st.title("🌐 Universal Q&A System")

# Temp folder setup
TEMP_DIR = "temp_files"
if os.path.exists(TEMP_DIR):
    shutil.rmtree(TEMP_DIR)
os.makedirs(TEMP_DIR, exist_ok=True)

# -------------------------
# Tabs
# -------------------------
tab_doc, tab_db = st.tabs(["📄 Document Q&A", "📊 Database Q&A"])

# =========================
# TAB 1: RAG (Document)
# =========================
with tab_doc:
    st.header("📄 Chat with Documents (Ollama)")
    uploaded_file = st.file_uploader("Upload PDF/DOCX/TXT", type=["pdf", "docx", "txt"])
    
    if uploaded_file:
        file_path = os.path.join(TEMP_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        docs, error = load_document(file_path)
        
        if error:
            st.error(error)
        elif docs:
            with st.spinner("Indexing document..."):
                vector_store = create_vector_store(docs)
                st.success("Document processed!")
            
            question = st.text_input("Ask a question about the document:")
            if question and vector_store:
                with st.spinner("Thinking..."):
                    answer = query_ollama(vector_store, question)
                    st.subheader("🧠 Answer:")
                    st.write(answer)

# =========================
# TAB 2: SQL (Database)
# =========================
with tab_db:
    st.header("📊 Chat with Database")
    db_file = st.file_uploader("Upload SQLite (.db) or CSV", type=["db", "csv"])
    
    if db_file:
        ext = os.path.splitext(db_file.name)[1].lower()
        
        # Handle CSV vs DB
        if ext == ".csv":
            df = pd.read_csv(db_file)
            conn = sqlite3.connect(":memory:")
            df.to_sql("data", conn, index=False, if_exists="replace")
            db_schema = {"data": df.columns.tolist()}
            db_source = conn
            st.dataframe(df.head(3))
        else:
            temp_db_path = os.path.join(TEMP_DIR, "uploaded.db")
            with open(temp_db_path, "wb") as f:
                f.write(db_file.read())
            conn = sqlite3.connect(temp_db_path)
            
            # Extract Schema
            tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
            db_schema = {}
            for t in tables['name']:
                cols = pd.read_sql(f"PRAGMA table_info({t});", conn)
                db_schema[t] = list(cols['name'])
            db_source = temp_db_path
            st.write(f"Tables found: {list(db_schema.keys())}")

        # Query Interface
        selected_table = st.selectbox("Select Table", list(db_schema.keys()))
        nl_query = st.text_input("Ask a question (e.g., 'Show me users above age 25')")
        
        if nl_query:
            # 1. Translate NL -> SQL
            schema_subset = {selected_table: db_schema[selected_table]}
            sql_query = natural_language_to_sql(nl_query, schema_subset)
            
            st.code(sql_query, language="sql")
            
            # 2. Execute SQL
            df_result, err = execute_sql_query(db_source, sql_query)
            
            if err:
                st.error(err)
            elif df_result is not None and not df_result.empty:
                st.dataframe(df_result)
            else:
                st.info("No results found.")