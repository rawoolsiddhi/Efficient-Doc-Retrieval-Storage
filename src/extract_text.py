<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 5ec07714bff833219f57c48f2792d6e0f26abf96
import os
import pdfplumber
import pymongo

# MongoDB setup
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["document_db"]
collection = db["documents"]

# Folder where PDFs are stored
pdf_folder = "data"  # Ensure your PDFs are in the "data" folder

def extract_text_from_pdf(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return text.strip()
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return ""

def process_pdfs():
    for filename in os.listdir(pdf_folder):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            print(f"Extracting text from {filename}...")
            extracted_text = extract_text_from_pdf(pdf_path)
            if extracted_text:
                document = {
                    "filename": filename,       # Use "filename" as the field name
                    "extracted_text": extracted_text
                    # Optionally, you can add "pdf_link": "<link>" if available.
                }
                collection.insert_one(document)
                print(f"Saved {filename} to MongoDB.")
            else:
                print(f"No text extracted from {filename}. Skipping.")

if __name__ == "__main__":
    process_pdfs()
    print("Text extraction and saving to MongoDB complete.")
<<<<<<< HEAD
=======
import pymongo
import PyPDF2
import requests
from io import BytesIO

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["document_database"]
collection = db["documents"]

# Function to extract text from PDF link
def extract_text_from_pdf(pdf_link):
    try:
        # Get the PDF file from the provided link
        response = requests.get(pdf_link)
        file = BytesIO(response.content)
        
        # Read the PDF file
        reader = PyPDF2.PdfReader(file)
        text = ""
        
        # Extract text from each page of the PDF
        for page in reader.pages:
            text += page.extract_text()
        
        return text
    except Exception as e:
        return str(e)

# Function to update documents in the collection with extracted text
def update_documents_with_extracted_text():
    # Iterate over all documents in the collection
    for document in collection.find():
        pdf_link = document.get("pdf_link")
        
        if pdf_link:
            print(f"Extracting text from {document['file_name']}...")
            
            # Extract text from the PDF
            extracted_text = extract_text_from_pdf(pdf_link)
            
            # Update the document with the extracted text
            collection.update_one(
                {"_id": document["_id"]},
                {"$set": {"extracted_text": extracted_text}}
            )
            print(f"Text extracted and updated for {document['file_name']}")
        else:
            print(f"No PDF link found for {document['file_name']}")

# Run the function to update documents with extracted text
update_documents_with_extracted_text()
>>>>>>> c51ece5 (Clean start: add source, app, and essential files only)
=======
>>>>>>> 5ec07714bff833219f57c48f2792d6e0f26abf96
