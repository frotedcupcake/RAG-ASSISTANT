import { cn } from "@/lib/utils";
import { ChatMessage as ChatMessageType, ResponseBlock, EvidenceSentence } from "@/types/chat";
import { User, Cpu } from "lucide-react";

interface ChatMessageProps {
  message: ChatMessageType;
  highlightedChunkId: string | null;
  onSentenceHover: (chunkId: string | null) => void;
  onSentenceClick: (chunkId: string) => void;
}

interface SentenceSpanProps {
  sentence: EvidenceSentence;
  isHighlighted: boolean;
  onHover: (chunkId: string | null) => void;
  onClick: (chunkId: string) => void;
}

function SentenceSpan({ sentence, isHighlighted, onHover, onClick }: SentenceSpanProps) {
  return (
    <span
      className={cn(
        "evidence-sentence",
        sentence.confidence === 'low' && "low-confidence",
        isHighlighted && "highlighted",
        sentence.isPinned && "pinned"
      )}
      onMouseEnter={() => sentence.sourceChunkId && onHover(sentence.sourceChunkId)}
      onMouseLeave={() => onHover(null)}
      onClick={() => sentence.sourceChunkId && onClick(sentence.sourceChunkId)}
    >
      {sentence.text}{' '}
    </span>
  );
}

function ResponseBlockComponent({ 
  block, 
  highlightedChunkId,
  onSentenceHover,
  onSentenceClick
}: { 
  block: ResponseBlock;
  highlightedChunkId: string | null;
  onSentenceHover: (chunkId: string | null) => void;
  onSentenceClick: (chunkId: string) => void;
}) {
  const blockLabels = {
    summary: 'Summary',
    explanation: 'Detailed Explanation',
    evidence: 'Evidence-Backed Reasoning'
  };

  return (
    <div className="space-y-2">
      <div className="flex items-center gap-2">
        <div className="h-px flex-1 bg-border/30" />
        <span className="text-[10px] font-mono uppercase tracking-wider text-muted-foreground/60">
          {blockLabels[block.type]}
        </span>
        <div className="h-px flex-1 bg-border/30" />
      </div>
      
      <p className={cn(
        "text-sm leading-relaxed",
        block.type === 'summary' && "font-medium text-foreground",
        block.type === 'explanation' && "text-foreground/90",
        block.type === 'evidence' && "text-muted-foreground"
      )}>
        {block.sentences.map((sentence) => (
          <SentenceSpan
            key={sentence.id}
            sentence={sentence}
            isHighlighted={highlightedChunkId === sentence.sourceChunkId}
            onHover={onSentenceHover}
            onClick={onSentenceClick}
          />
        ))}
      </p>
    </div>
  );
}

export function ChatMessageComponent({
  message,
  highlightedChunkId,
  onSentenceHover,
  onSentenceClick
}: ChatMessageProps) {
  const isUser = message.role === 'user';

  return (
    <div className={cn(
      "flex gap-3 animate-fade-in",
      isUser ? "justify-end" : "justify-start"
    )}>
      {!isUser && (
        <div className="flex-shrink-0 w-8 h-8 rounded-lg bg-secondary/50 flex items-center justify-center border border-border/50">
          <Cpu className="w-4 h-4 text-primary" />
        </div>
      )}
      
      <div className={cn(
        "max-w-[80%] rounded-lg",
        isUser 
          ? "glass-panel px-4 py-3 bg-secondary/30" 
          : "space-y-4"
      )}>
        {isUser ? (
          <p className="text-sm text-foreground">{message.content}</p>
        ) : (
          <>
            {message.responseBlocks?.map((block, index) => (
              <div key={index} className="glass-panel px-4 py-3">
                <ResponseBlockComponent 
                  block={block}
                  highlightedChunkId={highlightedChunkId}
                  onSentenceHover={onSentenceHover}
                  onSentenceClick={onSentenceClick}
                />
              </div>
            )) || (
              <div className="glass-panel px-4 py-3">
                <p className="text-sm text-foreground">{message.content}</p>
              </div>
            )}
          </>
        )}
      </div>
      
      {isUser && (
        <div className="flex-shrink-0 w-8 h-8 rounded-lg bg-secondary/30 flex items-center justify-center border border-border/50">
          <User className="w-4 h-4 text-muted-foreground" />
        </div>
      )}
    </div>
  );
}
