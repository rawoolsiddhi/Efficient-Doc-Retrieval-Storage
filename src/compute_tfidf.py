
import pymongo
from sklearn.feature_extraction.text import TfidfVectorizer

# MongoDB setup
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["doc_db"]
collection = db["extracted_text"]

def retrieve_documents():
    # Retrieve documents with file name and extracted text
    documents_cursor = collection.find({}, {"_id": 0, "file_name": 1, "extracted_text": 1})
    docs = []
    for doc in documents_cursor:
        text = doc.get("extracted_text", "").strip()
        if text:
            docs.append(text)
        else:
            print(f"Warning: Document '{doc.get('file_name', 'Unknown')}' has empty extracted_text.")
    return docs

def compute_tfidf(documents):
    # For debugging, try disabling stop words removal if needed:
    vectorizer = TfidfVectorizer(stop_words='english')
    # If you suspect that stopwords removal is eliminating too much, try:
    # vectorizer = TfidfVectorizer(stop_words=None)
    tfidf_matrix = vectorizer.fit_transform(documents)
    return tfidf_matrix, vectorizer

def main():
    print("Retrieving documents from MongoDB...")
    documents = retrieve_documents()
    
    if not documents:
        print("No documents found in MongoDB or all documents are empty!")
        return

    # Debug: Print information about each document
    for i, doc in enumerate(documents):
        print(f"Document {i}: Length = {len(doc)}; Sample = '{doc[:100]}'")

    print("Computing TF-IDF...")
    try:
        tfidf_matrix, vectorizer = compute_tfidf(documents)
        print(f"TF-IDF Matrix shape: {tfidf_matrix.shape}")
    except Exception as e:
        print(f"Error computing TF-IDF: {e}")

if __name__ == "__main__":
    main()

import pymongo
from sklearn.feature_extraction.text import TfidfVectorizer

# MongoDB setup
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["document_db"]
collection = db["documents"]

def retrieve_documents():
    """Retrieve documents from MongoDB for TF-IDF computation."""
    documents_cursor = collection.find({}, {"_id": 0, "file_name": 1, "cleaned_text": 1})
    docs = []
    
    for doc in documents_cursor:
        text = doc.get("cleaned_text", "").strip()
        if text:
            docs.append(text)
        else:
            print(f"⚠️ Warning: Document '{doc.get('file_name', 'Unknown')}' has empty text.")
    
    return docs

def compute_tfidf(documents):
    """Compute TF-IDF matrix for the documents."""
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)
    return tfidf_matrix, vectorizer

def main():
    print("📂 Retrieving documents from MongoDB...")
    documents = retrieve_documents()
    
    if not documents:
        print("❌ No documents found in MongoDB or all documents are empty!")
        return

    print("📝 Computing TF-IDF...")
    try:
        tfidf_matrix, vectorizer = compute_tfidf(documents)
        print(f"✅ TF-IDF Matrix shape: {tfidf_matrix.shape}")
    except Exception as e:
        print(f"❌ Error computing TF-IDF: {e}")

if __name__ == "__main__":
    main()

