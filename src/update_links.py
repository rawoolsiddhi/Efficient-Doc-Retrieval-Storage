# import pymongo

# client = pymongo.MongoClient("mongodb://localhost:27017/")
# db = client["document_database"]
# collection = db["documents"]

# def get_drive_link(file_name):
#     """Extract ID from filename and generate Drive link."""
#     file_id = file_name.split("_")[0]  # Assuming filename like 12345_file.pdf
#     return f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"

# # Fetch all documents without pdf_link
# documents = collection.find({"pdf_link": {"$exists": False}})

# updated_count = 0

# for doc in documents:
#     file_name = doc["file_name"]
#     drive_link = get_drive_link(file_name)

#     collection.update_one(
#         {"_id": doc["_id"]},
#         {"$set": {"pdf_link": drive_link}}
#     )
#     updated_count += 1
#     print(f"🔗 Added link for: {file_name}")

# print(f"🎯 {updated_count} Documents Updated with Drive Links!")
