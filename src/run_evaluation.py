import logging
from evaluation import precision_at_k, recall_at_k, f2_score, ndcg_at_k, average_precision, mean_average_precision
from vsm_retrieval import retrieve_vsm_results
from bm25_retrieval import retrieve_bm25_results

# Set up logging to file and console
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler("evaluation.log", mode='w'),
        logging.StreamHandler()
    ]
)

# --- Example Ground Truth and Retrieved Results ---
# For real evaluation, replace these with your own ground truth data.
# Ground truth: mapping of each query to the set of relevant document filenames.
ground_truth = {
    "machine learning": {"ML&&DL.pdf", "s42979-021-00592-x.pdf", "deepL.pdf"},
    "data mining": {"Research_Paper_On_Artificial_Intelligence_And_Its.pdf", "Paper_11-Internet_of_Things_IOT_Research_Challenges.pdf"}
}

# List of test queries
queries = list(ground_truth.keys())

# Retrieve results from both retrieval methods for each query
vsm_results = {}
bm25_results = {}

for query in queries:
    # Call your retrieval functions
    vsm_results[query] = retrieve_vsm_results(query)
    bm25_results[query] = retrieve_bm25_results(query)

# Evaluation for each query
all_vsm_results = []
all_bm25_results = []
all_relevant = []

logging.info("Evaluation Metrics:")
for query in queries:
    relevant = ground_truth[query]
    vsm_retrieved = vsm_results[query]
    bm25_retrieved = bm25_results[query]
    
    logging.info(f"Query: {query}")
    
    # Compute metrics at cutoff k = 5
    vsm_prec = precision_at_k(vsm_retrieved, relevant, k=5)
    vsm_rec = recall_at_k(vsm_retrieved, relevant, k=5)
    vsm_f2 = f2_score(vsm_prec, vsm_rec, beta=2)
    # For NDCG, assume binary relevance (1 for relevant, 0 for non-relevant)
    vsm_relevances = [1 if doc in relevant else 0 for doc in vsm_retrieved]
    vsm_ndcg = ndcg_at_k(vsm_relevances, k=5)
    vsm_ap = average_precision(vsm_retrieved, relevant)
    
    logging.info("Vector Space Retrieval:")
    logging.info(f"  Precision@5: {vsm_prec:.4f}")
    logging.info(f"  Recall@5:    {vsm_rec:.4f}")
    logging.info(f"  F2 Score:    {vsm_f2:.4f}")
    logging.info(f"  NDCG@5:      {vsm_ndcg:.4f}")
    logging.info(f"  Average Precision: {vsm_ap:.4f}")
    
    bm25_prec = precision_at_k(bm25_retrieved, relevant, k=5)
    bm25_rec = recall_at_k(bm25_retrieved, relevant, k=5)
    bm25_f2 = f2_score(bm25_prec, bm25_rec, beta=2)
    bm25_relevances = [1 if doc in relevant else 0 for doc in bm25_retrieved]
    bm25_ndcg = ndcg_at_k(bm25_relevances, k=5)
    bm25_ap = average_precision(bm25_retrieved, relevant)
    
    logging.info("BM25 Retrieval:")
    logging.info(f"  Precision@5: {bm25_prec:.4f}")
    logging.info(f"  Recall@5:    {bm25_rec:.4f}")
    logging.info(f"  F2 Score:    {bm25_f2:.4f}")
    logging.info(f"  NDCG@5:      {bm25_ndcg:.4f}")
    logging.info(f"  Average Precision: {bm25_ap:.4f}")
    logging.info("----------")
    
    all_vsm_results.append(vsm_retrieved)
    all_bm25_results.append(bm25_retrieved)
    all_relevant.append(relevant)

vsm_map = mean_average_precision(all_vsm_results, all_relevant)
bm25_map = mean_average_precision(all_bm25_results, all_relevant)
logging.info(f"Mean Average Precision (VSM): {vsm_map:.4f}")
logging.info(f"Mean Average Precision (BM25): {bm25_map:.4f}")
