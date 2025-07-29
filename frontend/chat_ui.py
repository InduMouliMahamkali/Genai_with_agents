# frontend/chat_ui.py

import sys
import os
import uuid
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from orchestrator.agent_orchestrator import AgentOrchestrator
from frontend.analytics_dashboard import show_dashboard
from sessions.interaction_logger import InteractionLogger

# Initialize logger
logger = InteractionLogger()

# Streamlit page config
st.set_page_config(page_title="GenAI Agent App", layout="centered")
st.title("🤖 GenAI Multi-Agent Chat")

# Auto-generate session ID
if "session_id" not in st.session_state:
    st.session_state.session_id = f"user_{str(uuid.uuid4())[:8]}"
session_id = st.session_state.session_id

# Sidebar
with st.sidebar:
    st.header("🆔 Session")
    st.markdown(f"**Session ID:** `{session_id}`")
    show_metrics = st.checkbox("📊 Show Analytics Dashboard")

# Init orchestrator + messages
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = AgentOrchestrator()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Input
user_input = st.text_input("Ask something...", key="input_box")

# Send logic
if st.button("Send") and user_input:
    orchestrator = st.session_state.orchestrator
    try:
        response = orchestrator.route_query(session_id, user_input)
    except Exception as e:
        response = f"❌ Error: {str(e)}"

    st.session_state.messages.append({
        "role": "user",
        "message": user_input
    })
    st.session_state.messages.append({
        "role": "agent",
        "message": response,
        "user_input": user_input,  # Save for feedback
        "feedback_given": False
    })

# Chat history
for idx, msg in enumerate(st.session_state.messages):
    if msg["role"] == "user":
        st.markdown(f"🧑 **You:** {msg['message']}")
    else:
        st.markdown(f"🤖 **Agent:** {msg['message']}")

        # Show feedback buttons only once per agent message
        if not msg.get("feedback_given", False):
            col1, col2 = st.columns([1, 5])
            with col1:
                if st.button("👍", key=f"thumbs_up_{idx}"):
                    logger.log_feedback(session_id, msg["user_input"], rating="positive", comment="")
                    st.session_state.messages[idx]["feedback_given"] = True
                    st.success("Thanks for your feedback! 👍")
            with col2:
                if st.button("👎", key=f"thumbs_down_{idx}"):
                    comment = st.text_input("What went wrong?", key=f"comment_{idx}")
                    if st.button("Submit", key=f"submit_comment_{idx}"):
                        logger.log_feedback(session_id, msg["user_input"], rating="negative", comment=comment)
                        st.session_state.messages[idx]["feedback_given"] = True
                        st.success("Thanks for your feedback! 👎")

# Optional: Show analytics dashboard
if show_metrics:
    st.divider()
    show_dashboard()
