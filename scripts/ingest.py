import os
from langchain.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import FAISS
from tqdm import tqdm
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
from config import OLLAMA_EMBED_MODEL

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
FAISS_INDEX_DIR = os.path.join(os.path.dirname(__file__), "..", "faiss_index")

# Load scanned PDFs using OCR
def load_scanned_pdf(path):
    images = convert_from_path(path)
    full_text = ""
    for i, img in enumerate(images):
        text = pytesseract.image_to_string(img)
        print(f"🖼️ OCR page {i+1} text preview: {text[:200]}")
        full_text += text + "\n"
    return full_text


# Load documents from directory
from langchain.document_loaders import TextLoader, PyPDFLoader
from langchain.schema import Document  # Required to create Document objects manually

from langchain.document_loaders import TextLoader, PyPDFLoader
from langchain.schema import Document

from langchain.schema import Document

from langchain.schema import Document

def load_documents(directory):
    docs = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if filename.endswith(".txt"):
            loaded_docs = TextLoader(filepath).load()
            for doc in loaded_docs:
                print(f"Loaded text from {filename}: {doc.get('page_content', 'No content found')[:200]}...")  # Preview first 200 chars
                if doc.get('page_content').strip():  # Check if content is non-empty
                    docs.append(doc)
                else:
                    print(f"⚠️ Skipped empty text document: {filename}")
        elif filename.endswith(".pdf"):
            try:
                loaded_docs = PyPDFLoader(filepath).load()
                for doc in loaded_docs:
                    print(f"Loaded PDF text from {filename}: {doc.get('page_content', 'No content found')[:200]}...")  # Preview first 200 chars
                    if doc.get('page_content').strip():  # Check if content is non-empty
                        docs.append(doc)
                    else:
                        print(f"⚠️ Skipped empty PDF: {filename}")
            except Exception as e:
                print(f"⚠️ Error loading PDF: {filename}, error: {e}")
                print(f"⚠️ Scanned PDF detected, using OCR: {filename}")
                try:
                    text = load_scanned_pdf(filepath)
                    if text.strip():  # Only add non-empty OCR text
                        docs.append(Document(page_content=text, metadata={"source": filename}))
                    else:
                        print(f"⚠️ Skipped empty OCR text from: {filename}")
                except Exception as ocr_error:
                    print(f"❌ OCR failed for {filename}: {ocr_error}")
    
    print(f"Loaded {len(docs)} documents.")
    return docs




# Ingest documents and generate embeddings with FAISS storage
def ingest_documents(directory):
    documents = load_documents(directory)

    print(f"📄 Loaded {len(documents)} documents.")
    for i, doc in enumerate(documents[:3]):
     print(f"🔹 Document {i+1} preview: {doc.page_content[:200]}")

    if not documents:
        raise ValueError("No documents found. Please check the input files.")

    # ✅ Filter out empty docs
    documents = [doc for doc in documents if doc.page_content.strip()]

    print(f"📄 {len(documents)} non-empty documents loaded.")

    # ✅ Optional: Preview document content
    for i, doc in enumerate(documents[:5]):
        print(f"\n[DEBUG] Document {i} content preview:\n{doc.page_content[:300]}")

    # Split the documents into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=30)
    chunks = splitter.split_documents(documents)

    # Print the number of chunks created
    print(f"✂️ Split into {len(chunks)} chunks.")

    for i, chunk in enumerate(chunks[:3]):
        print(f"🔸 Chunk {i+1}: {chunk.page_content[:200]}")


    if not chunks:
        raise ValueError("No chunks were created. Please check the document splitting logic.")

    print(f"🧩 Created {len(chunks)} chunks.")

    # Generate embeddings
    embeddings = OllamaEmbeddings(model=OLLAMA_EMBED_MODEL)

    # Load existing FAISS index or create a new one
    if os.path.exists(FAISS_INDEX_DIR):
        vector_store = FAISS.load_local(FAISS_INDEX_DIR, embeddings)
        print("✅ FAISS index loaded.")
    else:
        vector_store = FAISS.from_documents(chunks, embeddings)
        vector_store.save_local(FAISS_INDEX_DIR)
        print("✅ New FAISS index created and saved.")

    vector_store.add_documents(chunks)
    print("✅ Ingestion complete.")



# All imports ...

# All function definitions including ingest_documents ...

def main():
    print("📄 Loading documents...")
    try:
        ingest_documents(DATA_DIR)
    except Exception as e:
        print(f"❌ Error during ingestion: {e}")

# ✅ Correct placement of entry point
if __name__ == "__main__":
    main()


