import streamlit as st
from file_handler import handle_file_upload
from rag_model import start_new_conversation, save_message_to_conversation, retrieve_documents, response_generator

# Initialize sidebar state if it doesn't exist
if "sidebar_open" not in st.session_state:
    st.session_state.sidebar_open = True

# Initialize conversations state
if 'conversations' not in st.session_state:
    st.session_state.conversations = {}

# Initialize current session state
if "current_session" not in st.session_state:
    st.session_state.current_session = None

# Sidebar: Display components in the desired order
with st.sidebar:
    st.title("Conversation History")

    # Add the upload file button at the top
    uploaded_file = st.file_uploader("Upload a file", type=["txt", "csv", "pdf"])
    if uploaded_file is not None:
        upload_message = handle_file_upload(uploaded_file)  # Handle the uploaded file
        st.success(upload_message)  # Display success message

    # Add the "Start New Conversation" button below the file uploader
    if st.button("Start New Conversation"):
        start_new_conversation()

    # Display conversation sessions as buttons below the "Start New Conversation" button
    for session in st.session_state.conversations.keys():
        if st.button(session):
            st.session_state.current_session = session

# Main Title
st.title("Simple Chat")

# Display chat history of the selected conversation
current_session = st.session_state.current_session
if current_session:
    st.subheader(f"Conversation: {current_session}")
    for message in st.session_state.conversations[current_session]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
else:
    st.write("No conversation selected. Start or select a conversation from the sidebar.")

# Accept user input if a conversation is active
if current_session:
    if prompt := st.chat_input("What is up?"):
        # Save user message
        save_message_to_conversation(current_session, "user", prompt)
        with st.chat_message("user"):
            st.markdown(prompt)

        # Retrieve relevant documents based on the user input
        retrieved_docs = retrieve_documents(prompt)
        
        # Ensure retrieved_docs is not empty
        if retrieved_docs:
            # Generate assistant response and stream it
            with st.chat_message("assistant"):
                response_container = st.empty()
                response_text = response_generator(retrieved_docs)  # Pass retrieved documents to the generator
                response_container.markdown(response_text)

            # Save the streamed assistant response
            save_message_to_conversation(current_session, "assistant", response_text)
        else:
            # Handle the case where no relevant documents were found
            with st.chat_message("assistant"):
                st.markdown("I couldn't find any relevant documents based on your query.")
else:
    st.write("Please start or select a conversation from the sidebar to begin chatting.")
