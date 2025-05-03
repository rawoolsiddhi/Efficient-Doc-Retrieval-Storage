
# src/clustering.py
import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster

def perform_clustering(tfidf_matrix, threshold=0.5):
    """
    Perform single-link clustering on the TF-IDF matrix.
    Returns an array of cluster labels.
    """
    dense_matrix = tfidf_matrix.toarray()
    if len(dense_matrix) > 1:
        # Use cosine distance: distance = 1 - similarity
        Z = linkage(dense_matrix, method='single', metric='cosine')
        clusters = fcluster(Z, t=threshold, criterion='distance')
    else:
        clusters = np.array([1])
    return clusters

import numpy as np
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import linkage, fcluster

def perform_clustering(tfidf_matrix, threshold=0.5):
    """
    Perform single-link hierarchical clustering on the TF-IDF matrix using cosine distance.

    Parameters:
        tfidf_matrix (scipy.sparse matrix or numpy.ndarray): TF-IDF matrix.
        threshold (float): Distance threshold for forming clusters.

    Returns:
        np.ndarray: Cluster labels for each document.
    """
    if tfidf_matrix.shape[0] == 0:
        print("⚠️ Warning: Empty TF-IDF matrix. Returning empty clusters.")
        return np.array([])

    if tfidf_matrix.shape[0] == 1:
        print("⚠️ Only one document present. Assigning it to a single cluster.")
        return np.array([1])

    # Convert sparse matrix to dense for distance computation
    dense_matrix = tfidf_matrix.todense() if hasattr(tfidf_matrix, "todense") else tfidf_matrix

    # Compute cosine distance (1 - cosine similarity)
    cosine_distances = pdist(dense_matrix, metric="cosine")

    # Perform hierarchical clustering
    Z = linkage(cosine_distances, method="single")

    # Assign cluster labels
    clusters = fcluster(Z, t=threshold, criterion="distance")
    
    return clusters

