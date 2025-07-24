# agents/multi_agent.py

class MultiAgent:
    def __init__(self, agent_id="multi_agent", config=None, agents=None):
        self.agent_id = agent_id
        self.config = config or {}
        self.agents = agents or {}

    def answer_query(self, query, session_id=None):
        query_lower = query.lower()
        response_parts = []

        # ITSM
        if "ticket" in query_lower or "incident" in query_lower or "jira" in query_lower:
            itsm = self.agents.get("itsm_agent")
            if itsm:
                response_parts.append("🛠️ Ticket Info:\n" + itsm.answer_query(query, session_id=session_id))

        # DevOps
        if any(kw in query_lower for kw in ["etl", "dashboard", "pipeline", "kpi"]):
            devops = self.agents.get("devops_agent")
            if devops:
                response_parts.append("⚙️ DevOps Action:\n" + devops.answer_query(query))

        # Docs
        if any(kw in query_lower for kw in ["policy", "handbook", "mission", "values", "document"]):
            docs = self.agents.get("docs_agent")
            if docs:
                response_parts.append("📄 Policy Doc:\n" + docs.answer_query(query))

        # HR
        if any(kw in query_lower for kw in ["salary", "leave", "holiday", "appraisal", "pay"]):
            hr = self.agents.get("hr_agent")
            if hr:
                response_parts.append("👤 HR Info:\n" + hr.answer_query(query, session_id=session_id))

        # If no match
        if not response_parts:
            return "🤖 I couldn’t match this to any known combined task."

        return "\n\n".join(response_parts)
