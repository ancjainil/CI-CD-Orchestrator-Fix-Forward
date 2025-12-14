import pytest

from app.orchestrator.graph import OrchestratorState, policy_gate


@pytest.mark.asyncio
async def test_policy_allows_rerun_for_flake():
    state = OrchestratorState(repo="acme/payments", pr_number=1, failure_classification="flake")
    new_state = await policy_gate(state)
    assert "rerun-checks" in new_state.actions_to_execute


@pytest.mark.asyncio
async def test_policy_no_rerun_for_legit():
    state = OrchestratorState(repo="acme/payments", pr_number=1, failure_classification="legit")
    new_state = await policy_gate(state)
    assert "rerun-checks" not in new_state.actions_to_execute
