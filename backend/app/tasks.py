from .orchestrator.graph import run_orchestrator
from .worker import celery_app


@celery_app.task(name="orchestrate-pr")
def orchestrate_pr(repo: str, pr_number: int) -> dict:
    # Celery is sync; invoke async orchestrator via asyncio.run
    import asyncio

    state = asyncio.run(run_orchestrator(repo=repo, pr_number=pr_number))
    return state.dict()
