# Import libraries
import streamlit as st
import random
import time

# Streamed response emulator
def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

# Initialize sidebar state if it doesn't exist
if "sidebar_open" not in st.session_state:
    st.session_state.sidebar_open = True

# Initialize conversations state
if 'conversations' not in st.session_state:
    st.session_state.conversations = {}

# Initialize current session state
if "current_session" not in st.session_state:
    st.session_state.current_session = None

# Function to start a new conversation
def start_new_conversation():
    session_id = len(st.session_state.conversations) + 1
    st.session_state.conversations[f"Session {session_id}"] = []
    st.session_state.current_session = f"Session {session_id}"

# Save message to the current conversation
def save_message_to_conversation(session_id, role, content):
    st.session_state.conversations[session_id].append({"role": role, "content": content})

# Sidebar: Display conversation sessions as buttons
with st.sidebar:
    st.title("Conversation History")

    # Display buttons for each conversation session
    for session in st.session_state.conversations.keys():
        if st.button(session):
            st.session_state.current_session = session

    # Button to start a new conversation
    if st.button("Start New Conversation"):
        start_new_conversation()

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

# Accept user input
if prompt := st.chat_input("What is up?"):
    if current_session:
        # Save user message
        save_message_to_conversation(current_session, "user", prompt)
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate assistant response and stream it
        with st.chat_message("assistant"):
            response_container = st.empty()
            response_text = ""
            for word in response_generator():
                response_text += word
                response_container.markdown(response_text)

        # Save the streamed assistant response
        save_message_to_conversation(current_session, "assistant", response_text)
