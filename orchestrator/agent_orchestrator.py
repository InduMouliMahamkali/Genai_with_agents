# orchestrator/agent_orchestrator.py

import yaml
from agents.common_agent import CommonAgent
from agents.docs_agent import DocsAgent
from sessions.session_manager import SessionManager
from sessions.interaction_logger import InteractionLogger

class AgentOrchestrator:
    def __init__(self, config_path="config/agents_config.yaml"):
        self.session_manager = SessionManager()
        self.interaction_logger = InteractionLogger()
        self.agents = self.load_agents(config_path)

    def load_agents(self, config_path):
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)

        agent_instances = {}
        for agent in config['agents']:
            name = agent['name']
            if name == 'common_agent':
                agent_instances[name] = CommonAgent(config=agent.get("config", {}))
            elif name == 'docs_agent':
                agent_instances[name] = DocsAgent()
            # Other agents can be added here
        return agent_instances

    def route_query(self, session_id: str, query: str) -> str:
        # Simple keyword-based routing
        query_lower = query.lower()
        if any(keyword in query_lower for keyword in ['policy', 'benefits', 'leave', 'salary']):
            agent_name = 'docs_agent'
        else:
            agent_name = 'common_agent'

        agent = self.agents.get(agent_name)
        if not agent:
            return "❌ No agent configured."

        if hasattr(agent, "answer_query"):
            response = agent.answer_query(query)
        else:
            response = agent.chat(query)

        self.session_manager.update_context(session_id, query, response)
        self.interaction_logger.log(session_id, query, response, agent_name)
        return response, agent_name
