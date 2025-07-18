# agents/base_agent.py

from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """
    Abstract base class for all agents.
    All agents must inherit from this and implement required methods.
    """

    def __init__(self, config: dict):
        """
        Common init method for agents
        Args:
            config (dict): Configuration from YAML
        """
        self.id = config.get("id")
        self.name = config.get("name")
        self.description = config.get("description")
        self.config = config

    @abstractmethod
    def respond(self, session_id: str, user_input: str) -> str:
        """
        Main method to handle user input and return agent response
        Args:
            session_id (str): Unique session identifier
            user_input (str): User's message
        Returns:
            str: Agent's response
        """
        pass

    def load_resources(self):
        """
        Optional method for loading embeddings, vector DBs, or models
        """
        pass

    def cleanup(self):
        """
        Optional method to clean up after conversation ends or on shutdown
        """
        pass
