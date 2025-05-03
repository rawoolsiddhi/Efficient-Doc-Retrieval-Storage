
import os
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["document_database"]
collection = db["documents"]

input_dir = "extracted_text"

for filename in os.listdir(input_dir):
    if filename.endswith(".txt"):
        with open(os.path.join(input_dir, filename), "r", encoding="utf-8") as f:
            content = f.read()

        doc = {
            "filename": filename,
            "content": content
        }
        collection.insert_one(doc)
        print(f"Stored: {filename}")

print("✅ All documents stored in MongoDB!")
import os
import pymongo

# MongoDB setup
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["document_database"]  # Use same DB name across all scripts
collection = db["documents"]

# Correct input directory path inside data folder
input_dir = os.path.join(os.path.dirname(__file__), "data")

if not os.path.exists(input_dir):
    print(f"❌ Error: Directory '{input_dir}' does not exist!")
    exit()

# Process each text file in the directory
for filename in os.listdir(input_dir):
    if filename.endswith(".txt"):
        file_path = os.path.join(input_dir, filename)

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()

        if not content:
            print(f"⚠️ Skipping empty file: {filename}")
            continue

        doc = {
            "filename": filename,
            "extracted_text": content
        }

        try:
            collection.insert_one(doc)
            print(f"✅ Stored: {filename}")
        except Exception as e:
            print(f"❌ Error storing {filename}: {e}")

print("🎉 All valid documents stored in MongoDB!")

