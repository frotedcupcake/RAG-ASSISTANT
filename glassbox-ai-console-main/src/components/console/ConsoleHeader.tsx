import { cn } from "@/lib/utils";
import { Hexagon, ChevronLeft, ChevronRight, Settings } from "lucide-react";
interface ConsoleHeaderProps {
  leftPanelOpen: boolean;
  onToggleLeftPanel: () => void;
  className?: string;
}
export function ConsoleHeader({
  leftPanelOpen,
  onToggleLeftPanel,
  className
}: ConsoleHeaderProps) {
  return <header className={cn("glass-panel flex items-center justify-between px-4 py-3", className)}>
      {/* Logo / Title */}
      <div className="flex items-center gap-3">
        <div className="relative">
          <Hexagon className="w-8 h-8 text-primary" strokeWidth={1.5} />
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="w-2 h-2 rounded-full bg-primary animate-pulse-glow" />
          </div>
        </div>
        <div>
          <h1 className="text-sm font-semibold tracking-tight text-foreground">Glass-Box RAG</h1>
          <p className="text-[10px] font-mono text-muted-foreground uppercase tracking-wider">
            RAG Console v2.1
          </p>
        </div>
      </div>
      
      {/* Controls */}
      <div className="flex items-center gap-2">
        <button onClick={onToggleLeftPanel} className={cn("flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-mono", "transition-all duration-200", leftPanelOpen ? "bg-secondary/50 text-foreground" : "text-muted-foreground hover:text-foreground hover:bg-secondary/30")}>
          {leftPanelOpen ? <ChevronLeft className="w-3.5 h-3.5" /> : <ChevronRight className="w-3.5 h-3.5" />}
          <span>Sources</span>
        </button>
        
        <button className="p-2 rounded-lg text-muted-foreground hover:text-foreground hover:bg-secondary/30 transition-colors">
          <Settings className="w-4 h-4" />
        </button>
      </div>
    </header>;
}