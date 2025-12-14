"use client";
import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Card } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";

const apiBase = process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000";

export default function OAuthCallbackPage() {
  const router = useRouter();
  const params = useSearchParams();
  const code = params.get("code");
  const state = params.get("state");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const exchange = async () => {
      if (!code) {
        setError("Missing code");
        return;
      }
      try {
        const res = await fetch(`${apiBase}/oauth/callback?code=${encodeURIComponent(code)}&state=${encodeURIComponent(state || "")}`);
        if (!res.ok) throw new Error("OAuth exchange failed");
        const data = await res.json();
        if (data.session_token) {
          localStorage.setItem("slo_session", data.session_token);
        }
        router.replace("/dashboard");
      } catch (e: any) {
        setError(e.message || "OAuth error");
      }
    };
    exchange();
  }, [code, state, router]);

  if (error) {
    return (
      <main className="max-w-md mx-auto mt-24">
        <Card className="p-4 text-sm text-red-400">OAuth failed: {error}</Card>
      </main>
    );
  }

  return (
    <main className="max-w-md mx-auto mt-24">
      <Card className="p-4 space-y-2">
        <div className="text-sm text-muted-foreground">Finishing GitHub login...</div>
        <Skeleton className="h-2 w-32" />
      </Card>
    </main>
  );
}
