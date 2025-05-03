
import pymongo
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# MongoDB setup
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["doc_db"]
collection = db["extracted_text"]

# Preprocessing function
def preprocess_text(text):
    words = word_tokenize(text)
    words = [word.lower() for word in words if word.isalpha()]
    stop_words = set(stopwords.words("english"))
    filtered_words = [word for word in words if word not in stop_words]
    return " ".join(filtered_words)

# Process documents in MongoDB
def process_documents():
    for doc in collection.find():
        file_name = doc["file_name"]
        if "preprocessed_text" in doc:
            print(f"{file_name} already has preprocessed text. Skipping...")
        else:
            extracted_text = doc["extracted_text"]
            preprocessed_text = preprocess_text(extracted_text)
            collection.update_one(
                {"_id": doc["_id"]},
                {"$set": {"preprocessed_text": preprocessed_text}}
            )
            print(f"Preprocessed and saved text for {file_name}")

# Run preprocessing
process_documents()

import pymongo
import re

# MongoDB setup
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["document_db"]
collection = db["documents"]

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces/newlines
    text = re.sub(r'[^a-zA-Z0-9,.!? ]+', '', text)  # Keep only readable text
    return text.strip()

def preprocess_documents():
    documents = collection.find({})
    
    for doc in documents:
        doc_id = doc["_id"]
        raw_text = doc.get("text", "")  # Now it correctly fetches from "text"

        if not raw_text:
            print(f"Skipping {doc['filename']} (No extracted text)")
            continue

        # Clean text
        cleaned_text = clean_text(raw_text)

        # Update document with cleaned text
        collection.update_one(
            {"_id": doc_id},
            {"$set": {"cleaned_text": cleaned_text}}
        )
        print(f"Processed document: {doc['filename']}")

if __name__ == "__main__":
    preprocess_documents()
    print("Preprocessing complete.")
