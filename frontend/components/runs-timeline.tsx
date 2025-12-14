'use client';
import Link from "next/link";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { statusToBadge } from "@/lib/status";
import { AgentRun } from "@/lib/types";

export function AgentRunsTimeline({ runs }: { runs: AgentRun[] }) {
  return (
    <Card className="p-4">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-lg font-semibold">Agent runs</h3>
      </div>
      <div className="space-y-3">
        {runs.map((run) => (
          <Link key={run.id} href={`/agent-runs/${run.id}`} className="block rounded-md border border-border p-3 hover:border-accent transition-colors">
            <div className="flex items-center justify-between">
              <div className="text-sm text-muted-foreground">
                Started {new Date(run.started_at).toLocaleString()}
              </div>
              <Badge variant={statusToBadge(run.status)}>{run.status}</Badge>
            </div>
            <div className="text-sm mt-1 text-foreground">Decision: {run.result_json?.decision_memo || "pending"}</div>
          </Link>
        ))}
        {!runs.length ? <div className="text-muted-foreground text-sm">No runs yet.</div> : null}
      </div>
    </Card>
  );
}
