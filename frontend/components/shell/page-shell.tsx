import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { cn } from "@/lib/utils";

export function PageShell({
  title,
  subtitle,
  children,
  backHref,
}: {
  title: string;
  subtitle?: string;
  children: React.ReactNode;
  backHref?: string;
}) {
  return (
    <main className="max-w-6xl mx-auto px-6 py-8 space-y-6">
      <div className="flex items-start justify-between gap-3">
        <div>
          <div className="flex items-center gap-2">
            {backHref ? (
              <Link href={backHref} className="text-muted-foreground hover:text-foreground flex items-center gap-1 text-sm">
                <ArrowLeft size={14} />
                Back
              </Link>
            ) : null}
          </div>
          <h1 className="text-3xl font-bold">{title}</h1>
          {subtitle ? <p className="text-muted-foreground mt-1">{subtitle}</p> : null}
        </div>
      </div>
      <div className={cn("space-y-4")}>{children}</div>
    </main>
  );
}
