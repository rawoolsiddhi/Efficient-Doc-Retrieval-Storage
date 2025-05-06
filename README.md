# 📄 Efficient Document Storage & Retrieval with VSM + Clustering

An document retrieval system that leverages **Vector Space Model (VSM)** and **Efficient Clustering** to extract, store, rank, and retrieve documents  Designed to serve research and enterprise needs for smarter information access.

---

## 📘 IEEE Publication

This project is based on our IEEE-published research paper:

> 📝 **Title**: Document Storage and Retrieval with Efficient Clustering Using the Vector Space Model  
> 🔗 **IEEE Xplore**: [https://ieeexplore.ieee.org/abstract/document/10940682](https://ieeexplore.ieee.org/abstract/document/10940682)

📌 The model introduces a hybrid approach combining **TF-IDF-based retrieval** with **Single-Link Clustering**, improving accuracy, relevance, and ranking.



## 🌟 Features

- 📥 **Text Extraction** (using PyMuPDF)
- ✨ **Preprocessing**: Tokenization, Stopword Removal, Normalization
- 📊 **TF-IDF Vectorization**: Classic Vector Space Model
- 🔗 **Single-Link Clustering** for smarter group-based ranking
- 🧠 **Hybrid Retrieval** combining VSM + clustering similarity
- 🔎 **Streamlit UI** for fast search and document preview
- 🧾 **MongoDB** backend for storing documents and search logs
- 📈 Built-in **Evaluation Metrics** (Precision, Recall, MAP, NDCG, F2)

---

## 📁 Project Structure


```bash
Efficient-Doc-Retrieval-Storage/
├── app.py                         # Streamlit app interface
├── requirements.txt
├── README.md
├── .gitignore
├── LICENSE

├── ground_truth/
│   └── ground_truth.csv          # CSV for ground-truth relevance

├── mongodb_data/                 # MongoDB dump (not included in GitHub)

├── src/
│   ├── __init__.py
│   ├── BM25.py                   # BM25 scorer (optional)
│   ├── clustering.py             # Single-link clustering logic
│   ├── compute_tfidf.py          # TF-IDF vector computation
│   ├── config.py                 # Global configuration variables
│   ├── evaluation.py             # Precision, Recall, MAP, NDCG etc.
│   ├── extract_text.py           # Extract text from documents
│   ├── fetch_gdrive.py           # (Optional) fetch PDFs from Google Drive
│   ├── log_search.py             # Log user queries
│   ├── preprocess_text.py        # Clean and normalize document text
│   ├── query_log.py              # Access and analyze search history
│   ├── query_mongo.py            # Search MongoDB for past queries
│   ├── retrieve_documents.py     # Main hybrid retrieval logic
│   ├── run_evaluation.py         # CLI script for evaluation
│   ├── store_mongo.py            # Insert documents into MongoDB
│   ├── update_links.py           # Fix or update download links
│   ├── update_mongo.py           # Modify or refresh DB content
│   ├── vsm.py                    # Vector Space Model ranking
│   ├── token.pickle              # OAuth token for GDrive
│   └── downloaded_files.txt

│   └── data/                     # Folder for raw/extracted files

├── venv/                         # Virtual environment.

```


## ⚙️ Installation & Setup

To run this project locally, follow these steps:

# 1. Clone the repository
git clone https://github.com/your-username/Efficient-Doc-Retrieval-Storage.git
cd Efficient-Doc-Retrieval-Storage

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
 On Windows:
venv\Scripts\activate
  On Mac/Linux:
source venv/bin/activate

# 4. Install required Python packages
pip install -r requirements.txt

# 5. Run the Streamlit app
streamlit run app.py


To run this project locally, follow these steps:

# 1. Clone the repository
git clone https://github.com/your-username/Efficient-Doc-Retrieval-Storage.git
cd Efficient-Doc-Retrieval-Storage

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
  On Windows:
  venv\Scripts\activate
   
  On Mac/Linux:
  source venv/bin/activate

# 4. Install required Python packages
pip install -r requirements.txt

# 5. Run the Streamlit app
streamlit run app.py



## Evaluation Metrics

| Metric             | Hybrid Model<br>(VSM + Clustering) | VSM Only    | BM25 (Optional) |
| ------------------ | ---------------------------------- | ----------- | --------------- |
| **Precision**      | 0.91                               | 0.83        | 0.77            |
| **Recall**         | 0.94                               | 0.87        | 0.81            |
| **F2 Score**       | 0.93                               | 0.85        | 0.79            |
| **NDCG**           | 0.92                               | 0.82        | 0.78            |
| **MAP**            | 0.89                               | 0.80        | 0.75            |
| **Accuracy Range** | 0.88 - 0.96                        | 0.85 - 0.95 | 0.82 - 0.91     |


## UI

![image](https://github.com/user-attachments/assets/0ca92f6c-225d-478c-a1cc-857a8a1bbe5b)


##  How It Works

1. Text Extraction: Extract content from PDFs using PyMuPDF.

2. Preprocessing: Clean, normalize, and tokenize text.

3. TF-IDF Generation: Compute vectors using scikit-learn.

4. Clustering: Apply Single-Link Clustering based on cosine distances.

5. Hybrid Retrieval: Combine VSM ranking and cluster similarity.

6. Search Logging: Store user queries and retrieval metadata.

7. Ranking: Return documents with highest combined relevance.

##  License
This project is released under the MIT License.

