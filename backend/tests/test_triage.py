import pytest

from app.orchestrator.graph import OrchestratorState, failure_triage


@pytest.mark.asyncio
async def test_failure_triage_classifies_flake():
    state = OrchestratorState(repo="acme/payments", pr_number=1, logs_excerpt="Timeout in job")
    new_state = await failure_triage(state)
    assert new_state.failure_classification == "flake"


@pytest.mark.asyncio
async def test_failure_triage_classifies_legit():
    state = OrchestratorState(repo="acme/payments", pr_number=1, logs_excerpt="Null pointer")
    new_state = await failure_triage(state)
    assert new_state.failure_classification == "legit"
