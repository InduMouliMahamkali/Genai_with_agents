# frontend/analytics_dashboard.py

import streamlit as st
import pandas as pd
import sqlite3
import os

st.set_page_config(page_title="📊 GenAI Analytics Dashboard", layout="wide")
st.title("📊 GenAI Usage & Feedback Dashboard")

# ---- Load Data ----
INTERACTIONS_DB = "data/logs/interactions.db"
FEEDBACK_DB = "data/feedback.db"

@st.cache_data
def load_interactions():
    if not os.path.exists(INTERACTIONS_DB):
        return pd.DataFrame()
    conn = sqlite3.connect(INTERACTIONS_DB)
    df = pd.read_sql_query("SELECT * FROM interactions", conn)
    conn.close()
    return df

@st.cache_data
def load_feedback():
    if not os.path.exists(FEEDBACK_DB):
        return pd.DataFrame()
    conn = sqlite3.connect(FEEDBACK_DB)
    df = pd.read_sql_query("SELECT * FROM feedback", conn)
    conn.close()
    return df

interactions = load_interactions()
feedback = load_feedback()

# ---- Metrics Row ----
st.subheader("📌 Summary Metrics")
col1, col2, col3 = st.columns(3)

col1.metric("🧑 Unique Sessions", interactions['session_id'].nunique() if not interactions.empty else 0)
col2.metric("💬 Total Questions", len(interactions))
col3.metric("🤖 Agent Used", interactions['agent_id'].mode()[0] if not interactions.empty else "N/A")

# ---- Feedback Breakdown ----
st.subheader("👍👎 Feedback Sentiment")

if feedback.empty:
    st.info("No feedback available.")
else:
    sentiment_counts = feedback["rating"].value_counts().rename_axis("rating").reset_index(name="count")
    st.bar_chart(sentiment_counts.set_index("rating"))

# ---- Conversation Table ----
st.subheader("🧾 Full Interaction Log")

if interactions.empty:
    st.warning("No interactions found.")
else:
    st.dataframe(interactions.sort_values("timestamp", ascending=False), use_container_width=True)

# ---- Optional Filters ----
st.markdown("🔍 **Filter by Session**")
if not interactions.empty:
    session_filter = st.selectbox("Select session ID", options=interactions["session_id"].unique())
    filtered_df = interactions[interactions["session_id"] == session_filter]
    st.write(f"Showing {len(filtered_df)} records for session `{session_filter}`")
    st.dataframe(filtered_df, use_container_width=True)
