import os
import streamlit as st
from PyPDF2 import PdfReader

# Helper function to process PDF
def process_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Initialize sidebar state if it doesn't exist
if "sidebar_open" not in st.session_state:
    st.session_state.sidebar_open = True

# Initialize conversations state
if 'conversations' not in st.session_state:
    st.session_state.conversations = {}

# Initialize current session state
if "current_session" not in st.session_state:
    st.session_state.current_session = None

# Helper function to start a new conversation
def start_new_conversation():
    session_name = f"Conversation {len(st.session_state.conversations) + 1}"
    st.session_state.conversations[session_name] = []
    st.session_state.current_session = session_name
    st.success(f"Started new session: {session_name}")

# Helper function to save messages to conversation history
def save_message_to_conversation(session_name, role, message):
    st.session_state.conversations[session_name].append({"role": role, "content": message})

# Sidebar: Display components in the desired order
with st.sidebar:
    st.title("Conversation History")

    # Add the upload file button at the top
    uploaded_file = st.file_uploader("Upload a file", type=["pdf"])
    if uploaded_file is not None:
        st.write(f"Uploaded file: {uploaded_file.name}")
        st.write(f"File type: {uploaded_file.type}")
        st.write(f"File size: {uploaded_file.size} bytes")

        # Process and preview PDF
        if uploaded_file.type == "application/pdf":
            st.success("PDF file loaded successfully!")
            pdf_text = process_pdf(uploaded_file)
            st.write("Preview of the file content:")
            st.write(pdf_text[:500])  # Display first 500 characters

            # Ensure the uploads directory exists
            upload_dir = "uploads"
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)

            # Save the uploaded PDF locally
            save_path = os.path.join(upload_dir, uploaded_file.name)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"File saved to {save_path}")
        else:
            st.error("The uploaded file is not a PDF.")

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
    if prompt := st.chat_input("What is up?"):
        # Save user message
        save_message_to_conversation(current_session, "user", prompt)
        with st.chat_message("user"):
            st.markdown(prompt)

        # Retrieve relevant documents based on the user input
        # For simplicity, we simulate the retrieval here
        retrieved_docs = f"Relevant content for: {prompt}"  # This would be a placeholder for actual RAG model processing

        # Generate assistant response (simulated in this case)
        response_text = f"This is a simulated response based on the documents: {retrieved_docs}"

        # Display assistant's response
        with st.chat_message("assistant"):
            response_container = st.empty()
            response_container.markdown(response_text)

        # Save the assistant's response
        save_message_to_conversation(current_session, "assistant", response_text)
else:
    st.write("Please start or select a conversation from the sidebar to begin chatting.")
