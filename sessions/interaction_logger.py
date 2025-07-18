# sessions/interaction_logger.py

import sqlite3
import pandas as pd
import os
from datetime import datetime

CSV_LOG = "data/logs/interactions.csv"
DB_PATH = "data/logs/interactions.db"

class InteractionLogger:
    def __init__(self):
        os.makedirs("data/logs", exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self._create_table()

    def _create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    timestamp TEXT,
                    user_input TEXT,
                    agent_response TEXT,
                    agent_id TEXT
                )
            """)

    def log(self, session_id: str, user_input: str, agent_response: str, agent_id: str):
        timestamp = datetime.utcnow().isoformat()

        # SQLite logging
        with self.conn:
            self.conn.execute("""
                INSERT INTO interactions (session_id, timestamp, user_input, agent_response, agent_id)
                VALUES (?, ?, ?, ?, ?)
            """, (session_id, timestamp, user_input, agent_response, agent_id))

        # CSV logging
        entry = {
            "session_id": session_id,
            "timestamp": timestamp,
            "user_input": user_input,
            "agent_response": agent_response,
            "agent_id": agent_id
        }

        if not os.path.exists(CSV_LOG):
            pd.DataFrame([entry]).to_csv(CSV_LOG, index=False)
        else:
            pd.DataFrame([entry]).to_csv(CSV_LOG, mode="a", header=False, index=False)
