from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Load environment variables
load_dotenv()

# Get MongoDB credentials from the .env file
username = os.getenv('MONGO_USERNAME')  # MongoDB username
password = os.getenv('MONGO_PASSWORD')  # MongoDB password

# Ensure password is a string and URL encode it
encoded_password = quote_plus(str(password))

# Construct MongoDB URI
uri = "mongodb+srv://saisahil:<password>@ragdb.1siejk7.mongodb.net/?retryWrites=true&w=majority&appName=RAGdb"

# Connect to MongoDB and access the database
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['rag_db']  # Replace with your database name
collection = db['documents']  # Replace with your collection name

def insert_document(text, embedding):
    """Inserts a document and its embedding into the MongoDB collection."""
    collection.insert_one({
        'text': text,
        'embedding': embedding
    })

def search_similar(query_embedding, limit=3):
    """Searches the MongoDB collection for documents with similar embeddings."""
    return list(collection.aggregate([
        {
            "$vectorSearch": {
                "index": "default",
                "queryVector": query_embedding,
                "path": "embedding",
                "numCandidates": 100,
                "limit": limit
            }
        }
    ]))
