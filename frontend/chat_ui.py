# frontend/chat_ui.py

import streamlit as st
import requests
from datetime import datetime
from feedback.feedback_logger import FeedbackLogger

API_URL = "http://localhost:8000/ask"
logger = FeedbackLogger()

# Set page and title
st.set_page_config(page_title="GenAI Chat", page_icon="💬")
st.title("💬 Chat with GenAI Agent")
st.markdown("Ask HR, onboarding, or general company questions.")

# Session ID input
if "session_id" not in st.session_state:
    st.session_state.session_id = ""

st.sidebar.header("Session Settings")
session_id_input = st.sidebar.text_input("Session ID", value=st.session_state.session_id)

if session_id_input:
    st.session_state.session_id = session_id_input

# Chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input field
user_input = st.text_input("You:", key="input_box")

# Send message
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

    # Save to history
    st.session_state.chat_history.append({
        "timestamp": datetime.utcnow().isoformat(),
        "user": user_input,
        "agent": agent_reply
    })

    # Clear input box
    #st.session_state.input_box = ""
    st.rerun()

# Display chat with feedback
for i, chat in enumerate(reversed(st.session_state.chat_history)):
    st.markdown(f"👤 **You**: {chat['user']}")
    st.markdown(f"🤖 **Agent**: {chat['agent']}")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button(f"👍 Helpful {i}", key=f"up_{i}"):
            logger.log_feedback(
                session_id=st.session_state.session_id,
                user_input=chat['user'],
                agent_response=chat['agent'],
                rating="positive"
            )
            st.success("Feedback recorded: 👍")
    with col2:
        if st.button(f"👎 Not helpful {i}", key=f"down_{i}"):
            logger.log_feedback(
                session_id=st.session_state.session_id,
                user_input=chat['user'],
                agent_response=chat['agent'],
                rating="negative"
            )
            st.success("Feedback recorded: 👎")

    st.markdown("---")