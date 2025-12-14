from datetime import datetime
from typing import Optional

from sqlalchemy import JSON, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


class Installation(Base):
    __tablename__ = "installations"
    github_installation_id: Mapped[int] = mapped_column(unique=True, index=True)
    account_login: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    repos: Mapped[list["Repo"]] = relationship(back_populates="installation")


class Repo(Base):
    __tablename__ = "repos"
    full_name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    installation_id: Mapped[int] = mapped_column(ForeignKey("installations.id"))
    default_branch: Mapped[str] = mapped_column(default="main")
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    installation: Mapped[Installation] = relationship(back_populates="repos")
    prs: Mapped[list["PullRequest"]] = relationship(back_populates="repo")


class PullRequest(Base):
    __tablename__ = "pull_requests"
    repo_id: Mapped[int] = mapped_column(ForeignKey("repos.id"))
    number: Mapped[int]
    head_sha: Mapped[str] = mapped_column(String(64))
    base_sha: Mapped[str] = mapped_column(String(64))
    title: Mapped[str] = mapped_column(String(512))
    author: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(default="open")
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    repo: Mapped[Repo] = relationship(back_populates="prs")
    agent_runs: Mapped[list["AgentRun"]] = relationship(back_populates="pull_request")


class WorkflowRun(Base):
    __tablename__ = "workflow_runs"
    repo_id: Mapped[int] = mapped_column(ForeignKey("repos.id"))
    pr_id: Mapped[Optional[int]] = mapped_column(ForeignKey("pull_requests.id"), nullable=True)
    status: Mapped[str] = mapped_column(default="pending")
    conclusion: Mapped[Optional[str]] = mapped_column(nullable=True)
    raw: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class CheckRun(Base):
    __tablename__ = "check_runs"
    workflow_run_id: Mapped[int] = mapped_column(ForeignKey("workflow_runs.id"))
    name: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(default="queued")
    conclusion: Mapped[Optional[str]] = mapped_column(nullable=True)
    log_excerpt: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class AgentRun(Base):
    __tablename__ = "agent_runs"
    pr_id: Mapped[int] = mapped_column(ForeignKey("pull_requests.id"))
    status: Mapped[str] = mapped_column(default="pending")
    started_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    finished_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    result_json: Mapped[dict] = mapped_column(JSON, default=dict)
    trace: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    pull_request: Mapped[PullRequest] = relationship(back_populates="agent_runs")
    fix_forward_patch: Mapped[Optional["FixForwardPatch"]] = relationship(back_populates="agent_run")


class SLOSnapshot(Base):
    __tablename__ = "slo_snapshots"
    service: Mapped[str] = mapped_column(String(255))
    window: Mapped[str] = mapped_column(String(64))
    latency_p95: Mapped[float]
    error_rate: Mapped[float]
    burn_rate: Mapped[float]
    budget_remaining: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class FixForwardPatch(Base):
    __tablename__ = "fix_forward_patches"
    agent_run_id: Mapped[int] = mapped_column(ForeignKey("agent_runs.id"))
    branch: Mapped[str] = mapped_column(String(255))
    pr_url: Mapped[str] = mapped_column(String(512))
    diff_summary: Mapped[str] = mapped_column(Text)
    risk_score: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    agent_run: Mapped[AgentRun] = relationship(back_populates="fix_forward_patch")
