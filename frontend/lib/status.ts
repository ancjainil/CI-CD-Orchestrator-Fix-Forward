import { BadgeProps } from "@/components/ui/badge";

export function statusToBadge(status: string): BadgeProps["variant"] {
  const s = status?.toLowerCase() || "";
  if (s.includes("fail") || s.includes("blocked")) return "danger";
  if (s.includes("pending") || s.includes("running")) return "warning";
  return "success";
}
