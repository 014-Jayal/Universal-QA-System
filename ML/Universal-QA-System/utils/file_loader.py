import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader

def load_document(file_path):
    """Loads a document based on its extension."""
    ext = os.path.splitext(file_path)[1].lower()
    loader = None
    
    try:
        if ext == ".pdf":
            loader = PyPDFLoader(file_path)
        elif ext == ".docx":
            loader = Docx2txtLoader(file_path)
        elif ext == ".txt":
            loader = TextLoader(file_path)
        else:
            return None, f"Unsupported file type: {ext}"
            
        return loader.load(), None
    except Exception as e:
        return None, str(e)