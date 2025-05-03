from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client.document_db
search_logs = db.search_logs

def log_search(query):
    if query.strip():
        existing_query = search_logs.find_one({"query": query})

        if existing_query:
            search_logs.update_one({"query": query}, {"$inc": {"count": 1}})
        else:
            search_logs.insert_one({{"query": query, "count": 1}})
