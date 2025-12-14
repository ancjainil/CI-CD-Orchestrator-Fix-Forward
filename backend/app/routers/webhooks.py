import json
from fastapi import APIRouter, Depends, Header, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import get_settings
from ..db import get_session
from ..models import AgentRun, PullRequest, Repo, WorkflowRun
from ..services.github_client import verify_signature

router = APIRouter()


@router.post("/webhooks/github")
async def github_webhook(
    request: Request,
    x_hub_signature_256: str = Header(None, alias="X-Hub-Signature-256"),
    x_github_event: str = Header(..., alias="X-GitHub-Event"),
    x_github_delivery: str = Header(..., alias="X-GitHub-Delivery"),
    session: AsyncSession = Depends(get_session),
):
    settings = get_settings()
    body = await request.body()
    if not verify_signature(body, x_hub_signature_256, settings.github_webhook_secret):
        raise HTTPException(status_code=401, detail="Invalid signature")

    payload = await request.json()
    repo_full = payload.get("repository", {}).get("full_name", "unknown/unknown")
    pr_number = payload.get("pull_request", {}).get("number")
    result = await session.execute(select(Repo).where(Repo.full_name == repo_full))
    repo = result.scalar_one_or_none()
    if not repo:
        repo = Repo(full_name=repo_full, installation_id=None, default_branch="main")
        session.add(repo)
        await session.flush()

    event_record = WorkflowRun(
        repo_id=repo.id,
        pr_id=None,
        status="received",
        raw={"event": x_github_event, "delivery": x_github_delivery, "payload": payload},
    )
    session.add(event_record)

    if pr_number:
        pr = PullRequest(
            repo_id=repo.id,
            number=pr_number,
            head_sha=payload["pull_request"]["head"]["sha"],
            base_sha=payload["pull_request"]["base"]["sha"],
            title=payload["pull_request"]["title"],
            author=payload["pull_request"]["user"]["login"],
        )
        session.add(pr)
        await session.flush()
        session.add(AgentRun(pr_id=pr.id, status="queued", result_json={}))
        if x_github_event == "pull_request":
            try:
                from ..tasks import orchestrate_pr

                orchestrate_pr.delay(repo_full, pr_number)
            except Exception:
                # Celery broker may be absent in dev; ignore
                pass
    await session.commit()
    return {"ok": True, "event": x_github_event, "delivery": x_github_delivery}
