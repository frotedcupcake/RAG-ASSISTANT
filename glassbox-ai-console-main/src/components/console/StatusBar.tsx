import { cn } from "@/lib/utils";
import { Shield, AlertTriangle, XOctagon, Clock, Database, Cpu } from "lucide-react";

type GroundingStatus = 'grounded' | 'partial' | 'refused' | null;

interface StatusBarProps {
  groundingStatus: GroundingStatus;
  totalChunks: number;
  usedChunks: number;
  totalLatencyMs: number;
  className?: string;
}

export function StatusBar({
  groundingStatus,
  totalChunks,
  usedChunks,
  totalLatencyMs,
  className
}: StatusBarProps) {
  return (
    <div className={cn(
      "glass-panel flex items-center justify-between px-4 py-2",
      className
    )}>
      {/* Grounding status */}
      <div className="flex items-center gap-4">
        {groundingStatus === 'grounded' && (
          <div className="flex items-center gap-2 status-grounded">
            <Shield className="w-3.5 h-3.5" />
            <span>GROUNDED</span>
          </div>
        )}
        
        {groundingStatus === 'partial' && (
          <div className="flex items-center gap-2 status-partial">
            <AlertTriangle className="w-3.5 h-3.5" />
            <span>PARTIAL CONTEXT</span>
          </div>
        )}
        
        {groundingStatus === 'refused' && (
          <div className="flex items-center gap-2 status-refused">
            <XOctagon className="w-3.5 h-3.5" />
            <span>OUT-OF-SCOPE</span>
          </div>
        )}
        
        {!groundingStatus && (
          <div className="flex items-center gap-2 text-xs font-mono text-muted-foreground/50">
            <div className="w-1.5 h-1.5 rounded-full bg-muted-foreground/30" />
            <span>AWAITING QUERY</span>
          </div>
        )}
      </div>
      
      {/* Metrics */}
      <div className="flex items-center gap-6">
        <div className="flex items-center gap-2 text-xs font-mono text-muted-foreground">
          <Database className="w-3 h-3" />
          <span>{usedChunks}/{totalChunks} chunks</span>
        </div>
        
        <div className="flex items-center gap-2 text-xs font-mono text-muted-foreground">
          <Clock className="w-3 h-3" />
          <span>{totalLatencyMs}ms</span>
        </div>
        
        <div className="flex items-center gap-2 text-xs font-mono text-muted-foreground">
          <Cpu className="w-3 h-3" />
          <span>RAG v2.1</span>
        </div>
      </div>
    </div>
  );
}
