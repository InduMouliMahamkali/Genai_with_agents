# sessions/session_manager.py

import sqlite3
from datetime import datetime

DB_PATH = "data/sessions.db"

class SessionManager:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self._create_tables()

    def _create_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    user_input TEXT NOT NULL,
                    agent_response TEXT NOT NULL,
                    agent_id TEXT NOT NULL
                )
            """)

    def log_interaction(self, session_id: str, user_input: str, agent_response: str, agent_id: str):
        with self.conn:
            self.conn.execute("""
                INSERT INTO interactions (session_id, timestamp, user_input, agent_response, agent_id)
                VALUES (?, ?, ?, ?, ?)
            """, (session_id, datetime.utcnow().isoformat(), user_input, agent_response, agent_id))

    def get_history(self, session_id: str):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT timestamp, user_input, agent_response FROM interactions
            WHERE session_id = ?
            ORDER BY timestamp ASC
        """, (session_id,))
        return cursor.fetchall()
