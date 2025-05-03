# Document Storage and Retrieval with Efficient Clustering Using the Vector Space Model


## Problem Statement

In today's digital age, organizations accumulate vast amounts of unstructured documents such as PDFs, research papers, and reports. Traditional retrieval systems often struggle with efficiently indexing, storing, and accurately retrieving relevant documents from these large datasets. Additionally, the variability in document structure and content complicates ranking and clustering of search results, making it challenging for users to quickly access the precise information they need.

This project addresses these challenges by developing a system that not only stores and indexes unstructured documents but also employs advanced retrieval techniques. The system leverages both a vector space model with TF-IDF and cosine similarity—enhanced with single-link clustering—and a probabilistic BM25 ranking method to improve the relevance and efficiency of document retrieval. An evaluation framework is provided to measure system performance using standard IR metrics such as Precision, Recall, F2 Score, NDCG, and MAP.

## Project Overview

**Efficient Document Storage and Retrieval with Clustering-Based Ranking** is designed to:

- **Extract and Preprocess Documents:**  
  Automatically extract text from PDFs and other documents, then preprocess the text (e.g., tokenization, stop word removal) for further analysis.

- **Store Data Effectively:**  
  Store the extracted text and metadata in a MongoDB database, ensuring efficient management of large document collections.

- **Implement Advanced Retrieval Methods:**  
  Utilize two main retrieval approaches:
  - **Vector Space Model with Clustering:**  
    Compute TF-IDF vectors, use cosine similarity for ranking, and apply single-link clustering to group similar documents.
  - **BM25:**  
    Apply the BM25 ranking algorithm for probabilistic retrieval.
  
- **Evaluate Retrieval Performance:**  
  Use standard Information Retrieval (IR) metrics—Precision, Recall, F2 Score, NDCG, and MAP—to assess and compare the performance of the retrieval methods.

- **Modular and Scalable Design:**  
  The system is built using a modular architecture, making it easy to integrate new retrieval models, update preprocessing routines, and expand the dataset.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/rawoolsiddhi/Efficient-Doc-Retrieval-Storage.git
   cd Efficient-Doc-Retrieval-Storage

2. Create and Activate a Virtual Environment:
   
   python -m venv venvv
   venvv\Scripts\activate   # On Windows
   # source venvv/bin/activate  # On macOS/Linux

3. Install Dependencies:

    pip install -r requirements.txt

4. Set Up MongoDB:
Ensure you have MongoDB installed and running. The system uses a local MongoDB instance by default.

5. Google Drive API (Optional):
   If you plan to extract documents from Google Drive, configure your Google API credentials 
   (e.g., client_secrets.json) locally. This file is excluded from version control.


*Usage

1. Document Extraction & Storage
   Extract text from PDFs and store them in MongoDB by running:
   python src/extract_text.py
2. Retrieval
   - For retrieval using the vector space model (TF-IDF + cosine similarity with single-link 
   clustering):

     python src/retrieve_documents.py

   - For retrieval using BM25:

     python src/BM25.py

* Evaluation
---




