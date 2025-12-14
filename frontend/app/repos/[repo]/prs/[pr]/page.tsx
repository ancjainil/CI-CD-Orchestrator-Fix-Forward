import { Suspense } from "react";
import { notFound } from "next/navigation";
import { PageShell } from "@/components/shell/page-shell";
import { PRDetail } from "@/components/pr-detail";
import { SkeletonDetail } from "@/components/skeletons";
import { getPRDetail } from "@/lib/server-data";

interface Props {
  params: { repo: string; pr: string };
}

export default async function PRDetailPage({ params }: Props) {
  const repo = decodeURIComponent(params.repo);
  const prNumber = Number(params.pr);
  if (Number.isNaN(prNumber)) return notFound();

  return (
    <PageShell backHref="/dashboard" title={`PR #${prNumber}`} subtitle={`Repository: ${repo}`}>
      <Suspense fallback={<SkeletonDetail />}>
        {/* @ts-expect-error Async Server Component */}
        <PRDetail repo={repo} prNumber={prNumber} />
      </Suspense>
    </PageShell>
  );
}
