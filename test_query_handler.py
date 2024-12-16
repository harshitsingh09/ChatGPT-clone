from query_handler import handle_query

def test_handle_query():
    # Path to the folder containing test PDF files
    test_folder = 'uploads'
    
    # Sample query
    query = "Sample query text"

    # Call the handle_query function
    message, results = handle_query(test_folder, query)

    # Print the results
    print("Message:", message)
    print("Results:")
    for result in results:
        print(result)

if __name__ == "__main__":
    test_handle_query()