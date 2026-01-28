import { cn } from "@/lib/utils";
import { PipelineStep } from "@/types/chat";
import { 
  Search, 
  Database, 
  Filter, 
  Merge, 
  ArrowUpDown, 
  Sparkles,
  Check,
  Loader2,
  Circle
} from "lucide-react";

interface PipelineInspectorProps {
  steps: PipelineStep[];
  className?: string;
}

const stepIcons: Record<string, typeof Search> = {
  query: Search,
  vector: Database,
  bm25: Filter,
  fusion: Merge,
  rerank: ArrowUpDown,
  generate: Sparkles
};

const stepColors: Record<string, string> = {
  query: "text-pipeline-query",
  vector: "text-pipeline-vector",
  bm25: "text-pipeline-bm25",
  fusion: "text-pipeline-fusion",
  rerank: "text-pipeline-rerank",
  generate: "text-pipeline-generate"
};

export function PipelineInspector({ steps, className }: PipelineInspectorProps) {
  return (
    <div className={cn("space-y-1", className)}>
      <div className="flex items-center gap-2 mb-3">
        <div className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse-glow" />
        <h3 className="text-xs font-mono uppercase tracking-wider text-muted-foreground">
          Execution Trace
        </h3>
      </div>
      
      <div className="space-y-0.5">
        {steps.map((step, index) => {
          const Icon = stepIcons[step.id] || Circle;
          const colorClass = stepColors[step.id] || "text-muted-foreground";
          
          return (
            <div
              key={step.id}
              className={cn(
                "pipeline-step rounded transition-colors duration-200",
                step.status === 'active' && "bg-secondary/50",
                step.status === 'complete' && "opacity-80",
                step.status === 'pending' && "opacity-40"
              )}
            >
              <div className="flex items-center gap-2 flex-1">
                <div className={cn("relative", colorClass)}>
                  {step.status === 'active' ? (
                    <Loader2 className="w-3.5 h-3.5 animate-spin" />
                  ) : step.status === 'complete' ? (
                    <Check className="w-3.5 h-3.5" />
                  ) : (
                    <Icon className="w-3.5 h-3.5" />
                  )}
                </div>
                
                <span className={cn(
                  "flex-1 text-xs",
                  step.status === 'active' && "text-foreground",
                  step.status === 'complete' && "text-muted-foreground",
                  step.status === 'pending' && "text-muted-foreground/50"
                )}>
                  {step.name}
                </span>
                
                {step.latencyMs !== undefined && step.status === 'complete' && (
                  <span className="text-xs font-mono text-muted-foreground/70">
                    {step.latencyMs}ms
                  </span>
                )}
              </div>
              
              {step.status === 'active' && (
                <div className="progress-bar mt-1.5">
                  <div className="progress-bar-fill w-2/3" />
                </div>
              )}
            </div>
          );
        })}
      </div>
      
      {/* Connection lines */}
      <div className="absolute left-[1.1rem] top-12 bottom-4 w-px bg-border/50 -z-10" />
    </div>
  );
}
