# feedback/feedback_logger.py

import sqlite3
from datetime import datetime

DB_PATH = "data/feedback.db"

class FeedbackLogger:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self._create_table()

    def _create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    user_input TEXT,
                    agent_response TEXT,
                    rating TEXT,
                    timestamp TEXT
                )
            """)

    def log_feedback(self, session_id: str, user_input: str, agent_response: str, rating: str):
        with self.conn:
            self.conn.execute("""
                INSERT INTO feedback (session_id, user_input, agent_response, rating, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """, (session_id, user_input, agent_response, rating, datetime.utcnow().isoformat()))
