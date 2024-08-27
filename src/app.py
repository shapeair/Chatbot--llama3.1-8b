import os
import json

import streamlit as st
from groq import Groq

#streamlit page configuration
st.set_page_config(
    page_title = "LLAMA 3.1 Chat",
    page_icon = "🦙",
    layout = "centered"
)

working_dir = os.path.dirname(os.path.dirname(__file__))
config_data = json.load(open(r"C:\Users\AANCHAL\OneDrive - vit.ac.in\vscode\chatbot_groq\src\config.json"))

GROQ_API_KEY = config_data["GROQ_API_KEY"]

#save api key to environment variable
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

client = Groq()

# initialize the chat history as streamlit session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    
    
# streamlit page title
st.title("🦙LLAMA 3.1 Chatbot (8B instant)")

# display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        

# [{"role": "user", "content": "What is a LLM"}

# {"role": "assistant", "content": "LLM response"}]

# input field for user's message
user_prompt = st.chat_input("Ask LLAMA....")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})
    
    # sens user's message to the LLM and get response
    message = [
        {"role": "system", "content": "You are a helpful assistant"},
        *st.session_state.chat_history
    ]
    
    response = client.chat.completions.create(
        model = "llama-3.1-8b-instant",
        messages = message
    )
    
    assistant_response = response.choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
    
    #display llm response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
    
    
    