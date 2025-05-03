
# src/evaluation.py

import math
import numpy as np

def precision_at_k(retrieved, relevant, k):
    """
    Compute Precision at k.
    retrieved: list of retrieved document IDs.
    relevant: set (or list) of relevant document IDs.
    """
    retrieved_at_k = retrieved[:k]
    if not retrieved_at_k:
        return 0.0
    num_relevant = sum(1 for doc in retrieved_at_k if doc in relevant)
    return num_relevant / k

def recall_at_k(retrieved, relevant, k):
    """
    Compute Recall at k.
    """
    retrieved_at_k = retrieved[:k]
    if not relevant:
        return 0.0
    num_relevant = sum(1 for doc in retrieved_at_k if doc in relevant)
    return num_relevant / len(relevant)

def f2_score(precision, recall, beta=2):
    """
    Compute the F2 score (F-beta with beta=2).
    """
    if precision == 0 and recall == 0:
        return 0.0
    return (1 + beta**2) * precision * recall / ((beta**2 * precision) + recall)

def dcg_at_k(relevances, k):
    """
    Compute Discounted Cumulative Gain at k.
    relevances: list of relevance scores for the ranked documents.
    """
    dcg = 0.0
    for i, rel in enumerate(relevances[:k]):
        dcg += (2**rel - 1) / math.log2(i + 2)
    return dcg

def ndcg_at_k(relevances, k):
    """
    Compute Normalized Discounted Cumulative Gain (NDCG) at k.
    """
    actual_dcg = dcg_at_k(relevances, k)
    ideal_dcg = dcg_at_k(sorted(relevances, reverse=True), k)
    if ideal_dcg == 0:
        return 0.0
    return actual_dcg / ideal_dcg

def average_precision(retrieved, relevant):
    """
    Compute Average Precision for a single query.
    """
    ap = 0.0
    num_relevant_found = 0
    for i, doc in enumerate(retrieved):
        if doc in relevant:
            num_relevant_found += 1
            ap += num_relevant_found / (i + 1)
    if len(relevant) == 0:
        return 0.0
    return ap / len(relevant)

def mean_average_precision(all_retrieved, all_relevant):
    """
    Compute Mean Average Precision (MAP) over multiple queries.
    """
    ap_scores = []
    for retrieved, relevant in zip(all_retrieved, all_relevant):
        ap_scores.append(average_precision(retrieved, relevant))
    return np.mean(ap_scores)

from pymongo import MongoClient
from rank_bm25 import BM25Okapi
import nltk
from nltk.tokenize import word_tokenize
import string
import numpy as np

# Ensure you have NLTK tokenizers
nltk.download('punkt')

# Connect to MongoDB
def connect_to_mongo():
    client = MongoClient("mongodb://localhost:27017/")  # Update if needed
    db = client["doc_db"]  # Ensure correct DB name
    collection = db["extracted_text"]  # Ensure correct collection name
    return collection

# Fetch documents from MongoDB
def fetch_documents():
    collection = connect_to_mongo()
    documents = list(collection.find({}, {"_id": 0, "filename": 1, "text": 1}))  # Fetch filenames & text
    return documents

# Preprocess text
def preprocess_text(text):
    text = text.lower().translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
    tokens = word_tokenize(text)  # Tokenize text
    return tokens

# Build BM25 Index
def build_bm25_index(documents):
    tokenized_corpus = [preprocess_text(doc["text"]) for doc in documents]
    bm25 = BM25Okapi(tokenized_corpus)
    return bm25, tokenized_corpus

# Search BM25
def search_bm25(query, bm25, documents, tokenized_corpus, top_n=5):
    query_tokens = preprocess_text(query)
    scores = bm25.get_scores(query_tokens)
    top_indices = np.argsort(scores)[::-1][:top_n]  # Get top N results
    results = [(documents[i]["filename"], scores[i]) for i in top_indices if scores[i] > 0]
    return results

if __name__ == "__main__":
    print("Fetching documents from MongoDB...")
    documents = fetch_documents()
    if not documents:
        print("No documents found in MongoDB!")
    else:
        print(f"Loaded {len(documents)} documents.")
        
        print("Building BM25 index...")
        bm25, tokenized_corpus = build_bm25_index(documents)
        
        query = input("Enter search query: ")
        results = search_bm25(query, bm25, documents, tokenized_corpus)
        
        if results:
            print("Top relevant documents:")
            for filename, score in results:
                print(f"{filename} (Score: {score:.4f})")
        else:
            print("No relevant documents found.")
                 

