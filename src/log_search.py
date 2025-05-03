import pandas as pd
import os
from datetime import datetime

log_file = "search_logs.csv"

# Function to Log Search Queries
def log_search(query, results):
    logs = []
    for result in results:
        logs.append({
            "query": query,
            "retrieved_document": result["filename"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "similarity_score": result["similarity_score"]
        })

    df = pd.DataFrame(logs)

    if os.path.exists(log_file):
        df.to_csv(log_file, mode='a', header=False, index=False)
    else:
        df.to_csv(log_file, index=False)

    print(f"Logged {len(logs)} results for query: {query}")
