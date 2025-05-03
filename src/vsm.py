
# src/vsm.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compute_tfidf(texts, stop_words='english'):
    """
    Compute TF-IDF vectors for a list of text documents.
    Returns the TF-IDF matrix and the fitted vectorizer.
    """
    vectorizer = TfidfVectorizer(stop_words=stop_words)
    tfidf_matrix = vectorizer.fit_transform(texts)
    return tfidf_matrix, vectorizer

def compute_similarity(query, vectorizer, tfidf_matrix):
    """
    Compute cosine similarity between the query and each document in the TF-IDF matrix.
    Returns a similarity array.
    """
    query_vector = vectorizer.transform([query])
    similarities = cosine_similarity(query_vector, tfidf_matrix)[0]
    return similarities

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def compute_tfidf_matrix(texts):
    """
    Compute the TF-IDF matrix from a list of documents.

    Parameters:
        texts (list): List of document texts.

    Returns:
        tuple: TF-IDF matrix and vectorizer object.
    """
    if not texts:
        print("⚠️ No documents provided for TF-IDF computation.")
        return None, None

    try:
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(texts)
        print(f"✅ TF-IDF Matrix computed with shape: {tfidf_matrix.shape}")
        return tfidf_matrix, vectorizer
    except Exception as e:
        print(f"❌ Error computing TF-IDF: {e}")
        return None, None


def calculate_query_similarity(query, vectorizer, tfidf_matrix):
    """
    Calculate cosine similarity between the query and documents.

    Parameters:
        query (str): User query.
        vectorizer (TfidfVectorizer): Fitted TF-IDF vectorizer.
        tfidf_matrix (scipy.sparse matrix): TF-IDF matrix.

    Returns:
        list: Similarity scores.
    """
    if not query:
        print("⚠️ Empty query provided.")
        return []

    if vectorizer is None or tfidf_matrix is None:
        print("❌ Error: Vectorizer or TF-IDF matrix not provided.")
        return []

    try:
        query_vector = vectorizer.transform([query])
        similarity_scores = cosine_similarity(query_vector, tfidf_matrix).flatten()
        print("✅ Similarity scores computed.")
        return similarity_scores
    except Exception as e:
        print(f"❌ Error calculating similarity: {e}")
        return []
