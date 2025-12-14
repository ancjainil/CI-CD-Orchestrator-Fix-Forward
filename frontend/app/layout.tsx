import type { Metadata } from "next";
import "./globals.css";
import { ReactQueryProvider } from "@/components/providers/react-query-provider";
import { cn } from "@/lib/utils";

export const metadata: Metadata = {
  title: "SLO Orchestrator",
  description: "SLO-driven CI/CD orchestrator + fix-forward",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={cn("min-h-screen bg-background text-foreground font-sans")}>
        <ReactQueryProvider>{children}</ReactQueryProvider>
      </body>
    </html>
  );
}
