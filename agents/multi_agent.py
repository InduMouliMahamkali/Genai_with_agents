import re

class MultiAgent:
    def __init__(self, agent_id="multi_agent", config=None, agents=None):
        self.agent_id = agent_id
        self.config = config or {}

        # Injected agents from orchestrator (preferred) or fallback to direct init
        if agents:
            self.itsm_agent = agents.get("itsm_agent")
            self.devops_agent = agents.get("devops_agent")
            self.docs_agent = agents.get("docs_agent")
            self.hr_agent = agents.get("hr_agent")
        else:
            from agents.itsm_agent import ITSMAgent
            from agents.devops_agent import DevOpsAgent
            from agents.docs_agent import DocsAgent
            from agents.hr_agent import HRAgent

            self.itsm_agent = ITSMAgent()
            self.devops_agent = DevOpsAgent()
            self.docs_agent = DocsAgent()
            self.hr_agent = HRAgent(agent_id="hr_agent", config={})

    def answer_query(self, query, session_id=None):
        query_lower = query.lower()
        response_parts = []

        # Split query into logical sub-tasks
        tasks = re.split(r'\band\b|[.,]', query_lower)

        for task in tasks:
            task = task.strip()
            if not task:
                continue

            # Route to ITSM agent
            if any(kw in task for kw in ['ticket', 'incident', 'update', 'inc']):
                resp = self.itsm_agent.answer_query(task, session_id=session_id)
                response_parts.append("🛠️ Ticket Info:\n" + resp)

            # Route to DevOps agent
            elif any(kw in task for kw in ['etl', 'pipeline', 'dashboard']):
                resp = self.devops_agent.answer_query(task)
                response_parts.append("⚙️ DevOps Action:\n" + resp)

            # Route to Docs agent
            elif any(kw in task for kw in ['policy', 'handbook', 'document']):
                resp = self.docs_agent.answer_query(task)
                response_parts.append("📄 Policy Doc:\n" + resp)

            # Route to HR agent
            elif any(kw in task for kw in ['leave', 'salary', 'holiday']):
                resp = self.hr_agent.answer_query(task, session_id=session_id)
                response_parts.append("👤 HR Info:\n" + resp)

        if not response_parts:
            return "🤖 I couldn’t match this to any known combined task."

        return "\n\n".join(response_parts)
