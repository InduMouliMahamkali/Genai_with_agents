# orchestrator/api.py

from fastapi import FastAPI, Request
from pydantic import BaseModel
from orchestrator.agent_orchestrator import AgentOrchestrator
import yaml

# ---------- Load Config ----------
with open("config/agents_config.yaml", "r") as f:
    config = yaml.safe_load(f)

# ---------- Init Orchestrator ----------
orchestrator = AgentOrchestrator(config)

# ---------- FastAPI App ----------
app = FastAPI(title="GenAI Agent API")

class AskRequest(BaseModel):
    session_id: str
    user_input: str

@app.post("/ask")
async def ask_agent(request: AskRequest):
    response = orchestrator.handle_input(
        session_id=request.session_id,
        user_input=request.user_input
    )
    return {"response": response}
