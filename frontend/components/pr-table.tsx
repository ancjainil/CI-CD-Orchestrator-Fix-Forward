'use client';
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { useRepoStore } from "@/store/use-repo-store";
import { api } from "@/lib/api-client";
import { statusToBadge } from "@/lib/status";

export function PRTable() {
  const { repo } = useRepoStore();
  const { data } = useQuery({
    queryKey: ["prs", repo],
    queryFn: () => api.prs.list(repo || undefined),
    enabled: Boolean(repo),
  });

  return (
    <Card className="p-4">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>PR</TableHead>
            <TableHead>Author</TableHead>
            <TableHead>Branch</TableHead>
            <TableHead>Updated</TableHead>
            <TableHead>CI</TableHead>
            <TableHead>SLO</TableHead>
            <TableHead>Decision</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {data?.map((pr) => (
            <TableRow key={pr.id}>
              <TableCell>
                <Link href={`/repos/${encodeURIComponent(pr.repo || "unknown")}/prs/${pr.number}`} className="text-accent hover:underline">
                  #{pr.number} {pr.title}
                </Link>
              </TableCell>
              <TableCell>{pr.author}</TableCell>
              <TableCell>{pr.head_sha.slice(0, 7)}</TableCell>
              <TableCell>{new Date(pr.updated_at).toLocaleString()}</TableCell>
              <TableCell>
                <Badge variant={statusToBadge(pr.status)}>{pr.status}</Badge>
              </TableCell>
              <TableCell>
                <Badge variant="success">Healthy</Badge>
              </TableCell>
              <TableCell>
                <Badge variant="warning">Human review</Badge>
              </TableCell>
            </TableRow>
          ))}
          {!data?.length ? (
            <TableRow>
              <TableCell colSpan={7} className="text-muted-foreground text-center py-6">
                No pull requests yet.
              </TableCell>
            </TableRow>
          ) : null}
        </TableBody>
      </Table>
    </Card>
  );
}
