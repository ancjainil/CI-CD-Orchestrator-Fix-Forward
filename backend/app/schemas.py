from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, Field, ConfigDict


class RepoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    default_branch: str


class PullRequestOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    number: int
    title: str
    author: str
    status: str
    head_sha: str
    base_sha: str
    created_at: datetime
    updated_at: datetime


class AgentRunOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: str
    started_at: datetime
    finished_at: Optional[datetime] = None
    result_json: dict


class SLOSnapshotOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    service: str
    window: str
    latency_p95: float
    error_rate: float
    burn_rate: float
    budget_remaining: float
    created_at: datetime


class DecisionMemo(BaseModel):
    markdown: str
    risk_score: int
    rollout_plan: str
    actions: List[str]


class OrchestrateRequest(BaseModel):
    allow_autofix: bool = False


class FixForwardRequest(BaseModel):
    target_branch: Optional[str] = None


class WebhookEvent(BaseModel):
    delivery: str = Field(..., alias="X-GitHub-Delivery")
    signature: str = Field(..., alias="X-Hub-Signature-256")
    event: str = Field(..., alias="X-GitHub-Event")
    payload: Any
