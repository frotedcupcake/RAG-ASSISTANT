import { cn } from "@/lib/utils";
import { ReactNode } from "react";

interface GlassPanelProps {
  children: ReactNode;
  className?: string;
  glow?: boolean;
}

export function GlassPanel({ children, className, glow = false }: GlassPanelProps) {
  return (
    <div
      className={cn(
        glow ? "glass-panel-glow" : "glass-panel",
        "rounded-lg",
        className
      )}
    >
      {children}
    </div>
  );
}
