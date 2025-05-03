
import os

# Google Drive API Credentials - file path for the client_secrets.json
CLIENT_SECRETS_FILE = "src/client_secrets.json"  # Update the path if necessary
MONGO_URI = "mongodb://localhost:27017/"  # Replace with your MongoDB URI if different
DATABASE_NAME = "document_database"
COLLECTION_NAME = "documents"

# Google Drive Folder ID - You can get it from the URL of the folder in Google Drive
DRIVE_FOLDER_ID = "1kpVBUu8FXn90Udsr-UOpzoWKVeV2zyKW"  # Replace with your Google Drive folder ID

# MongoDB Configuration
MONGO_URI = "mongodb://localhost:27017"  # Your MongoDB connection string
DATABASE_NAME = "document_db"           # Your Database Name
COLLECTION_NAME = "documents"           # Your Collection Name

# TF-IDF Vectorizer Configuration
MAX_FEATURES = 10000  # Maximum number of features for TF-IDF
STOPWORDS_LANG = "english"  # Language for stopwords removal

# Clustering Parameters
CLUSTER_THRESHOLD = 0.8  # Cosine Similarity threshold for clustering

# Other Settings
DEBUG = True  # Set to True for debugging logs

