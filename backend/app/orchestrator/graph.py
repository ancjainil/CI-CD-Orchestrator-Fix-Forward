from datetime import datetime
from typing import List, Optional

from langchain_core.runnables import RunnableLambda
from langgraph.graph import END, StateGraph
from pydantic import BaseModel, Field

from ..services.github_client import GithubClient
from ..services.prom_client import PrometheusClient


class OrchestratorState(BaseModel):
    repo: str
    pr_number: int
    head_sha: Optional[str] = None
    base_sha: Optional[str] = None
    diff_summary: Optional[str] = None
    changed_files: List[str] = Field(default_factory=list)
    ci_status: Optional[str] = None
    failing_jobs: List[str] = Field(default_factory=list)
    failing_tests: List[str] = Field(default_factory=list)
    logs_excerpt: Optional[str] = None
    slo_snapshot: Optional[dict] = None
    budget_status: Optional[str] = None
    failure_classification: Optional[str] = None
    proposed_fix: Optional[dict] = None
    test_plan: Optional[List[str]] = None
    rollout_plan: Optional[str] = None
    decision_memo: Optional[str] = None
    actions_to_execute: List[str] = Field(default_factory=list)
    trace: List[str] = Field(default_factory=list)


async def fetch_pr_context(state: OrchestratorState) -> OrchestratorState:
    gh = GithubClient()
    pr = await gh.get_pr(state.repo, state.pr_number)
    files = await gh.get_files(state.repo, state.pr_number)
    await gh.close()
    summary = f"Files changed: {', '.join(files)}"
    state.head_sha = pr["head"]["sha"]
    state.base_sha = pr["base"]["sha"]
    state.diff_summary = summary
    state.changed_files = files
    state.trace.append("Fetched PR context")
    return state


async def fetch_ci_logs(state: OrchestratorState) -> OrchestratorState:
    state.ci_status = "failed"
    state.failing_jobs = ["integration-tests", "lint"]
    state.failing_tests = ["tests/integration/test_payments.py::test_refund"]
    state.logs_excerpt = "Timeout in integration suite"
    state.trace.append("Fetched CI logs")
    return state


async def failure_triage(state: OrchestratorState) -> OrchestratorState:
    if "Timeout" in (state.logs_excerpt or ""):
        state.failure_classification = "flake"
    else:
        state.failure_classification = "legit"
    state.trace.append("Classified failure")
    return state


async def test_selection(state: OrchestratorState) -> OrchestratorState:
    state.test_plan = ["pytest tests/integration/test_payments.py::test_refund"]
    state.trace.append("Selected targeted tests")
    return state


async def fix_forward(state: OrchestratorState) -> OrchestratorState:
    state.proposed_fix = {
        "patch": "--- a/service/handler.py\n+++ b/service/handler.py\n@@\n- retry=False\n+ retry=True\n",
        "rationale": "Enable retry for transient failures",
    }
    state.trace.append("Proposed fix-forward patch")
    return state


async def slo_telemetry(state: OrchestratorState) -> OrchestratorState:
    prom = PrometheusClient()
    slo = await prom.query_slo(service=state.repo.split("/")[-1])
    await prom.close()
    state.slo_snapshot = slo
    state.budget_status = "burning hot" if slo["burn_rate"] > 2 else "healthy"
    state.trace.append("Pulled SLO telemetry")
    return state


async def rollout_plan(state: OrchestratorState) -> OrchestratorState:
    slo = state.slo_snapshot or {}
    if slo.get("burn_rate", 0) > 2:
        plan = "10% → pause 30m → 25% → pause 1h → rollback if burn_rate >2"
    else:
        plan = "25% → pause 30m → 50% → 100% with flag fallback"
    state.rollout_plan = plan
    state.trace.append("Planned rollout")
    return state


async def policy_gate(state: OrchestratorState) -> OrchestratorState:
    allowed = ["comment", "check-run"]
    if state.failure_classification == "flake":
        allowed.append("rerun-checks")
    state.actions_to_execute = allowed
    state.trace.append("Applied policy gate")
    return state


async def decision_memo(state: OrchestratorState) -> OrchestratorState:
    memo = [
        f"# Decision memo for PR #{state.pr_number}",
        f"- Risk: based on burn {state.slo_snapshot.get('burn_rate') if state.slo_snapshot else 'n/a'}",
        f"- Failure classification: {state.failure_classification}",
        f"- Rollout: {state.rollout_plan}",
        f"- Actions: {', '.join(state.actions_to_execute)}",
    ]
    state.decision_memo = "\n".join(memo)
    state.trace.append("Built decision memo")
    return state


async def action_execute(state: OrchestratorState) -> OrchestratorState:
    # In production, would call GitHub comment / check-runs; here we simply log.
    state.trace.append(f"Actions executed: {', '.join(state.actions_to_execute)}")
    return state


def build_graph() -> StateGraph:
    graph = StateGraph(OrchestratorState)
    graph.add_node("pr_context", RunnableLambda(fetch_pr_context))
    graph.add_node("ci_logs", RunnableLambda(fetch_ci_logs))
    graph.add_node("triage", RunnableLambda(failure_triage))
    graph.add_node("test_selection", RunnableLambda(test_selection))
    graph.add_node("fix_forward", RunnableLambda(fix_forward))
    graph.add_node("slo", RunnableLambda(slo_telemetry))
    graph.add_node("rollout", RunnableLambda(rollout_plan))
    graph.add_node("policy", RunnableLambda(policy_gate))
    graph.add_node("memo", RunnableLambda(decision_memo))
    graph.add_node("execute", RunnableLambda(action_execute))

    graph.set_entry_point("pr_context")
    graph.add_edge("pr_context", "ci_logs")
    graph.add_edge("ci_logs", "triage")
    graph.add_edge("triage", "test_selection")
    graph.add_edge("test_selection", "fix_forward")
    graph.add_edge("fix_forward", "slo")
    graph.add_edge("slo", "rollout")
    graph.add_edge("rollout", "policy")
    graph.add_edge("policy", "memo")
    graph.add_edge("memo", "execute")
    graph.add_edge("execute", END)
    return graph


async def run_orchestrator(repo: str, pr_number: int) -> OrchestratorState:
    graph = build_graph().compile()
    result: OrchestratorState = await graph.ainvoke(
        OrchestratorState(repo=repo, pr_number=pr_number)
    )
    result.trace.append(f"Completed at {datetime.utcnow().isoformat()}Z")
    return result
