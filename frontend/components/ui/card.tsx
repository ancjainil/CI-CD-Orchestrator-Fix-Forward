import * as React from "react";
import { cn } from "@/lib/utils";

export const Card = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn(
        "rounded-lg border border-border bg-card/90 text-card-foreground shadow-card backdrop-blur supports-[backdrop-filter]:bg-card/80",
        className,
      )}
      {...props}
    />
  ),
);
Card.displayName = "Card";
