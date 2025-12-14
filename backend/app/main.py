from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .logging_config import setup_logging
from .routers import agent_runs, health, prs, repos, stream, webhooks


def create_app() -> FastAPI:
    settings = get_settings()
    setup_logging(settings.log_level)

    app = FastAPI(title="SLO-Driven CI/CD Orchestrator", version="0.1.0")
    app.include_router(health.router)
    app.include_router(webhooks.router)
    app.include_router(repos.router)
    app.include_router(prs.router)
    app.include_router(agent_runs.router)
    app.include_router(stream.router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


app = create_app()
