from pymongo import MongoClient
from config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME

def query_documents(query):
    try:
        # Establish MongoDB connection using credentials from config
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

# Fetch documents using a simple MongoDB query
client = MongoClient("mongodb://localhost:27017/")
db = client["document_db"]
collection = db["documents"]

def fetch_documents(query):
    # Perform a full-text search query
    cursor = collection.find({"$text": {"$search": query}})
    file_names = []
    texts = []
    pdf_links = []

    # Extract relevant fields from the documents
    for doc in cursor:
        file_names.append(doc["filename"])
        texts.append(doc["text"])
        pdf_links.append(doc.get("pdf_link", "#"))

    return file_names, texts, pdf_links
