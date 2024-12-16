import os
from doc_processor import embed_documents

def test_embed_documents():
    # Path to the folder containing test PDF files
    test_folder = 'uploads'

    # Ensure the test folder exists
    if not os.path.exists(test_folder):
        print(f"Test folder '{test_folder}' does not exist.")
        return

    # Call the embed_documents function
    docs, embeddings = embed_documents(test_folder)

    # Print the results
    print("Documents:")
    for doc in docs:
        print(doc[:100])  # Print the first 100 characters of each document

    print("\nEmbeddings:")
    for embedding in embeddings:
        print(embedding[:10])  # Print the first 10 elements of each embedding

if __name__ == "__main__":
    test_embed_documents()