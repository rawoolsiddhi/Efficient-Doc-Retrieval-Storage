<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 5ec07714bff833219f57c48f2792d6e0f26abf96
import math
import numpy as np

def precision_at_k(retrieved, relevant, k):
    """
    Compute Precision at k.
    
    retrieved: list of retrieved document IDs in ranked order.
    relevant: set (or list) of relevant document IDs.
    k: cutoff rank.
    """
    retrieved_at_k = retrieved[:k]
    if not retrieved_at_k:
        return 0.0
    num_relevant = sum(1 for doc in retrieved_at_k if doc in relevant)
    return num_relevant / k

def recall_at_k(retrieved, relevant, k):
    """
    Compute Recall at k.
    
    retrieved: list of retrieved document IDs.
    relevant: set (or list) of relevant document IDs.
    k: cutoff rank.
    """
    retrieved_at_k = retrieved[:k]
    if not relevant:
        return 0.0
    num_relevant = sum(1 for doc in retrieved_at_k if doc in relevant)
    return num_relevant / len(relevant)

def f2_score(precision, recall, beta=2):
    """
    Compute the F2 score.
    
    beta=2 weights recall more than precision.
    """
    if precision == 0 and recall == 0:
        return 0.0
    return (1 + beta**2) * precision * recall / ((beta**2 * precision) + recall)

def dcg_at_k(relevances, k):
    """
    Compute Discounted Cumulative Gain at k.
    
    relevances: list of relevance scores for the ranked documents (in order).
    """
    dcg = 0.0
    for i, rel in enumerate(relevances[:k]):
        dcg += (2**rel - 1) / math.log2(i + 2)
    return dcg

def ndcg_at_k(relevances, k):
    """
    Compute Normalized Discounted Cumulative Gain (NDCG) at k.
    
    relevances: list of actual relevance scores for retrieved documents.
    """
    actual_dcg = dcg_at_k(relevances, k)
    ideal_dcg = dcg_at_k(sorted(relevances, reverse=True), k)
    if ideal_dcg == 0:
        return 0.0
    return actual_dcg / ideal_dcg

def average_precision(retrieved, relevant):
    """
    Compute Average Precision for a single query.
    
    retrieved: list of retrieved document IDs in ranked order.
    relevant: set (or list) of relevant document IDs.
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
    
    all_retrieved: list of lists, where each inner list is the retrieved document IDs for a query.
    all_relevant: list of sets/lists, where each element is the set of relevant document IDs for the corresponding query.
    """
    ap_scores = []
    for retrieved, relevant in zip(all_retrieved, all_relevant):
        ap_scores.append(average_precision(retrieved, relevant))
    return np.mean(ap_scores)
<<<<<<< HEAD
=======
import pandas as pd
from sklearn.metrics import precision_score
from pymongo import MongoClient

# Function to load logs from MongoDB
def load_logs_from_mongo():
    client = MongoClient("mongodb://localhost:27017/")  # Update URI if needed
    db = client["document_db"]  # Replace with your database name
    collection = db["search_logs"]  # Replace with your collection name
    logs = pd.DataFrame(list(collection.find()))
    return logs

# Evaluation function
def evaluate():
    logs = load_logs_from_mongo()

    print("Logs Columns:", logs.columns)
    print("First few rows of logs:")
    print(logs.head())

    ground_truth_file = "C:/Users/Hp/Desktop/Efficient-Doc-Retrieval-Storage/ground_truth/ground_truth.csv"
    ground_truth_df = pd.read_csv(ground_truth_file)

    sample_queries = ground_truth_df["query"].unique()

    for query in sample_queries:
        print(f"\nEvaluating query: {query}")

        # 1. Get retrieved documents from Mongo logs
        query_logs = logs[logs["query"] == query]
        if query_logs.empty or "retrieved_documents" not in query_logs.columns:
            print("No retrieved documents found in logs for this query.")
            continue

        retrieved_documents = query_logs.iloc[0]["retrieved_documents"]
        if not isinstance(retrieved_documents, list):
            print("retrieved_documents is not a list.")
            continue

        # 2. Get ground truth for the same query
        gt_subset = ground_truth_df[ground_truth_df["query"] == query]

        # Create a dict for relevance: filename -> 0/1
        relevance_dict = dict(zip(gt_subset["filename"], gt_subset["relevance"]))

        # 3. Prepare true/pred labels
        y_true = []
        y_pred = []

        for doc in retrieved_documents:
            rel = relevance_dict.get(doc, 0)  # default 0 if not found
            y_true.append(rel)
            y_pred.append(1)  # Retrieved => predicted relevant

        if not y_true:
            print("No overlap with ground truth — skipping.")
            continue

        precision = precision_score(y_true, y_pred, average='binary', zero_division=0)
        print(f"Retrieved: {retrieved_documents}")
        print(f"Ground Truth Matches: {sum(y_true)} / {len(retrieved_documents)}")
        print(f"Precision for '{query}': {precision:.2f}")

if __name__ == "__main__":
    evaluate()
>>>>>>> c51ece5 (Clean start: add source, app, and essential files only)
=======
>>>>>>> 5ec07714bff833219f57c48f2792d6e0f26abf96
