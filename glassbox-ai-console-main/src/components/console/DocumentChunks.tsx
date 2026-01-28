import { cn } from "@/lib/utils";
import { DocumentChunk } from "@/types/chat";
import { FileText, Hash } from "lucide-react";

interface DocumentChunksProps {
  chunks: DocumentChunk[];
  highlightedChunkId: string | null;
  pinnedChunkIds: string[];
  onChunkHover: (id: string | null) => void;
  onChunkClick: (id: string) => void;
  className?: string;
}

export function DocumentChunks({
  chunks,
  highlightedChunkId,
  pinnedChunkIds,
  onChunkHover,
  onChunkClick,
  className
}: DocumentChunksProps) {
  return (
    <div className={cn("space-y-2", className)}>
      <div className="flex items-center gap-2 mb-3">
        <FileText className="w-3.5 h-3.5 text-muted-foreground" />
        <h3 className="text-xs font-mono uppercase tracking-wider text-muted-foreground">
          Retrieved Chunks
        </h3>
        <span className="text-xs font-mono text-muted-foreground/60">
          ({chunks.length})
        </span>
      </div>
      
      <div className="space-y-2">
        {chunks.map((chunk) => {
          const isHighlighted = highlightedChunkId === chunk.id;
          const isPinned = pinnedChunkIds.includes(chunk.id);
          
          return (
            <div
              key={chunk.id}
              className={cn(
                "chunk-card cursor-pointer",
                !chunk.usedInAnswer && "dimmed",
                isHighlighted && "border-primary/50 bg-primary/5",
                isPinned && "border-primary bg-primary/10"
              )}
              onMouseEnter={() => onChunkHover(chunk.id)}
              onMouseLeave={() => onChunkHover(null)}
              onClick={() => onChunkClick(chunk.id)}
            >
              {/* Header */}
              <div className="flex items-center justify-between gap-2">
                <div className="flex items-center gap-1.5">
                  <Hash className="w-3 h-3 text-muted-foreground/60" />
                  <span className="text-xs font-mono text-muted-foreground">
                    {chunk.section}
                  </span>
                </div>
                
                <div className={cn(
                  "px-1.5 py-0.5 text-[10px] font-mono rounded",
                  chunk.similarityScore >= 0.8 
                    ? "bg-success/20 text-success" 
                    : chunk.similarityScore >= 0.6 
                    ? "bg-warning/20 text-warning"
                    : "bg-muted/30 text-muted-foreground"
                )}>
                  {(chunk.similarityScore * 100).toFixed(0)}%
                </div>
              </div>
              
              {/* Content preview */}
              <p className="text-xs text-muted-foreground line-clamp-3 leading-relaxed">
                {chunk.content}
              </p>
              
              {/* Footer */}
              <div className="flex items-center justify-between text-[10px] text-muted-foreground/50 font-mono">
                <span>p.{chunk.page}</span>
                {isPinned && (
                  <span className="text-primary">PINNED</span>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
