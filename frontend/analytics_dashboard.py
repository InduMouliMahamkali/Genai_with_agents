# frontend/analytics_dashboard.py

import streamlit as st
import pandas as pd
import sqlite3
import os
from sessions.interaction_logger import InteractionLogger

INTERACTIONS_DB = "data/sessions.db"
CSV_LOG_PATH = "data/logs/interactions.csv"

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
    if not os.path.exists(INTERACTIONS_DB):
        return pd.DataFrame()
    conn = sqlite3.connect(INTERACTIONS_DB)
    try:
        df = pd.read_sql_query("SELECT * FROM feedback", conn)
    except Exception:
        df = pd.DataFrame()
    conn.close()
    return df

def show_dashboard():
    st.subheader("📊 GenAI Usage & Feedback Dashboard")

    interactions = load_interactions()
    feedback = load_feedback()

    # --- Summary metrics ---
    st.subheader("📌 Summary Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("🧑 Unique Sessions", interactions['session_id'].nunique() if not interactions.empty else 0)
    col2.metric("💬 Total Questions", len(interactions))
    col3.metric("🤖 Top Agent", interactions['agent_id'].mode()[0] if not interactions.empty else "N/A")

    # --- Feedback Breakdown ---
    st.subheader("👍👎 Feedback Sentiment")
    if feedback.empty:
        st.info("No feedback available.")
    else:
        sentiment_counts = feedback["feedback_score"].value_counts().rename_axis("rating").reset_index(name="count")
        st.bar_chart(sentiment_counts.set_index("rating"))

    # --- Search + Filter ---
    st.subheader("🔍 Search & Filter Interactions")

    if not interactions.empty:
        search_query = st.text_input("Search query")
        session_filter = st.selectbox("Filter by session ID", ["All"] + sorted(interactions["session_id"].unique()))

        filtered_df = interactions.copy()

        if search_query:
            filtered_df = filtered_df[filtered_df["user_input"].str.contains(search_query, case=False)]

        if session_filter != "All":
            filtered_df = filtered_df[filtered_df["session_id"] == session_filter]

        st.write(f"📄 Showing {len(filtered_df)} records")

        # --- Tagging ---
        st.markdown("🔖 **Tag Interactions**")
        for idx, row in filtered_df.iterrows():
            st.write(f"**Q:** {row['user_input']}")
            current_tags = row.get("tags", "") or ""
            tag_input = st.text_input("Add/Edit tags (comma-separated)", value=current_tags, key=f"tags_{row['id']}")
            if st.button("💾 Save Tags", key=f"save_{row['id']}"):
                logger = InteractionLogger()
                logger.update_tags(row['id'], tag_input)
                st.success("✅ Tags updated!")

        # --- Export ---
        st.markdown("📥 **Export Filtered Interactions**")
        if st.button("Export to CSV"):
            export_path = "data/logs/exported_interactions.csv"
            filtered_df.to_csv(export_path, index=False)
            st.success(f"Exported to `{export_path}`")
    else:
        st.warning("No interactions available.")
