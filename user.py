from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Construct MongoDB URI
uri = "mongodb+srv://saisahil:mongodbpassword@ragdb.1siejk7.mongodb.net/RAGdb?retryWrites=true&w=majority&appName=RAGdb"

# Connect to MongoDB and access the database
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['RAGdb']  # Replace with your database name

# List all collection names in the database
collection_names = db.list_collection_names()
print("Collections in the 'rag_db' database:")
print(collection_names)
