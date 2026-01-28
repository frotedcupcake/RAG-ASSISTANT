import { useState } from "react";
import { cn } from "@/lib/utils";
import { GlassPanel } from "@/components/console/GlassPanel";
import { ConsoleHeader } from "@/components/console/ConsoleHeader";
import { PipelineInspector } from "@/components/console/PipelineInspector";
import { DocumentChunks } from "@/components/console/DocumentChunks";
import { ChatMessageComponent } from "@/components/console/ChatMessage";
import { StreamingPlaceholder } from "@/components/console/StreamingPlaceholder";
import { ChatInput } from "@/components/console/ChatInput";
import { StatusBar } from "@/components/console/StatusBar";
import { useConversation } from "@/hooks/useConversation";
import { ScrollArea } from "@/components/ui/scroll-area";

export default function Index() {
  const [leftPanelOpen, setLeftPanelOpen] = useState(false);
  
  const {
    messages,
    isGenerating,
    pipelineSteps,
    retrievedChunks,
    highlightedChunkId,
    pinnedChunkIds,
    sendMessage,
    setHighlightedChunk,
    togglePinnedChunk,
    totalLatency,
    usedChunks,
    currentGroundingStatus
  } = useConversation();

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <ConsoleHeader
        leftPanelOpen={leftPanelOpen}
        onToggleLeftPanel={() => setLeftPanelOpen(!leftPanelOpen)}
        className="border-b border-border/50"
      />
      
      {/* Main content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left panel - Document chunks */}
        <aside
          className={cn(
            "w-80 border-r border-border/50 flex flex-col transition-all duration-300 ease-out",
            leftPanelOpen ? "translate-x-0" : "-translate-x-full absolute left-0 top-[57px] bottom-[41px] z-10 bg-background"
          )}
          style={{ display: leftPanelOpen ? 'flex' : 'none' }}
        >
          <ScrollArea className="flex-1 p-4">
            {retrievedChunks.length > 0 ? (
              <DocumentChunks
                chunks={retrievedChunks}
                highlightedChunkId={highlightedChunkId}
                pinnedChunkIds={pinnedChunkIds}
                onChunkHover={setHighlightedChunk}
                onChunkClick={togglePinnedChunk}
              />
            ) : (
              <div className="h-full flex items-center justify-center">
                <p className="text-xs font-mono text-muted-foreground/50 text-center">
                  No retrieved chunks yet.<br />
                  Submit a query to begin.
                </p>
              </div>
            )}
          </ScrollArea>
        </aside>
        
        {/* Center - Chat canvas */}
        <main className="flex-1 flex flex-col min-w-0">
          <ScrollArea className="flex-1 p-6">
            <div className="max-w-3xl mx-auto space-y-6">
              {messages.length === 0 && !isGenerating && (
                <div className="h-[50vh] flex flex-col items-center justify-center text-center space-y-4">
                  <div className="w-16 h-16 rounded-2xl bg-secondary/30 border border-border/50 flex items-center justify-center">
                    <div className="w-6 h-6 rounded-full bg-primary/20 animate-pulse-glow" />
                  </div>
                  <div className="space-y-2">
                    <h2 className="text-lg font-medium text-foreground">
                      Intelligence Console Ready
                    </h2>
                    <p className="text-sm text-muted-foreground max-w-md">
                      Enter a query to retrieve relevant context and generate an auditable, evidence-backed response.
                    </p>
                  </div>
                  <div className="flex items-center gap-4 mt-4">
                    <div className="flex items-center gap-2 text-xs font-mono text-muted-foreground/60">
                      <div className="w-1.5 h-1.5 rounded-full bg-success" />
                      <span>Vector DB Connected</span>
                    </div>
                    <div className="flex items-center gap-2 text-xs font-mono text-muted-foreground/60">
                      <div className="w-1.5 h-1.5 rounded-full bg-success" />
                      <span>LLM Online</span>
                    </div>
                  </div>
                </div>
              )}
              
              {messages.map((message) => (
                <ChatMessageComponent
                  key={message.id}
                  message={message}
                  highlightedChunkId={highlightedChunkId}
                  onSentenceHover={setHighlightedChunk}
                  onSentenceClick={togglePinnedChunk}
                />
              ))}
              
              {isGenerating && <StreamingPlaceholder />}
            </div>
          </ScrollArea>
          
          {/* Chat input */}
          <div className="p-4 border-t border-border/50">
            <div className="max-w-3xl mx-auto">
              <ChatInput
                onSend={sendMessage}
                disabled={isGenerating}
              />
            </div>
          </div>
        </main>
        
        {/* Right panel - Pipeline inspector */}
        <aside className="w-64 border-l border-border/50 p-4 flex flex-col">
          <GlassPanel className="flex-1 p-4 relative">
            <PipelineInspector steps={pipelineSteps} />
          </GlassPanel>
        </aside>
      </div>
      
      {/* Status bar */}
      <StatusBar
        groundingStatus={currentGroundingStatus}
        totalChunks={retrievedChunks.length}
        usedChunks={usedChunks}
        totalLatencyMs={totalLatency}
        className="border-t border-border/50"
      />
    </div>
  );
}
