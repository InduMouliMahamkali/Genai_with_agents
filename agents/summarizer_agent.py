# agents/summarizer_agent.py

import re
from sessions.session_manager import SessionManager

class SummarizerAgent:
    def __init__(self, agent_id="summarizer_agent", config=None):
        self.agent_id = agent_id
        self.config = config or {}
        self.session_manager = SessionManager()

    def answer_query(self, query, session_id=None):
        if not session_id:
            return "❗ Please provide a valid session ID for summarization."

        # 🔍 Extract message count (e.g. "summarize last 3 messages")
        num = self._extract_message_count(query)
        if not num:
            num = 5  # Default if not specified

        # 🧾 Get session history
        interactions = self.session_manager.get_history(session_id)
        if not interactions:
            return "🗃️ No conversations found for this session."

        last_messages = interactions[-num:]
        context = "\n".join([
            f"User: {user_input}\nBot: {agent_response}"
            for _, user_input, agent_response in last_messages
        ])

        # 🧠 Local summarization using rule-based fallback
        summary = self._simple_summarizer(context)
        return summary

    def _extract_message_count(self, query: str) -> int:
        """Extract number of messages to summarize from the query."""
        match = re.search(r"(?:last|past)\s+(\d+)", query)
        if match:
            return int(match.group(1))
        match = re.search(r"summarize\s+(\d+)", query)
        if match:
            return int(match.group(1))
        return None

    def _simple_summarizer(self, text: str) -> str:
        """Fallback basic summarizer (first and last message)."""
        lines = [line for line in text.strip().split("\n") if line]
        if not lines:
            return "❓ No meaningful content to summarize."
        
        if len(lines) <= 2:
            return "\n".join(lines)

        summary = f"📝 Summary:\n• {lines[0]}\n• {lines[-1]}"
        return summary
