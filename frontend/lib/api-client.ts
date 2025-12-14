import { z } from "zod";
import { mockRepos, mockPRs, mockRuns } from "./mocks";
import { AgentRun, PullRequest, Repo } from "./types";

const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000";

async function fetchJSON<T>(path: string, init?: RequestInit): Promise<T> {
  try {
    const res = await fetch(`${baseUrl}${path}`, {
      ...init,
      headers: {
        "Content-Type": "application/json",
        ...(init?.headers || {}),
      },
      cache: "no-store",
    });
    if (!res.ok) throw new Error(`status ${res.status}`);
    return (await res.json()) as T;
  } catch (err) {
    console.warn("API fallback to mock", path, err);
    throw err;
  }
}

const repoSchema = z.object({
  id: z.number(),
  full_name: z.string(),
  default_branch: z.string(),
});

const prSchema = z.object({
  id: z.number(),
  number: z.number(),
  title: z.string(),
  author: z.string(),
  status: z.string(),
  head_sha: z.string(),
  base_sha: z.string(),
  updated_at: z.string(),
  repo: z.string().optional(),
});

const runSchema = z.object({
  id: z.number(),
  status: z.string(),
  started_at: z.string(),
  finished_at: z.string().nullish(),
  result_json: z.record(z.any()).default({}),
});

function fallback<T>(value: T): () => T {
  return () => value;
}

export const api = {
  repos: {
    list: async (): Promise<Repo[]> => {
      try {
        const data = await fetchJSON<unknown>("/repos/");
        return z.array(repoSchema).parse(data);
      } catch {
        return mockRepos;
      }
    },
  },
  prs: {
    list: async (repo?: string): Promise<PullRequest[]> => {
      try {
        const path = repo ? `/prs?repo=${encodeURIComponent(repo)}` : "/prs";
        const data = await fetchJSON<unknown>(path);
        return z.array(prSchema).parse(data);
      } catch {
        return mockPRs.filter((pr) => !repo || pr.repo === repo);
      }
    },
    getById: async (id: number): Promise<PullRequest> => {
      try {
        const data = await fetchJSON<unknown>(`/prs/${id}`);
        return prSchema.parse(data);
      } catch {
        const found = mockPRs.find((p) => p.id === id || p.number === id);
        if (!found) throw new Error("PR not found");
        return found;
      }
    },
  },
  agentRuns: {
    listForPR: async (prId: number): Promise<AgentRun[]> => {
      try {
        const data = await fetchJSON<unknown>(`/prs/${prId}/agent-runs`);
        return z.array(runSchema).parse(data);
      } catch {
        return mockRuns;
      }
    },
    get: async (id: number): Promise<AgentRun | null> => {
      try {
        const data = await fetchJSON<unknown>(`/agent-runs/${id}`);
        return runSchema.parse(data);
      } catch {
        return mockRuns.find((r) => r.id === id) || null;
      }
    },
  },
  actions: {
    orchestrate: async (prId: number) => {
      return fetchJSON(`/prs/${prId}/orchestrate`, { method: "POST", body: JSON.stringify({ allow_autofix: true }) });
    },
    fixForward: async (prId: number) => {
      return fetchJSON(`/prs/${prId}/fix-forward`, { method: "POST", body: JSON.stringify({}) });
    },
  },
};
