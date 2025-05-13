import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB settings removed as you are now using FAISS
# MONGO_URI = os.getenv("MONGO_URI")
# MONGO_DB = os.getenv("MONGO_DB", "RAGembeddings")
# MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "embeddings")

OLLAMA_EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
OLLAMA_LLM_MODEL = os.getenv("OLLAMA_LLM_MODEL", "llama3")

FAISS_INDEX_DIR = os.path.join(os.path.dirname(__file__), "faiss_index")
