from sentence_transformers import SentenceTransformer
import faiss
import os
import numpy as np
import PyPDF2

# Load the embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to embed documents
def embed_documents(upload_folder):
    """
    Process and embed PDF documents from the upload folder.
    :param upload_folder: Path to the folder containing uploaded documents.
    :return: Tuple (docs, embeddings).
    """
    docs = []
    embeddings = []

    for file_name in os.listdir(upload_folder):
        file_path = os.path.join(upload_folder, file_name)
        if os.path.isfile(file_path) and file_name.lower().endswith('.pdf'):
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                content = ""
                for page in reader.pages:
                    content += page.extract_text()
                docs.append(content)
                embeddings.append(model.encode(content, convert_to_tensor=False))

    return docs, embeddings

# Function to create a FAISS index
def create_faiss_index(embeddings):
    """
    Create a FAISS index from document embeddings.
    :param embeddings: List of embeddings.
    :return: FAISS index object.
    """
    d = embeddings[0].shape[0]  # Dimension of embeddings
    index = faiss.IndexFlatL2(d)
    index.add(np.array(embeddings))
    return index

# Function to search the index
def search_index(index, query, docs, top_k=5):
    """
    Search the FAISS index for the most relevant documents.
    :param index: FAISS index object.
    :param query: Query string.
    :param docs: List of original documents.
    :param top_k: Number of top results to retrieve.
    :return: List of tuples (document, score).
    """
    query_embedding = model.encode(query, convert_to_tensor=False)
    distances, indices = index.search(np.array([query_embedding]), k=top_k)
    results = [(docs[i], distances[0][j]) for j, i in enumerate(indices[0])]
    return results

# Function to initialize RAG process
def initialize_rag(upload_folder, query, top_k=5):
    """
    Complete RAG workflow: embed documents, create FAISS index, and perform retrieval.
    :param upload_folder: Path to the folder containing uploaded documents.
    :param query: Query string.
    :param top_k: Number of top results to retrieve.
    :return: List of retrieved documents and scores.
    """
    docs, embeddings = embed_documents(upload_folder)
    index = create_faiss_index(embeddings)
    return search_index(index, query, docs, top_k)
