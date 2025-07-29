# logging/query_logger.py

import csv
import os
from datetime import datetime

LOG_FILE = "data/query_logs.csv"

class QueryLogger:
    def __init__(self, log_path=LOG_FILE):
        self.log_path = log_path
        if not os.path.exists(os.path.dirname(log_path)):
            os.makedirs(os.path.dirname(log_path))
        if not os.path.exists(self.log_path):
            self._init_log_file()

    def _init_log_file(self):
        with open(self.log_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "session_id", "agent", "query", "response", "feedback"])

    def log_query(self, session_id: str, agent: str, query: str, response: str, feedback: str = ""):
        timestamp = datetime.utcnow().isoformat()
        with open(self.log_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, session_id, agent, query, response, feedback])

    def load_logs(self) -> list:
        with open(self.log_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)
