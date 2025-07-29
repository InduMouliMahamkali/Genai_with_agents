# sessions/interaction_logger.py

import sqlite3
import pandas as pd
import os
from datetime import datetime

INTERACTIONS_DB = "data/logs/interactions.db"
INTERACTIONS_CSV = "data/logs/interactions.csv"
FEEDBACK_DB = "data/feedback.db"
FEEDBACK_CSV = "data/logs/feedback.csv"

class InteractionLogger:
    def __init__(self):
        os.makedirs("data/logs", exist_ok=True)

        # Connect to interaction database
        self.interaction_conn = sqlite3.connect(INTERACTIONS_DB, check_same_thread=False)
        self._create_interaction_table()

        # Connect to feedback database
        self.feedback_conn = sqlite3.connect(FEEDBACK_DB, check_same_thread=False)
        self._create_feedback_table()

    def _create_interaction_table(self):
        with self.interaction_conn:
            self.interaction_conn.execute("""
                CREATE TABLE IF NOT EXISTS interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    timestamp TEXT,
                    user_input TEXT,
                    agent_response TEXT,
                    agent_id TEXT,
                    tags TEXT DEFAULT ''
                )
            """)

    def _create_feedback_table(self):
        with self.feedback_conn:
            self.feedback_conn.execute("""
                CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    query TEXT,
                    rating TEXT,
                    comment TEXT,
                    timestamp TEXT
                )
            """)

    def log(self, session_id: str, user_input: str, agent_response: str, agent_id: str):
        timestamp = datetime.utcnow().isoformat()

        # Log to SQLite
        with self.interaction_conn:
            self.interaction_conn.execute("""
                INSERT INTO interactions (session_id, timestamp, user_input, agent_response, agent_id)
                VALUES (?, ?, ?, ?, ?)
            """, (session_id, timestamp, user_input, agent_response, agent_id))

        # Log to CSV
        entry = {
            "session_id": session_id,
            "timestamp": timestamp,
            "user_input": user_input,
            "agent_response": agent_response,
            "agent_id": agent_id
        }

        if not os.path.exists(INTERACTIONS_CSV):
            pd.DataFrame([entry]).to_csv(INTERACTIONS_CSV, index=False)
        else:
            pd.DataFrame([entry]).to_csv(INTERACTIONS_CSV, mode="a", header=False, index=False)

    def log_feedback(self, session_id: str, query: str, rating: str, comment: str = ""):
        timestamp = datetime.utcnow().isoformat()

        # Log to SQLite
        with self.feedback_conn:
            self.feedback_conn.execute("""
                INSERT INTO feedback (session_id, query, rating, comment, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """, (session_id, query, rating, comment, timestamp))

        # Log to CSV
        entry = {
            "session_id": session_id,
            "query": query,
            "rating": rating,
            "comment": comment,
            "timestamp": timestamp
        }

        if not os.path.exists(FEEDBACK_CSV):
            pd.DataFrame([entry]).to_csv(FEEDBACK_CSV, index=False)
        else:
            pd.DataFrame([entry]).to_csv(FEEDBACK_CSV, mode="a", header=False, index=False)

    def update_tags(self, interaction_id: int, tags: str):
        with self.interaction_conn:
            self.interaction_conn.execute(
                "UPDATE interactions SET tags = ? WHERE id = ?",
                (tags, interaction_id)
            )
