# orchestrator/api.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from orchestrator.agent_orchestrator import AgentOrchestrator

router = APIRouter()

# This will be set by captain.py
orchestrator: AgentOrchestrator = None

class QueryInput(BaseModel):
    session_id: str
    user_query: str

@router.post("/query")
async def handle_query(input_data: QueryInput):
    if orchestrator is None:
        raise HTTPException(status_code=500, detail="Orchestrator not initialized.")
    try:
        response = orchestrator.process(input_data.session_id, input_data.user_query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
