import os
import streamlit as st
import time
from helpers import process_pdf, save_uploaded_file, create_vector_space

# Initialize session states
if 'conversations' not in st.session_state:
    st.session_state.conversations = {}
if 'current_session' not in st.session_state:
    st.session_state.current_session = None
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []
if 'processed_files' not in st.session_state:
    st.session_state.processed_files = []

# Helper function to start a new conversation
def start_new_conversation():
    session_name = f"Conversation {len(st.session_state.conversations) + 1}"
    st.session_state.conversations[session_name] = []
    st.session_state.current_session = session_name
    with st.empty():
        st.success(f"Started new session: {session_name}")
        time.sleep(3)

# Helper function to save messages to conversation history
def save_message_to_conversation(session_name, role, message):
    st.session_state.conversations[session_name].append({"role": role, "content": message})

# Sidebar: Display components in the desired order
with st.sidebar:
    st.title("Conversation History")

    uploaded_files = st.file_uploader("Upload files", type=["pdf"], accept_multiple_files=True)

    if uploaded_files:
        st.session_state.uploaded_files = []
        for uploaded_file in uploaded_files:
            if uploaded_file.name not in st.session_state.uploaded_files:
                st.session_state.uploaded_files.append(uploaded_file.name)
                save_path = save_uploaded_file(uploaded_file)
                with st.empty():
                    st.success(f"File saved to {save_path}")
                    time.sleep(3)
            # Process and preview PDF content
            pdf_text = process_pdf(uploaded_file)
            st.write(f"Uploaded file: {uploaded_file.name}")
            st.write(f"File size: {uploaded_file.size} bytes")
            st.write("Preview of the file content:")
            st.write(pdf_text[:500])

    # Add a process button to read all uploaded files
    if st.button("Process Uploaded Files"):
        st.session_state.processed_files = [
            {
                "name": uploaded_file.name,
                "content": process_pdf(uploaded_file)
            } for uploaded_file in uploaded_files
        ]
        with st.empty():
            st.success("Files processed successfully!")
            time.sleep(3)

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
    st.subheader(f"Session: {current_session}")
    for message in st.session_state.conversations[current_session]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
else:
    st.write("No conversation selected. Start or select a conversation from the sidebar.")

# Accept user input if a conversation is active
if current_session:
    prompt = st.chat_input("What is up?")
    if prompt:
        save_message_to_conversation(current_session, "user", prompt)
        with st.chat_message("user"):
            st.markdown(prompt)

        ########################################## temporary solution ##########################################
        # Generate assistant response based on the processed PDF content or state if no documents are uploaded
        if 'processed_files' in st.session_state and len(st.session_state.processed_files) > 0:
            pdf_texts = ""
            for file_info in st.session_state.processed_files:
                pdf_texts += f"\n\n--- Content from {file_info['name']} ---\n\n{file_info['content'][:500]}"
            response_text = f"This is a response based on the content of the uploaded documents:{pdf_texts}"
        else:
            response_text = "No documents uploaded. This is a response without any document context."
        ########################################## temporary solution ##########################################

        with st.chat_message("assistant"):
            st.markdown(response_text)

        save_message_to_conversation(current_session, "assistant", response_text)
else:
    st.write("Please start or select a conversation from the sidebar to begin chatting.")
