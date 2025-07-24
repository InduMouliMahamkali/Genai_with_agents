# frontend/chat_ui.py

import sys
import os
import uuid
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from orchestrator.agent_orchestrator import AgentOrchestrator
from frontend.analytics_dashboard import show_dashboard  # Optional: show dashboard from same UI

# Page config
st.set_page_config(page_title="GenAI Agent App", layout="centered")
st.title("🤖 GenAI Multi-Agent Chat")

# Auto-generate session ID (if not already present)
if "session_id" not in st.session_state:
    st.session_state.session_id = f"user_{str(uuid.uuid4())[:8]}"

session_id = st.session_state.session_id

# Session info in sidebar
with st.sidebar:
    st.header("🆔 Session")
    st.markdown(f"**Session ID:** `{session_id}`")
    show_metrics = st.checkbox("📊 Show Analytics Dashboard")

# Initialize orchestrator and message state
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = AgentOrchestrator()

if "messages" not in st.session_state:
    st.session_state.messages = []

# User input box
user_input = st.text_input("Ask something...", key="input_box")

# Send logic
if st.button("Send") and user_input:
    orchestrator = st.session_state.orchestrator
    try:
        response = orchestrator.route_query(session_id, user_input)
    except Exception as e:
        response = f"❌ Error: {str(e)}"

    st.session_state.messages.append(("user", user_input))
    st.session_state.messages.append(("agent", response))

# Display chat history
for role, message in st.session_state.messages:
    if role == "user":
        st.markdown(f"🧑 **You:** {message}")
    else:
        st.markdown(f"🤖 **Agent:** {message}")

# Show analytics dashboard if selected
if show_metrics:
    st.divider()
    show_dashboard()
