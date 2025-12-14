import { api } from "./api-client";

export async function getPRDetail(prId: number) {
  return api.prs.getById(prId);
}

export async function getAgentRun(id: number) {
  return api.agentRuns.get(id);
}
