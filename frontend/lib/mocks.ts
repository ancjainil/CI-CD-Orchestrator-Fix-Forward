import { AgentRun, PullRequest, Repo } from "./types";

export const mockRepos: Repo[] = [
  { id: 1, full_name: "acme/payments", default_branch: "main" },
  { id: 2, full_name: "acme/checkout", default_branch: "main" },
];

export const mockPRs: PullRequest[] = [
  {
    id: 1,
    number: 42,
    title: "Improve retry handling",
    author: "octocat",
    status: "open",
    head_sha: "abc1234",
    base_sha: "def5678",
    updated_at: new Date().toISOString(),
    repo: "acme/payments",
  },
];

export const mockRuns: AgentRun[] = [
  {
    id: 1,
    status: "completed",
    started_at: new Date().toISOString(),
    finished_at: new Date().toISOString(),
    result_json: {
      failure_classification: "flake",
      rollout_plan: "25% → 50% → 100%",
      test_plan: ["pytest tests/integration/test_payments.py::test_refund"],
      decision_memo: "# Decision memo\n- Risk: moderate\n- Actions: comment, rerun",
      actions_to_execute: ["comment", "rerun-checks"],
    },
  },
];
