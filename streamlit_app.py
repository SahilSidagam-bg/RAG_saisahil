import os
import streamlit as st
from scripts.ingest import ingest_documents
from scripts.query import stream_answer
from config import FAISS_INDEX_DIR
import shutil

st.set_page_config(page_title="RAG Q&A with FAISS", layout="centered")
st.title("🧠 RAG Assistant (FAISS + Ollama)")
st.markdown("Upload `.txt` or scanned `.pdf` files to ingest. Ask any question below.")

# Upload section
uploaded_files = st.file_uploader("Upload files", type=["txt", "pdf"], accept_multiple_files=True)

# Ingestion handling
def process_uploaded_files(uploaded_files):
    # Save uploaded files to the 'data' directory
    uploaded_file_paths = []
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    
    # Ensure the data directory exists
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    for uploaded_file in uploaded_files:
        file_path = os.path.join(data_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        uploaded_file_paths.append(file_path)

    return uploaded_file_paths

if uploaded_files:
    # User uploaded files
    st.info("Ingesting documents...")
    uploaded_file_paths = process_uploaded_files(uploaded_files)
    
    try:
        # Trigger ingestion with FAISS
        ingest_documents(os.path.join(os.path.dirname(__file__), "..", "data"))
        st.success("✅ Documents ingested successfully!")

        # Optional: Clean up after ingestion
        # Remove the uploaded files from the 'data' folder after processing
        for file_path in uploaded_file_paths:
            os.remove(file_path)
        
    except Exception as e:
        st.error(f"❌ Error during ingestion: {e}")

# Ask question
query = st.text_input("Ask a question:")

if query:
    st.write("### 💡 Answer")
    try:
        st.write_stream(stream_answer(query))
    except Exception as e:
        st.error(f"❌ Streaming failed: {e}")
