# frontend/chat_ui.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from orchestrator.agent_orchestrator import AgentOrchestrator

st.set_page_config(page_title="GenAI Agent App", layout="centered")
st.title("🤖 GenAI Multi-Agent Chat")

# Initialize orchestrator and message state
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = AgentOrchestrator()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Input field
user_input = st.text_input("Ask something...", key="input_box")

# Send button logic
if st.button("Send") and user_input:
    orchestrator = st.session_state.orchestrator
    session_id = st.session_state.get("session_id", "default_user")

    try:
        response = orchestrator.route_query(session_id, user_input)
    except Exception as e:
        response = f"❌ Error: {str(e)}"

    st.session_state.messages.append(("user", user_input))
    st.session_state.messages.append(("agent", response))

# Display messages
for role, message in st.session_state.messages:
    if role == "user":
        st.markdown(f"🧑 **You:** {message}")
    else:
        st.markdown(f"🤖 **Agent:** {message}")
