import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { SLOChart } from "@/components/slo-chart";
import { AgentRunsTimeline } from "@/components/runs-timeline";
import { api } from "@/lib/api-client";
import { statusToBadge } from "@/lib/status";
import { PRDetailData } from "@/lib/types";

async function getData(repo: string, prNumber: number): Promise<PRDetailData> {
  const pr = await api.prs.getById(prNumber);
  const runs = await api.agentRuns.listForPR(prNumber);
  return { pr, runs };
}

export async function PRDetail({ repo, prNumber }: { repo: string; prNumber: number }) {
  const data = await getData(repo, prNumber);
  const pr = data.pr;
  return (
    <div className="space-y-4">
      <Card className="p-4 space-y-3">
        <div className="flex flex-wrap items-center gap-3 justify-between">
          <div>
            <div className="text-sm text-muted-foreground">#{pr.number}</div>
            <h2 className="text-2xl font-semibold">{pr.title}</h2>
            <div className="text-sm text-muted-foreground">
              {pr.author} • updated {new Date(pr.updated_at).toLocaleString()}
            </div>
          </div>
          <div className="flex gap-2">
            <Badge variant={statusToBadge(pr.status)}>{pr.status}</Badge>
            <Badge variant="warning">Human review</Badge>
          </div>
        </div>
        <Separator />
        <div className="grid gap-4 md:grid-cols-2">
          <Card className="p-3">
            <div className="text-sm text-muted-foreground mb-2">CI failures</div>
            <div className="text-sm text-foreground">integration-tests, lint</div>
            <details className="mt-2 text-sm text-muted-foreground">
              <summary>Logs excerpt</summary>
              <div className="mt-2 rounded-md bg-black/30 p-2 text-xs">Timeout in integration suite</div>
            </details>
          </Card>
          <Card className="p-3">
            <div className="text-sm text-muted-foreground mb-2">SLOs</div>
            <div className="flex gap-2 items-center">
              <Badge variant="success">Budget 73%</Badge>
              <Badge variant="warning">Burn 1.2x</Badge>
            </div>
            <SLOChart />
          </Card>
        </div>
        <Separator />
        <div className="flex flex-wrap gap-2">
          <Button>Run Orchestrator</Button>
          <Button variant="secondary">Fix-Forward</Button>
          <Button variant="secondary">Explain Decision</Button>
          <Button variant="secondary">Generate Rollout Plan</Button>
        </div>
      </Card>

      <AgentRunsTimeline runs={data.runs} />
    </div>
  );
}
