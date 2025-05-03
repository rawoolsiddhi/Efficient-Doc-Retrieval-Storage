<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 5ec07714bff833219f57c48f2792d6e0f26abf96
import os
import pymongo
import pdfplumber

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["doc_db"]
collection = db["extracted_text"]

pdf_folder = "data"  # Folder where new PDFs are located

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def save_to_mongo(pdf_path, text):
    file_name = os.path.basename(pdf_path)
    document = {
        "file_name": file_name,
        "extracted_text": text
    }
    collection.update_one({"file_name": file_name}, {"$set": document}, upsert=True)
    print(f"Saving {file_name} to MongoDB...")

def process_new_pdfs():
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            # Check if this file already exists in MongoDB
            if collection.find_one({"file_name": filename}):
                print(f"{filename} already exists in MongoDB. Skipping...")
            else:
                print(f"Extracting text from {filename}...")
                extracted_text = extract_text_from_pdf(pdf_path)
                save_to_mongo(pdf_path, extracted_text)

if __name__ == "__main__":
    process_new_pdfs()
    print("Text extraction and saving to MongoDB complete.")
<<<<<<< HEAD
=======
import os
import pymongo
import pdfplumber
import pytesseract
from PIL import Image
from pdf2image import convert_from_path

# MongoDB Setup
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["document_database"]
collection = db["documents"]

pdf_folder = "src/data"  # Correct Path

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
            if not text.strip():
                print(f"🧠 OCR Applied for {pdf_path}")
                return extract_text_with_ocr(pdf_path)  # Apply OCR if no text found
            return text.strip()
    except Exception as e:
        print(f"❌ Error extracting text from {pdf_path}: {e}")
        return ""

def extract_text_with_ocr(pdf_path):
    """Extract text using OCR for scanned PDFs."""
    try:
        images = convert_from_path(pdf_path)
        full_text = ""
        for img in images:
            text = pytesseract.image_to_string(img)
            full_text += text + "\n"
        return full_text.strip()
    except Exception as e:
        print(f"❌ OCR Error: {e}")
        return ""

def process_new_pdfs():
    """Check for new PDFs and update MongoDB."""
    if not os.path.exists(pdf_folder):
        print(f"❌ Error: Directory '{pdf_folder}' does not exist!")
        return

    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)

            # Check if file already exists in MongoDB
            if collection.find_one({"file_name": filename}):
                print(f"⚠️ {filename} already exists in MongoDB. Skipping...")
                continue

            print(f"📄 Extracting text from {filename}...")
            extracted_text = extract_text_from_pdf(pdf_path)
            
            if extracted_text:
                document = {
                    "file_name": filename,
                    "extracted_text": extracted_text
                }
                collection.insert_one(document)
                print(f"✅ Saved {filename} to MongoDB.")
            else:
                print(f"⚠️ No text extracted from {filename}. Skipping.")

if __name__ == "__main__":
    process_new_pdfs()
    print("🎯 Text extraction and update complete.")
>>>>>>> c51ece5 (Clean start: add source, app, and essential files only)
=======
>>>>>>> 5ec07714bff833219f57c48f2792d6e0f26abf96
