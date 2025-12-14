'use client';
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";

export function SearchFilters() {
  return (
    <div className="flex flex-wrap gap-3 items-center">
      <Input placeholder="Search PR title or author" className="w-64" />
      <Badge variant="success">Healthy</Badge>
      <Badge variant="warning">Warning</Badge>
      <Badge variant="danger">Critical</Badge>
    </div>
  );
}
