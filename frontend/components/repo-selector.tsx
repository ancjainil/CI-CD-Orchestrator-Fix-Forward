'use client';
import { useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import { Dropdown, DropdownItem } from "@/components/ui/dropdown";
import { useRepoStore } from "@/store/use-repo-store";
import { api } from "@/lib/api-client";

export function RepoSelector() {
  const { data: repos } = useQuery({
    queryKey: ["repos"],
    queryFn: () => api.repos.list(),
  });
  const { repo, setRepo } = useRepoStore();

  useEffect(() => {
    if (!repo && repos?.length) {
      setRepo(repos[0].full_name);
    }
  }, [repos, repo, setRepo]);

  const currentLabel = repo || "Select repo";

  return (
    <Dropdown label={currentLabel}>
      {repos?.map((r) => (
        <DropdownItem key={r.full_name} onSelect={() => setRepo(r.full_name)}>
          {r.full_name}
        </DropdownItem>
      ))}
      {!repos?.length ? <DropdownItem>No repos</DropdownItem> : null}
    </Dropdown>
  );
}
