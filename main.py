import streamlit as st
from app.ocr_utils import pdf_to_text
from app.embed import get_ollama_embedding
from app.db import insert_document, search_similar
from app.rag import generate_answer
import tempfile

st.title("📄🧠 RAG with Ollama + Streamlit + MongoDB")

menu = st.sidebar.selectbox("Select Option", ["Upload PDF", "Ask Question"])

if menu == "Upload PDF":
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")
    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name
        st.success("File uploaded. Extracting text...")
        text = pdf_to_text(tmp_path)
        st.text_area("Extracted Text", text, height=200)
        if st.button("Embed and Save"):
            embedding = get_ollama_embedding(text)  # Get the embedding for the text
            insert_document(text, embedding)  # Save it to MongoDB
            st.success("Document embedded and saved to DB.")

elif menu == "Ask Question":
    query = st.text_input("Ask your question:")
    if st.button("Get Answer") and query:
        answer = generate_answer(query)  # Generate the answer based on the query
        st.markdown("### Answer")
        st.write(answer)
