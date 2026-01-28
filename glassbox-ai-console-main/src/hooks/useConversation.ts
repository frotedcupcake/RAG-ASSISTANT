import { useState, useCallback } from "react";
import {
  ConversationState,
  ChatMessage,
  PipelineStep,
  DocumentChunk
} from "@/types/chat";

/* -----------------------------
   Pipeline Steps (Real)
----------------------------- */
const initialPipelineSteps: PipelineStep[] = [
  { id: "retrieval", name: "Hybrid Retrieval", status: "pending" },
  { id: "reranking", name: "Reranking", status: "pending" },
  { id: "generation", name: "Generation", status: "pending" }
];

/* -----------------------------
   API CONFIG
----------------------------- */
const API_URL = "http://localhost:8000/ask";

/* -----------------------------
   Hook
----------------------------- */
export function useConversation() {
  const [state, setState] = useState<ConversationState>({
    messages: [],
    currentQuery: "",
    isGenerating: false,
    pipelineSteps: initialPipelineSteps,
    retrievedChunks: [],
    highlightedChunkId: null,
    pinnedChunkIds: []
  });

  /* -----------------------------
     Send Message → FastAPI
  ----------------------------- */
  const sendMessage = useCallback(async (content: string) => {
    const userMessage: ChatMessage = {
      id: `msg-${Date.now()}`,
      role: "user",
      content,
      timestamp: new Date()
    };

    // Reset UI + show pending pipeline
    setState(prev => ({
      ...prev,
      messages: [...prev.messages, userMessage],
      isGenerating: true,
      pipelineSteps: initialPipelineSteps.map(s => ({ ...s, status: "pending" })),
      retrievedChunks: []
    }));

    try {
      // 🔥 CALL FASTAPI
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: content })
      });

      const data = await response.json();

      /* -----------------------------
         Map Retrieved Chunks
      ----------------------------- */
      const retrievedChunks: DocumentChunk[] = data.retrieved_chunks.map(
        (chunk: any, idx: number) => ({
          id: `chunk-${idx}`,
          content: chunk.text,
          section: chunk.heading,
          page: Number(chunk.page),
          similarityScore: chunk.score,
          usedInAnswer: data.reranked_chunks.some(
            (r: any) => r.text === chunk.text
          )
        })
      );

      /* -----------------------------
         Pipeline Steps (Real Latency)
      ----------------------------- */
      const steps: PipelineStep[] = [
        {
          id: "retrieval",
          name: "Hybrid Retrieval",
          status: "complete",
          latencyMs: data.latency.retrieval * 1000
        },
        {
          id: "reranking",
          name: "Reranking",
          status: "complete",
          latencyMs: data.latency.reranking * 1000
        },
        {
          id: "generation",
          name: "Generation",
          status: "complete",
          latencyMs: data.latency.generation * 1000
        }
      ];

      /* -----------------------------
         Assistant Message
      ----------------------------- */
      const assistantMessage: ChatMessage = {
        id: `msg-${Date.now() + 1}`,
        role: "assistant",
        content: data.answer,
        timestamp: new Date(),
        groundingStatus: data.grounded ? "grounded" : "refused"
      };

      setState(prev => ({
        ...prev,
        messages: [...prev.messages, assistantMessage],
        pipelineSteps: steps,
        retrievedChunks,
        isGenerating: false
      }));
    } catch (err) {
      console.error("API error:", err);

      const errorMessage: ChatMessage = {
        id: `msg-${Date.now() + 2}`,
        role: "assistant",
        content: "⚠️ Backend connection failed.",
        timestamp: new Date(),
        groundingStatus: "refused"
      };

      setState(prev => ({
        ...prev,
        messages: [...prev.messages, errorMessage],
        isGenerating: false
      }));
    }
  }, []);

  /* -----------------------------
     UI Helpers
  ----------------------------- */
  const setHighlightedChunk = useCallback((chunkId: string | null) => {
    setState(prev => ({ ...prev, highlightedChunkId: chunkId }));
  }, []);

  const togglePinnedChunk = useCallback((chunkId: string) => {
    setState(prev => ({
      ...prev,
      pinnedChunkIds: prev.pinnedChunkIds.includes(chunkId)
        ? prev.pinnedChunkIds.filter(id => id !== chunkId)
        : [...prev.pinnedChunkIds, chunkId]
    }));
  }, []);

  /* -----------------------------
     Derived Metrics
  ----------------------------- */
  const totalLatency = state.pipelineSteps
    .filter(s => s.status === "complete")
    .reduce((sum, s) => sum + (s.latencyMs || 0), 0);

  const usedChunks = state.retrievedChunks.filter(c => c.usedInAnswer).length;

  const currentGroundingStatus =
    state.messages.length > 0
      ? state.messages[state.messages.length - 1].groundingStatus || null
      : null;

  return {
    ...state,
    sendMessage,
    setHighlightedChunk,
    togglePinnedChunk,
    totalLatency,
    usedChunks,
    currentGroundingStatus
  };
}
