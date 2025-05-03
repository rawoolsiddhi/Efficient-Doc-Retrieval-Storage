<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 5ec07714bff833219f57c48f2792d6e0f26abf96
from pymongo import MongoClient
from config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME

def query_documents(query):
    try:
        client = MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]
        
        # Search the collection based on query
        result = collection.find(query)
        
        # Print the results
        for document in result:
            print(document)
        client.close()
    except Exception as e:
        print(f"Error querying MongoDB: {e}")

if __name__ == "__main__":
    # Example: Query documents that contain the word "data"
    query = {"text": {"$regex": "data", "$options": "i"}}  # Example query
    query_documents(query)
<<<<<<< HEAD
=======
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["document_db"]
collection = db["documents"]


def fetch_documents(query):
    cursor = collection.find({"$text": {"$search": query}})
    file_names = []
    texts = []
    pdf_links = []

    for doc in cursor:
        file_names.append(doc["filename"])
        texts.append(doc["text"])
        pdf_links.append(doc.get("pdf_link", "#"))

    return file_names, texts, pdf_links
>>>>>>> c51ece5 (Clean start: add source, app, and essential files only)
=======
>>>>>>> 5ec07714bff833219f57c48f2792d6e0f26abf96
