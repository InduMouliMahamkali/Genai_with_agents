# frontend/chat_ui.py

import streamlit as st
import requests
from datetime import datetime

API_URL = "http://localhost:8000/ask"

# Set up the page
st.set_page_config(page_title="GenAI Agent", page_icon="🧠")
st.title("🧠 GenAI Company Agent")
st.markdown("Ask me anything about your company policies, onboarding, or HR info.")

# Session ID input
if "session_id" not in st.session_state:
    st.session_state.session_id = ""

st.sidebar.header("Session Settings")
session_id_input = st.sidebar.text_input("Session ID", value=st.session_state.session_id)

if session_id_input:
    st.session_state.session_id = session_id_input

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Text box for user input
user_input = st.text_input("You:", key="input_box")

# On submission
if st.button("Send") and user_input and st.session_state.session_id:
    payload = {
        "session_id": st.session_state.session_id,
        "user_input": user_input
    }

    try:
        response = requests.post(API_URL, json=payload)
        agent_reply = response.json().get("response", "⚠️ No reply from agent.")
    except Exception as e:
        agent_reply = f"❌ Error: {e}"

    # Save to chat history
    st.session_state.chat_history.append({
        "timestamp": datetime.utcnow().isoformat(),
        "user": user_input,
        "agent": agent_reply
    })

    # Clear input box
    st.session_state.input_box = ""

# Display chat history
for chat in reversed(st.session_state.chat_history):
    st.markdown(f"👤 **You**: {chat['user']}")
    st.markdown(f"🤖 **Agent**: {chat['agent']}")
    st.markdown("---")
