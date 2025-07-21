# orchestrator/agent_orchestrator.py

import yaml
from agents.common_agent import CommonAgent
from agents.docs_agent import DocsAgent
from sessions.session_manager import SessionManager
from sessions.interaction_logger import InteractionLogger
from agents.itsm_agent import ITSMAgent
from agents.devops_agent import DevOpsAgent


class AgentOrchestrator:
    def __init__(self, config_path="config/agents_config.yaml"):
        self.session_manager = SessionManager()
        self.logger = InteractionLogger()
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
            elif name == 'itsm_agent':
                agent_instances[name] = ITSMAgent()
            elif name == 'devops_agent':
                agent_instances[name] = DevOpsAgent()
            # Other agents can be added here
        return agent_instances

    def route_query(self, session_id, query):
        query_lower = query.lower()

        # Route to ITSM Agent
        itsm_keywords = ['incident', 'ticket', 'issue', 'servicenow', 'jira', 'status', 'outage', 'escalation', 'impact']
        if any(kw in query_lower for kw in itsm_keywords):
            response = self.agents['itsm_agent'].answer_query(query)
            self.session_manager.update_context(session_id, query, response)
            self.logger.log(session_id, query, response, agent_id="itsm_agent")
            return response

        # Route to Docs Agent
        doc_keywords = ['policy', 'benefits', 'leave', 'salary', 'document', 'kpi']
        if any(kw in query_lower for kw in doc_keywords):
            response = self.agents['docs_agent'].answer_query(query)
            self.session_manager.update_context(session_id, query, response)
            self.logger.log(session_id, query, response, agent_id="docs_agent")
            return response

        # Route to DevOps Agent
        devops_keywords = ["run etl", "etl", "execute pipeline", "pipeline",
                            "sync db", "sync database", "update database", "refresh database",
                            "update dashboard", "refresh dashboard", "dashboard",
                            "kpi", "show kpi", "metric", "report", "kpi report"
]
        if any(kw in query_lower for kw in devops_keywords):
            response = self.agents['devops_agent'].answer_query(query)
            self.session_manager.update_context(session_id, query, response)
            self.logger.log(session_id, query, response, agent_id="devops_agent")
            return response

        
        # Fallback to Common Agent
        
        response = self.agents['common_agent'].answer_query(query)
        self.session_manager.update_context(session_id, query, response)
        self.logger.log(session_id, query, response, agent_id="common_agent")
        return response
