import streamlit as st
from app.ocr_utils import pdf_to_text
from app.embed import get_ollama_embedding
from app.db import insert_document, search_similar
from app.rag import generate_answer
import tempfile
import os

st.set_page_config(page_title="RAG PDF QA", layout="wide")
st.title("📄🧠 RAG with Ollama + Streamlit + MongoDB")

# Initialize session state variables
if 'text' not in st.session_state:
    st.session_state.text = ""
if 'query' not in st.session_state:
    st.session_state.query = ""
if 'answer' not in st.session_state:
    st.session_state.answer = ""

# Reset app state
if st.button("🔄 Reset App State"):
    st.session_state.text = ""
    st.session_state.query = ""
    st.session_state.answer = ""
    st.experimental_rerun()

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    st.success("✅ File uploaded. Extracting text...")

    # OCR text extraction
    text = pdf_to_text(tmp_path)
    st.session_state.text = text  # Save extracted text in session state
    st.text_area("📄 Extracted Text", st.session_state.text, height=200)

    if st.button("🚀 Embed and Save to MongoDB"):
        try:
            embedding = get_ollama_embedding(st.session_state.text)
            insert_document(st.session_state.text, embedding)
            st.success("✅ Document embedded and stored in database.")
        except Exception as e:
            st.error(f"❌ Error during embedding or DB insertion: {e}")

# Ask question section (always visible)
st.markdown("---")
st.subheader("💬 Ask a Question about the Uploaded Document")

st.session_state.query = st.text_input("Type your question here:", value=st.session_state.query)

if st.button("Get Answer") and st.session_state.query:
    try:
        answer = generate_answer(st.session_state.query)
        st.session_state.answer = answer
        st.markdown("### 🧠 Answer")
        st.write(st.session_state.answer)
    except Exception as e:
        st.error(f"❌ Error generating answer: {e}")
