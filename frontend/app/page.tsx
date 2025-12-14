import Link from "next/link";
import { Github } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { useAuthClient } from "@/lib/auth-client";

export default function LandingPage() {
  const { loginUrl } = useAuthClient();
  return (
    <main className="max-w-5xl mx-auto px-6 py-16">
      <div className="grid gap-8 md:grid-cols-[2fr,1fr] items-center">
        <div>
          <div className="text-sm uppercase tracking-[0.2em] text-muted mb-3">SLO-Driven CI/CD</div>
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            Orchestrate PRs with SLO guardrails and fix-forward automation.
          </h1>
          <p className="text-lg text-muted-foreground mb-8 max-w-2xl">
            GitHub-integrated agent that triages failures, proposes minimal patches, plans rollouts, and posts a decision
            memo. Reliability-first, with hard guardrails.
          </p>
          <div className="flex flex-wrap gap-3 items-center">
            <Link href="/dashboard">
              <Button size="lg" className="gap-2">
                <Github size={18} />
                Login with GitHub
              </Button>
            </Link>
            <a href={loginUrl} className="text-sm text-muted-foreground underline">
              Use dev stub
            </a>
          </div>
          <div className="mt-8 grid gap-3 md:grid-cols-3 text-sm text-muted-foreground">
            <div>LangGraph multi-agent</div>
            <div>Prometheus SLO gating</div>
            <div>Fix-forward PR automation</div>
          </div>
        </div>
        <Card className="p-5 space-y-3">
          <div className="text-sm text-muted-foreground">Live feed</div>
          <div className="rounded-md bg-black/30 border border-border p-3 text-xs text-muted-foreground">
            <div>• pull_request opened → risk: 0.68 → canary: 25%</div>
            <div>• check_run failed → flake → rerun triggered</div>
            <div>• memo posted → reviewer loop shortened</div>
          </div>
          <Link href="/dashboard">
            <Button variant="ghost" className="w-full">
              Go to dashboard
            </Button>
          </Link>
        </Card>
      </div>
    </main>
  );
}
