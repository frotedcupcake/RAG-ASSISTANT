import { cn } from "@/lib/utils";
import { useState, KeyboardEvent } from "react";
import { Send, Command } from "lucide-react";

interface ChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
  className?: string;
}

export function ChatInput({ onSend, disabled, className }: ChatInputProps) {
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (input.trim() && !disabled) {
      onSend(input.trim());
      setInput("");
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className={cn("glass-panel p-3", className)}>
      <div className="flex items-end gap-3">
        <div className="flex-1 relative">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Enter your query..."
            disabled={disabled}
            rows={1}
            className={cn(
              "w-full bg-transparent text-sm text-foreground placeholder:text-muted-foreground/50",
              "resize-none focus:outline-none",
              "min-h-[24px] max-h-[120px]",
              disabled && "opacity-50 cursor-not-allowed"
            )}
            style={{ height: 'auto' }}
          />
        </div>
        
        <div className="flex items-center gap-2">
          <div className="hidden sm:flex items-center gap-1 text-[10px] font-mono text-muted-foreground/40">
            <Command className="w-3 h-3" />
            <span>+ Enter</span>
          </div>
          
          <button
            onClick={handleSend}
            disabled={!input.trim() || disabled}
            className={cn(
              "p-2 rounded-lg transition-all duration-200",
              "bg-primary/10 hover:bg-primary/20 text-primary",
              "disabled:opacity-30 disabled:cursor-not-allowed",
              input.trim() && !disabled && "shadow-glow"
            )}
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
