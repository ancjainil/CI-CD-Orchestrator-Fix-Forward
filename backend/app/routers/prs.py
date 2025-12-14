from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_session
from ..models import AgentRun, PullRequest, Repo
from ..orchestrator.graph import run_orchestrator
from ..schemas import AgentRunOut, FixForwardRequest, OrchestrateRequest, PullRequestOut

router = APIRouter(prefix="/prs", tags=["prs"])


@router.get("/", response_model=list[PullRequestOut])
async def list_prs(repo: str | None = None, session: AsyncSession = Depends(get_session)):
    stmt = select(PullRequest)
    if repo:
        stmt = stmt.join(Repo).where(Repo.full_name == repo)
    result = await session.execute(stmt)
    return result.scalars().all()


@router.get("/{pr_id}", response_model=PullRequestOut)
async def get_pr(pr_id: int, session: AsyncSession = Depends(get_session)):
    pr = await session.get(PullRequest, pr_id)
    if not pr:
        raise HTTPException(status_code=404, detail="PR not found")
    return pr


@router.get("/{pr_id}/agent-runs", response_model=list[AgentRunOut])
async def get_agent_runs(pr_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(AgentRun).where(AgentRun.pr_id == pr_id))
    return result.scalars().all()


@router.post("/{pr_id}/orchestrate", response_model=AgentRunOut)
async def orchestrate(pr_id: int, _: OrchestrateRequest, session: AsyncSession = Depends(get_session)):
    pr = await session.get(PullRequest, pr_id)
    if not pr:
        raise HTTPException(status_code=404, detail="PR not found")
    agent_run = AgentRun(pr_id=pr_id, status="running", result_json={})
    session.add(agent_run)
    await session.flush()
    result_state = await run_orchestrator(repo=pr.repo.full_name if pr.repo else "unknown/repo", pr_number=pr.number)
    agent_run.status = "completed"
    agent_run.result_json = result_state.dict()
    await session.commit()
    return agent_run


@router.post("/{pr_id}/fix-forward", response_model=AgentRunOut)
async def fix_forward(pr_id: int, _: FixForwardRequest, session: AsyncSession = Depends(get_session)):
    pr = await session.get(PullRequest, pr_id)
    if not pr:
        raise HTTPException(status_code=404, detail="PR not found")
    agent_run = AgentRun(pr_id=pr_id, status="running", result_json={})
    session.add(agent_run)
    await session.flush()
    result_state = await run_orchestrator(repo=pr.repo.full_name if pr.repo else "unknown/repo", pr_number=pr.number)
    agent_run.status = "completed"
    agent_run.result_json = result_state.dict()
    await session.commit()
    return agent_run
