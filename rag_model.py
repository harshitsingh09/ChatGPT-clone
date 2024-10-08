import streamlit as st
import random
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from transformers import pipeline  # Import Hugging Face summarizer

# Initialize variables
documents = []
vectorizer = TfidfVectorizer()
knn = None

# Initialize the summarizer pipeline using transformers
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# Function to start a new conversation
def start_new_conversation():
    session_id = len(st.session_state.conversations) + 1
    st.session_state.conversations[f"Session {session_id}"] = []
    st.session_state.current_session = f"Session {session_id}"

# Save message to the current conversation
def save_message_to_conversation(session_id, role, content):
    st.session_state.conversations[session_id].append({"role": role, "content": content})

# Retrieve documents based on user query
def retrieve_documents(query):
    global knn, vectorizer
    if len(documents) < 2:  # Check if there are at least 2 documents
        return documents  # Return the only document available if there's just one

    query_vector = vectorizer.transform([query])  # Vectorize the query
    distances, indices = knn.kneighbors(query_vector)  # Retrieve top documents
    return [documents[i] for i in indices.flatten()]

# Generate response based on retrieved documents
def response_generator(retrieved_docs):
    # Combine the retrieved documents into a single string
    combined_text = " ".join(retrieved_docs)
    
    # Handle empty or very short inputs gracefully
    if not combined_text.strip():
        return "I couldn't find relevant information in the documents."
    
    # If the input is too short for summarization, respond with a fallback message
    if len(combined_text.split()) < 10:  # Assume at least 10 words are needed for meaningful summarization
        return "The content is too short to summarize."

    # Generate a summary using the summarizer
    try:
        summary = summarizer(combined_text, max_length=50, min_length=25, do_sample=False)[0]['summary_text']
        return summary
    except Exception as e:
        return f"An error occurred while generating a response: {e}"
