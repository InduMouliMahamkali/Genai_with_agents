# orchestrator/agent_orchestrator.py

import importlib
from typing import Dict, Any
from sessions.session_manager import SessionManager


class AgentOrchestrator:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.agents = {}
        self.load_agents()

    def load_agents(self):
        for agent_cfg in self.config.get('agents', []):
            if agent_cfg.get("active"):
                module_path = agent_cfg["module"]
                class_name = agent_cfg["class"]
                agent_id = agent_cfg["id"]

                try:
                    module = importlib.import_module(module_path)
                    agent_class = getattr(module, class_name)
                    self.agents[agent_id] = agent_class(config=agent_cfg)
                except Exception as e:
                    print(f"❌ Error loading {class_name} from {module_path}: {e}")

    def handle_input(self, session_id: str, user_input: str) -> str:
        # For now, route everything to the common agent
        agent = self.agents.get("common_agent")
        if not agent:
            return "No active agent found."
        
        response = agent.respond(session_id=session_id, user_input=user_input)

        self.session_manager.log_interaction(
            session_id=session_id,
            user_input=user_input,
            agent_response=response,
            agent_id="common_agent"
        )

        return response

        
