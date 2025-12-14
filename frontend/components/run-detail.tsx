'use client';
import ReactMarkdown from "react-markdown";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { AgentRun } from "@/lib/types";

export function AgentRunDetail({ run }: { run: AgentRun }) {
  const memo = run.result_json?.decision_memo || "No memo available.";
  const classification = run.result_json?.failure_classification || "unknown";
  const rollout = run.result_json?.rollout_plan || "n/a";
  const testPlan = run.result_json?.test_plan?.join("\n") || "n/a";
  const actions = run.result_json?.actions_to_execute || [];

  return (
    <Card className="p-5 space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <div className="text-sm text-muted-foreground">Run #{run.id}</div>
          <div className="text-sm text-muted-foreground">
            Started {new Date(run.started_at).toLocaleString()}
          </div>
        </div>
        <Badge>{run.status}</Badge>
      </div>
      <Separator />
      <div className="grid gap-4 md:grid-cols-2">
        <Card className="p-3 space-y-2">
          <div className="text-sm text-muted-foreground">Failure classification</div>
          <div className="text-foreground">{classification}</div>
          <div className="text-sm text-muted-foreground">Actions</div>
          <div className="flex flex-wrap gap-2">
            {actions.map((a) => (
              <Badge key={a} variant="secondary">
                {a}
              </Badge>
            ))}
            {!actions.length ? <div className="text-muted-foreground text-sm">None</div> : null}
          </div>
          <div className="text-sm text-muted-foreground">Test plan</div>
          <pre className="rounded-md bg-black/30 p-2 text-xs whitespace-pre-wrap">{testPlan}</pre>
          <div className="text-sm text-muted-foreground">Rollout plan</div>
          <pre className="rounded-md bg-black/30 p-2 text-xs whitespace-pre-wrap">{rollout}</pre>
        </Card>
        <Card className="p-3">
          <div className="text-sm text-muted-foreground mb-2">Decision memo</div>
          <div className="prose prose-invert max-w-none text-sm">
            <ReactMarkdown>{memo}</ReactMarkdown>
          </div>
        </Card>
      </div>
    </Card>
  );
}
