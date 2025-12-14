import { Card } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";

export function SkeletonTable() {
  return (
    <Card className="p-4 space-y-3">
      <Skeleton className="h-6 w-40" />
      {[...Array(5)].map((_, i) => (
        <Skeleton key={i} className="h-10 w-full" />
      ))}
    </Card>
  );
}

export function SkeletonDetail() {
  return (
    <div className="space-y-3">
      <Card className="p-4 space-y-3">
        <Skeleton className="h-6 w-52" />
        <Skeleton className="h-4 w-72" />
        <Skeleton className="h-32 w-full" />
      </Card>
    </div>
  );
}
