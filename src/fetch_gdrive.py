<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 5ec07714bff833219f57c48f2792d6e0f26abf96
import os
import pickle
import io
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# Authenticate and download files
def authenticate_and_download():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
    results = service.files().list(q="mimeType='application/pdf'", pageSize=10).execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        for item in items:
            print(f"Downloading: {item['name']}")
            request = service.files().get_media(fileId=item['id'])
            fh = io.FileIO(f"data/{item['name']}", 'wb')
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
            print(f"Downloaded: {item['name']}")

if __name__ == '__main__':
    authenticate_and_download()
<<<<<<< HEAD
=======
import os
import pickle
import io
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pymongo

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
DATA_FOLDER = "data"
RECORD_FILE = "downloaded_files.txt"
 
# MongoDB setup
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["document_database"]
collection = db["documents"]

# Authenticate Google Drive
def authenticate():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)

# Load previously downloaded file records
def load_downloaded_files():
    if os.path.exists(RECORD_FILE):
        with open(RECORD_FILE, 'r') as f:
            return set(f.read().splitlines())
    return set()

# Save new downloads to record
def save_downloaded_file(file_name):
    with open(RECORD_FILE, 'a') as f:
        f.write(file_name + "\n")

# ✅ Fixed: Use "pdf_link" to match what's expected by retrieve_documents()
def store_in_mongo(file_name, file_id, file_link):
    document = {
        "file_name": file_name,
        "pdf_link": file_link,
        "file_type": file_name.split('.')[-1],
    }
    collection.insert_one(document)
    print(f"Stored {file_name} with link {file_link} in MongoDB.")

# Download new PDFs only
def download_new_pdfs():
    service = authenticate()
    query = "mimeType='application/pdf'"
    page_token = None

    os.makedirs(DATA_FOLDER, exist_ok=True)
    downloaded_files = load_downloaded_files()

    while True:
        results = service.files().list(q=query, pageSize=100, pageToken=page_token).execute()
        items = results.get('files', [])

        if not items:
            print('No new PDF files found.')
            break

        for item in items:
            file_name = item['name']
            file_id = item['id']
            file_path = os.path.join(DATA_FOLDER, file_name)

            if file_name in downloaded_files:
                print(f"Skipping (Already Downloaded): {file_name}")
                continue

            print(f"Downloading: {file_name}")
            request = service.files().get_media(fileId=file_id)
            with io.FileIO(file_path, 'wb') as fh:
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                    print(f"Download progress: {int(status.progress() * 100)}%")
            print(f"Downloaded: {file_name}")

            save_downloaded_file(file_name)

            file_link = f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"
            store_in_mongo(file_name, file_id, file_link)

        page_token = results.get('nextPageToken')
        if not page_token:
            break

if __name__ == '__main__':
    download_new_pdfs()
>>>>>>> c51ece5 (Clean start: add source, app, and essential files only)
=======
>>>>>>> 5ec07714bff833219f57c48f2792d6e0f26abf96
