# captain.py

from fastapi import FastAPI
from orchestrator.api import router as orchestrator_router
from orchestrator.agent_orchestrator import AgentOrchestrator
import yaml
import os

# Create the FastAPI app
app = FastAPI(
    title="GenAI Agent App",
    description="Multi-Agent Orchestrator for Enterprise GenAI",
    version="3.4.0"
)

# Load configuration
CONFIG_PATH = os.path.join("config", "agents_config.yaml")
with open(CONFIG_PATH, "r") as f:
    agent_config = yaml.safe_load(f)

# Initialize the orchestrator
orchestrator = AgentOrchestrator(config=agent_config)

# Attach orchestrator to router so endpoints have access
orchestrator_router.orchestrator = orchestrator

# Register API endpoints
app.include_router(orchestrator_router)

# Optional root health check route
@app.get("/")
def root():
    return {"message": "Welcome to the GenAI Agent API!"}


# ✅ This allows manual execution with: python captain.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("captain:app", host="0.0.0.0", port=8000, reload=True)
