from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_session
from ..models import AgentRun
from ..schemas import AgentRunOut

router = APIRouter(prefix="/agent-runs", tags=["agent-runs"])


@router.get("/{agent_run_id}", response_model=AgentRunOut)
async def get_agent_run(agent_run_id: int, session: AsyncSession = Depends(get_session)):
    agent_run = await session.get(AgentRun, agent_run_id)
    if not agent_run:
        raise HTTPException(status_code=404, detail="Agent run not found")
    return agent_run
