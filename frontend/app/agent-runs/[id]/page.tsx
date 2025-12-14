import { notFound } from "next/navigation";
import { PageShell } from "@/components/shell/page-shell";
import { AgentRunDetail } from "@/components/run-detail";
import { getAgentRun } from "@/lib/server-data";

interface Props {
  params: { id: string };
}

export default async function AgentRunPage({ params }: Props) {
  const id = Number(params.id);
  if (Number.isNaN(id)) return notFound();
  const run = await getAgentRun(id);
  if (!run) return notFound();
  return (
    <PageShell backHref="/dashboard" title={`Agent run #${id}`} subtitle="Decision memo and audit trail.">
      <AgentRunDetail run={run} />
    </PageShell>
  );
}
