# orchestrator/agent_orchestrator.py

from sessions.session_manager import SessionManager
from agents.common_agent import CommonAgent
from agents.devops_agent import DevOpsAgent
from agents.itsm_agent import ITSMAgent

class AgentOrchestrator:
    def __init__(self, config):
        self.config = config
        self.session_manager = SessionManager()
        self.agents = self._initialize_agents()

    def _initialize_agents(self):
        agents = {}
        for agent_cfg in self.config.get("agents", []):
            name = agent_cfg["name"]
            if name == "common_agent":
                agents[name] = CommonAgent(agent_cfg)
            elif name == "itsm_agent":
                agents[name] = ITSMAgent(agent_cfg)
            elif name == "devops_agent":
                agents[name] = DevOpsAgent(agent_cfg)
            else:
                print(f"⚠️ Unknown agent: {name}")
        return agents

    def process(self, session_id: str, user_query: str) -> str:
        session_context = self.session_manager.get_context(session_id)

        # Basic routing logic based on keywords (can be replaced with intent detection)
        if "incident" in user_query.lower() or "ticket" in user_query.lower():
            agent = self.agents.get("itsm_agent")
        elif "update db" in user_query.lower() or "airflow" in user_query.lower():
            agent = self.agents.get("devops_agent")
        else:
            agent = self.agents.get("common_agent")

        if not agent:
            return "❌ No agent configured."

        response = agent.respond(user_query, session_context)
        self.session_manager.update_context(session_id, user_query, response)
        return response