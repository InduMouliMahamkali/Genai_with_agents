from sessions.interaction_logger import InteractionLogger

class FeedbackCollector:
    def __init__(self):
        self.logger = InteractionLogger()

    def submit_feedback(self, session_id, query, score, comment=""):
        self.logger.log_feedback(session_id, query, score, comment)
        return "✅ Feedback submitted. Thank you!"

    def get_all_feedback(self):
        cursor = self.logger.conn.cursor()
        cursor.execute("SELECT session_id, query, feedback_score, comment FROM feedback ORDER BY timestamp DESC")
        return cursor.fetchall()