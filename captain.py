# captain.py

from orchestrator.agent_orchestrator import AgentOrchestrator
import uvicorn
import yaml
import os

def load_config(config_path='config/agents_config.yaml'):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def main():
    print("🧠 Starting GenAI Agent Platform...")

    # Load agent configs
    config = load_config()

    # Initialize orchestrator with config
    orchestrator = AgentOrchestrator(config=config)

    print("✅ Agents Loaded:", [agent['name'] for agent in config['agents']])
    print("💬 You can now start sending messages via Streamlit UI or API (to be implemented).")

    # Placeholder CLI for basic testing (can be replaced later)
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['exit', 'quit']:
            break

        response = orchestrator.handle_input(session_id="demo_session", user_input=user_input)
        print(f"Agent: {response}")

if __name__ == "__main__":
    print("🚀 Starting FastAPI GenAI Backend at http://localhost:8000")
    uvicorn.run("orchestrator.api:app", host="0.0.0.0", port=8000, reload=True)
