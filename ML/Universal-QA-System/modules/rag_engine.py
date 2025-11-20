import torch
import streamlit as st
import ollama
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

@st.cache_resource
def get_embedding_model():
    """Loads the embedding model once and caches it."""
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model_kwargs = {'device': device}
    encode_kwargs = {'normalize_embeddings': True}
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

def create_vector_store(documents):
    """Splits docs and creates a FAISS vector store."""
    embeddings = get_embedding_model()
    if not embeddings:
        return None
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    chunks = text_splitter.split_documents(documents)
    vector_store = FAISS.from_documents(chunks, embeddings)
    return vector_store

def query_ollama(vector_store, question, model="llama3.1"):
    """Retrieves context and queries Ollama."""
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    results = retriever.invoke(question)
    context = "\n\n".join([r.page_content for r in results])

    prompt = f"""
    You are an AI assistant. Answer ONLY using the context provided below.

    Context:
    {context}

    Question: {question}

    If the answer is not found in the context, reply "Information not found in document."
    """
    
    try:
        response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
        return response["message"]["content"]
    except Exception as e:
        return f"Error querying Ollama: {e}"