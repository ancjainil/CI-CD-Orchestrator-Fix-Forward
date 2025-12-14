# CI/CD Orchestrator + Fix-Forward (MVP)

SLO-driven CI/CD assistant that ingests GitHub webhooks, triages CI failures via a LangGraph workflow, proposes fix-forward patches, plans rollouts, and posts decision memos. Frontend is a Next.js devtools UI; backend is FastAPI + Postgres + Celery.

What’s inside
-------------
- **Backend** (`backend/`): FastAPI REST + SSE, GitHub webhook verification, LangGraph orchestrator, SQLAlchemy models with Alembic migrations, Celery worker, Prometheus + GitHub clients (mock-friendly).
- **Frontend** (`frontend/`): Next.js App Router, Tailwind/shadcn-style UI, React Query, Zustand, Recharts, mock fallback when API unavailable.
- **Ops**: Dockerfile for API, docker-compose for Postgres/Redis/prom mock/api/worker, GitHub Actions CI, env example, Makefile shortcuts.

Quick start (backend)
---------------------
Prereqs: Python 3.11, Docker (optional).

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate      # on Windows; source .venv/bin/activate on macOS/Linux
python -m pip install --upgrade pip
pip install -r requirements.txt
alembic upgrade head          # requires Postgres up (see docker-compose)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
Celery worker (optional):
```bash
celery -A app.tasks worker --loglevel=info
```
Using docker-compose (Postgres, Redis, Prom mock, API, worker):
```bash
docker-compose up --build
```

Quick start (frontend)
----------------------
```bash
cd frontend
npm install
set NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000   # PowerShell; export for bash
npm run dev
```
Open http://localhost:3000.

Key endpoints (backend)
-----------------------
- `POST /webhooks/github` (HMAC verified)
- `GET /health`
- `GET /repos`, `GET /prs`, `GET /prs/{id}`, `GET /prs/{id}/agent-runs`
- `POST /prs/{id}/orchestrate`, `POST /prs/{id}/fix-forward`
- `GET /agent-runs/{id}`
- `GET /stream` (SSE heartbeat; extend for live updates)

LangGraph workflow (mocked for now)
-----------------------------------
PR context → CI logs → Failure triage → Test selection → Fix-forward patch → SLO telemetry → Rollout planner → Policy gate → Decision memo → Action executor. Actions are guardrailed (comment/check-run/open bot PR/rerun only).

Notes
-----
- GitHub and Prometheus clients are stubbed; wire real tokens/queries to go beyond mock mode.
- Use Python 3.11 to avoid building pydantic-core from source on unsupported versions.
- Frontend falls back to fixtures if the API is unreachable.
- For OAuth login: set `NEXT_PUBLIC_GITHUB_CLIENT_ID` and `NEXT_PUBLIC_APP_URL`, and configure GitHub App redirect to `/oauth/callback`.
