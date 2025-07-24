# orchestrator/agent_orchestrator.py

import yaml
from sessions.session_manager import SessionManager
from sessions.interaction_logger import InteractionLogger

# importing all agents
from agents.common_agent import CommonAgent
from agents.docs_agent import DocsAgent
from agents.itsm_agent import ITSMAgent
from agents.devops_agent import DevOpsAgent
from agents.hr_agent import HRAgent
#from agents.summarizer_agent import SummarizerAgent
#from agents.multi_agent import MultiAgent


class AgentOrchestrator:
    def __init__(self, config_path="config/agents_config.yaml"):
        self.session_manager = SessionManager()
        self.logger = InteractionLogger()
        self.agents = self.load_agents(config_path)

    def load_agents(self, config_path):
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)

        agent_instances = {}
        for agent in config.get('agents', []):
            name = agent['name']
            agent_type = agent.get('type', name)  # fallback to name if type is not defined
            agent_conf = agent.get('config', {})

            if agent_type == 'common':
                agent_instances[name] = CommonAgent(config=agent_conf)

            elif agent_type == 'docs':
                agent_instances[name] = DocsAgent(config=agent_conf)

            elif agent_type == 'itsm':
                agent_instances[name] = ITSMAgent(config=agent_conf)

            elif agent_type == 'devops':
                agent_instances[name] = DevOpsAgent(config=agent_conf)

            elif agent_type == 'hr':
                agent_instances[name] = HRAgent(agent_id=name, config=agent_conf)

            #elif agent_type == 'summarizer':
             #   agent_instances[name] = SummarizerAgent(agent_id=name, config=agent_conf)

            #elif agent_type == 'multi':
             #   agent_instances[name] = MultiAgent(agent_id=name, config=agent_conf)

            else:
                print(f"⚠️ Unknown agent type '{agent_type}' for '{name}' – skipping.")

        return agent_instances

    def route_query(self, session_id, query):
        query_lower = query.lower()

        # === Agent Routing Rules ===

        # ITSM Agent
        itsm_keywords = ['incident', 'ticket', 'issue', 'servicenow', 'jira', 'status', 'outage', 'escalation', 'impact']
        if any(kw in query_lower for kw in itsm_keywords):
            response = self.agents['itsm_agent'].answer_query(query, session_id=session_id)
            return self._log(session_id, query, response, "itsm_agent")

        # Docs Agent
        doc_keywords = ['policy', 'document', 'handbook', 'guideline']
        if any(kw in query_lower for kw in doc_keywords):
            response = self.agents['docs_agent'].answer_query(query)
            return self._log(session_id, query, response, "docs_agent")

        # DevOps Agent
        devops_keywords = ['etl', 'pipeline', 'dashboard', 'sync db', 'kpi', 'metrics', 'refresh database']
        if any(kw in query_lower for kw in devops_keywords):
            response = self.agents['devops_agent'].answer_query(query)
            return self._log(session_id, query, response, "devops_agent")

        # HR Agent
        hr_keywords = ['leave', 'salary', 'appraisal', 'holiday', 'hike', 'pay']
        if any(kw in query_lower for kw in hr_keywords):
            response = self.agents['hr_agent'].answer_query(query, session_id=session_id)
            return self._log(session_id, query, response, "hr_agent")

        # Summarizer Agent
        #if "summary" in query_lower or "summarize" in query_lower:
         #   response = self.agents['summarizer_agent'].answer_query(query)
          #  return self._log(session_id, query, response, "summarizer_agent")

        # Multi Agent (composite)
        #if "use multiple agents" in query_lower or "composite task" in query_lower:
         #   response = self.agents['multi_agent'].answer_query(query, session_id=session_id)
          #  return self._log(session_id, query, response, "multi_agent")

        # Fallback to Common Agent
        response = self.agents['common_agent'].answer_query(query)
        return self._log(session_id, query, response, "common_agent")

    def _log(self, session_id, query, response, agent_id):
        self.session_manager.update_context(session_id, query, response)
        self.logger.log(session_id, query, response, agent_id=agent_id)
        return response
