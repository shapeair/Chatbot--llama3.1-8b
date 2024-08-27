import os
import json
import streamlit as st
from groq import Groq

# Streamlit page configuration
st.set_page_config(
    page_title="LLAMA 3.1 Chat",
    page_icon="🦙",
    layout="centered"
)

# Load configuration data
config_path = r"C:\Users\AANCHAL\OneDrive - vit.ac.in\vscode\chatbot_groq\src\config.json"
try:
    with open(config_path) as f:
        config_data = json.load(f)
except FileNotFoundError:
    st.error(f"Configuration file not found at {config_path}")
    st.stop()

GROQ_API_KEY = config_data.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("GROQ_API_KEY not found in configuration")
    st.stop()

# Save API key to environment variable
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

client = Groq()

# Initialize session states for chat history and previous chats
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "previous_chats" not in st.session_state:
    st.session_state.previous_chats = []

# Sidebar for new chat and previous chats
with st.sidebar:
    st.title("Chat Options")
    
    # New chat button
    if st.button("New Chat"):
        if st.session_state.chat_history:
            st.session_state.previous_chats.append(st.session_state.chat_history)
        st.session_state.chat_history = []

    # Display previous chats
    st.write("History")
    for i, chat in enumerate(st.session_state.previous_chats):
        if st.button(f"Chat {i+1}"):
            st.session_state.chat_history = chat
            st.experimental_rerun()  # Refresh the page to show the selected chat

# Streamlit page title
st.title("🦙LLAMA 3.1 Chatbot (8B instant)")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input field for user's message
user_prompt = st.chat_input("Ask LLAMA...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})
    
    # Send user's message to the LLM and get response
    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        *st.session_state.chat_history
    ]
    
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages
        )
        assistant_response = response.choices[0].message.content
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
        
        # Display LLM response
        with st.chat_message("assistant"):
            st.markdown(assistant_response)
    except Exception as e:
        st.error(f"An error occurred: {e}")
