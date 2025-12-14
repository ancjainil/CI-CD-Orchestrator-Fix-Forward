export type Repo = {
  id: number;
  full_name: string;
  default_branch: string;
};

export type PullRequest = {
  id: number;
  number: number;
  title: string;
  author: string;
  status: string;
  head_sha: string;
  base_sha: string;
  updated_at: string;
  repo?: string;
};

export type AgentRun = {
  id: number;
  status: string;
  started_at: string;
  finished_at?: string | null;
  result_json: Record<string, any>;
};

export type PRDetailData = {
  pr: PullRequest;
  runs: AgentRun[];
};
