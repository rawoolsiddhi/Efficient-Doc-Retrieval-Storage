
import pymongo
import numpy as np
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.cluster.hierarchy import linkage, fcluster

# Ensure required NLTK resources are downloaded
nltk.download("punkt")
nltk.download("stopwords")

def preprocess(text):
    """
    Preprocess text: convert to lowercase, remove non-alphanumeric characters,
    tokenize, and remove English stopwords.
    """
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    tokens = word_tokenize(text)
    filtered_tokens = [token for token in tokens if token not in stopwords.words("english")]
    return " ".join(filtered_tokens)

def retrieve_documents():
    """
    Retrieve documents from MongoDB.
    Expects each document to have:
      - filename         (the PDF's name, stored during extraction)
      - preprocessed_text (if available) or extracted_text (or text)
      - pdf_link         (optional)
    Only documents with non-empty text are returned.
    """
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["document_db"]  # Adjust to your database name
    collection = db["documents"]  # Adjust to your collection name
    
    # Try to fetch multiple possible text fields
    docs = list(collection.find({}, {
        "_id": 0,
        "filename": 1, 
        "preprocessed_text": 1, 
        "extracted_text": 1,
        "text": 1,
        "pdf_link": 1
    }))
    
    file_names = []
    texts = []
    pdf_links = []
    for doc in docs:
        # Use "preprocessed_text" if available; otherwise, check "extracted_text" or "text"
        text = doc.get("preprocessed_text") or doc.get("extracted_text") or doc.get("text", "")
        text = text.strip()
        if text:
            file_names.append(doc.get("filename", "Unknown"))
            pdf_links.append(doc.get("pdf_link", "N/A"))
            texts.append(text)
        else:
            print(f"Document '{doc.get('filename', 'Unknown')}' has empty text. Skipping...")
    return file_names, texts, pdf_links

def compute_tfidf(texts):
    """
    Compute TF-IDF vectors for the provided texts.
    """
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(texts)
    return tfidf_matrix, vectorizer

def perform_clustering(tfidf_matrix, threshold=0.5):
    """
    Perform single-link clustering on the TF-IDF matrix.
    """
    dense_matrix = tfidf_matrix.toarray()
    if len(dense_matrix) > 1:
        Z = linkage(dense_matrix, method="single", metric="cosine")
        clusters = fcluster(Z, t=threshold, criterion="distance")
    else:
        clusters = np.array([1])
    return clusters

def main():
    query = input("Enter your query: ")
    preprocessed_query = preprocess(query)
    
    file_names, texts, pdf_links = retrieve_documents()
    if not texts:
        print("No documents with non-empty text found in MongoDB!")
        return
    
    # Debug: print details for each retrieved document
    for i, t in enumerate(texts):
        print(f"Document {i} ('{file_names[i]}'): Length = {len(t)}; Sample = '{t[:100]}'")
    
    print("Computing TF-IDF...")
    try:
        tfidf_matrix, vectorizer = compute_tfidf(texts)
        print(f"TF-IDF Matrix shape: {tfidf_matrix.shape}")
    except Exception as e:
        print(f"Error computing TF-IDF: {e}")
        return

    # Transform the preprocessed query into a TF-IDF vector
    query_vector = vectorizer.transform([preprocessed_query])
    similarities = cosine_similarity(query_vector, tfidf_matrix)[0]
    
    # Perform clustering on the document vectors
    clusters = perform_clustering(tfidf_matrix, threshold=0.5)
    
    # Combine the results
    results = []
    for i in range(len(file_names)):
        results.append({
            "file_name": file_names[i],
            "similarity": similarities[i],
            "cluster": int(clusters[i]),
            "pdf_link": pdf_links[i]
        })
    
    # Sort results by similarity in descending order
    results_sorted = sorted(results, key=lambda x: x["similarity"], reverse=True)
    
    print("\nTop 5 relevant documents:")
    for res in results_sorted[:5]:
        print(f"File: {res['file_name']}, Similarity: {res['similarity']:.4f}, Cluster: {res['cluster']}, Link: {res['pdf_link']}")

if __name__ == "__main__":
    main()

import os
import base64
from pymongo import MongoClient
from src.query_mongo import fetch_documents
from src.vsm import compute_tfidf_matrix, calculate_query_similarity
from src.clustering import perform_clustering

# MongoDB Client Setup
client = MongoClient("mongodb://localhost:27017/")
db = client["document_db"]
search_logs = db["search_logs"]

def get_top_searches(limit=5):
    top_queries = search_logs.find().sort("count", -1).limit(limit)
    return [doc["query"] for doc in top_queries]

def log_query(query, relevant_documents_count=0, retrieved_documents=None):
    existing_query = search_logs.find_one({"query": query})
    if existing_query:
        search_logs.update_one(
            {"query": query},
            {"$inc": {"count": 1},
             "$set": {
                 "relevant_documents_count": relevant_documents_count,
                 "retrieved_documents": retrieved_documents
             }}
        )
    else:
        search_logs.insert_one({
            "query": query,
            "count": 1,
            "relevant_documents_count": relevant_documents_count,
            "retrieved_documents": retrieved_documents
        })

def display_pdf(pdf_path):
    with open(pdf_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="500" type="application/pdf"></iframe>'
    return pdf_display

def retrieve_documents(query):
    file_names, texts, _ = fetch_documents(query)

    if not texts:
        return [{"message": "No documents found in MongoDB"}]

    tfidf_matrix, vectorizer = compute_tfidf_matrix(texts)
    similarity_scores = calculate_query_similarity(query, vectorizer, tfidf_matrix)

    if similarity_scores is None or similarity_scores.size == 0:
        return [{"message": "No relevant documents found"}]

    cluster_labels = perform_clustering(tfidf_matrix)

    relevant_documents = [
        file_names[i] for i in range(len(file_names)) if similarity_scores[i] > 0.5
    ]
    relevant_count = len(relevant_documents)

    # Look for the PDF in src/data/
    results = []
    for i in range(len(file_names)):
        file_name = file_names[i]
        relative_pdf_path = f"src/data/{file_name}"
        pdf_path = relative_pdf_path if os.path.exists(relative_pdf_path) else "#"
        
        results.append({
            "filename": file_name,
            "pdf_link": pdf_path,  # Returning path for inline preview or download
            "similarity_score": round(similarity_scores[i], 2),
            "cluster": int(cluster_labels[i])
        })

    retrieved_filenames = [res["filename"] for res in results]
    log_query(query, relevant_count, retrieved_filenames)

    return sorted(results, key=lambda x: x["similarity_score"], reverse=True)[:10]
