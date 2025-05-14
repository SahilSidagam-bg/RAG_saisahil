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
uri = "mongodb+srv://saisahil:mongodbpassword@ragdb.1siejk7.mongodb.net/RAGdb?retryWrites=true&w=majority&appName=RAGdb"


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

def search_similar(query_embedding, top_k=3):
    """Search for similar documents using MongoDB Atlas vector search."""
    pipeline = [
        {
            "$search": {
                "index": "default",  # default index name
                "knnBeta": {
                    "vector": query_embedding,
                    "path": "embedding",
                    "k": top_k
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "text": 1,
                "score": {"$meta": "searchScore"}
            }
        }
    ]
    return list(collection.aggregate(pipeline))
