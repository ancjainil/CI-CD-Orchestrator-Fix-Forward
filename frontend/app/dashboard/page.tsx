import { Suspense } from "react";
import { RepoSelector } from "@/components/repo-selector";
import { PRTable } from "@/components/pr-table";
import { PageShell } from "@/components/shell/page-shell";
import { SearchFilters } from "@/components/search-filters";
import { SkeletonTable } from "@/components/skeletons";

export default function DashboardPage() {
  return (
    <PageShell title="Dashboard" subtitle="Track PRs, CI state, SLO health, and agent decisions.">
      <div className="flex flex-wrap gap-3 items-center justify-between">
        <RepoSelector />
        <SearchFilters />
      </div>
      <Suspense fallback={<SkeletonTable />}>
        <PRTable />
      </Suspense>
    </PageShell>
  );
}
