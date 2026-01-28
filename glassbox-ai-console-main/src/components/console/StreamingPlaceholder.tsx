import { cn } from "@/lib/utils";
import { Cpu } from "lucide-react";

interface StreamingPlaceholderProps {
  className?: string;
}

export function StreamingPlaceholder({ className }: StreamingPlaceholderProps) {
  return (
    <div className={cn("flex gap-3 animate-fade-in", className)}>
      <div className="flex-shrink-0 w-8 h-8 rounded-lg bg-secondary/50 flex items-center justify-center border border-border/50">
        <Cpu className="w-4 h-4 text-primary animate-pulse" />
      </div>
      
      <div className="flex-1 space-y-4 max-w-[80%]">
        {/* Summary block skeleton */}
        <div className="glass-panel px-4 py-3 space-y-3">
          <div className="flex items-center gap-2">
            <div className="h-px flex-1 bg-border/30" />
            <span className="text-[10px] font-mono uppercase tracking-wider text-muted-foreground/40">
              Summary
            </span>
            <div className="h-px flex-1 bg-border/30" />
          </div>
          <div className="space-y-2">
            <div className="skeleton-line w-full" />
            <div className="skeleton-line w-4/5" />
          </div>
        </div>
        
        {/* Explanation block skeleton */}
        <div className="glass-panel px-4 py-3 space-y-3">
          <div className="flex items-center gap-2">
            <div className="h-px flex-1 bg-border/30" />
            <span className="text-[10px] font-mono uppercase tracking-wider text-muted-foreground/40">
              Processing
            </span>
            <div className="h-px flex-1 bg-border/30" />
          </div>
          <div className="space-y-2">
            <div className="skeleton-line w-full" />
            <div className="skeleton-line w-11/12" />
            <div className="skeleton-line w-3/4" />
          </div>
        </div>
        
        {/* Progress indicator */}
        <div className="flex items-center gap-2 px-2">
          <div className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse" />
          <span className="text-xs font-mono text-muted-foreground/60">
            Generating response...
          </span>
        </div>
      </div>
    </div>
  );
}
