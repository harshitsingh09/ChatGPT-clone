# file_handler.py
import pandas as pd
import fitz  # PyMuPDF
from sklearn.neighbors import NearestNeighbors  # Import NearestNeighbors
from rag_model import documents, vectorizer, knn

def handle_file_upload(uploaded_file):
    global documents, vectorizer, knn

    # Clear previous documents
    documents.clear()

    if uploaded_file.type == "text/plain":
        content = uploaded_file.read().decode("utf-8")
        documents.append(content)
    elif uploaded_file.type == "text/csv":  # for CSV
        df = pd.read_csv(uploaded_file)
        documents.extend(df['text_column'].tolist())  # Adjust 'text_column' as needed
    elif uploaded_file.type == "application/pdf":  # for PDF
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in pdf_document:
            text += page.get_text()
        documents.append(text)

    # Initialize the RAG model with uploaded documents
    if documents:
        vectorizer.fit(documents)
        X = vectorizer.transform(documents)
        knn = NearestNeighbors(n_neighbors=min(3, len(documents)), metric='cosine').fit(X)

        return "File processed successfully!"  # Confirmation message
    else:
        return "No text found in the uploaded file."  # Warning message
