from doc_processor import initialize_rag

def handle_query(upload_folder, query, top_k=5):
    """
    Handle the user query by retrieving relevant content.
    :param upload_folder: Path to the folder containing uploaded documents.
    :param query: User query string.
    :param top_k: Number of top documents to retrieve.
    :return: List of tuples (retrieved_document, score).
    """
    if not query.strip():
        return "Query cannot be empty. Please provide valid input.", []

    try:
        # Perform retrieval
        results = initialize_rag(upload_folder, query, top_k)
        return "Query processed successfully.", results
    except Exception as e:
        return f"Error processing query: {str(e)}", []
