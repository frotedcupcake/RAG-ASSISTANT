export interface DocumentChunk {
  id: string;
  content: string;
  section: string;
  page: number;
  similarityScore: number;
  usedInAnswer: boolean;
}

export interface PipelineStep {
  id: string;
  name: string;
  status: 'pending' | 'active' | 'complete';
  latencyMs?: number;
  details?: string;
}

export interface EvidenceSentence {
  id: string;
  text: string;
  confidence: 'high' | 'low';
  sourceChunkId?: string;
  isPinned: boolean;
}

export interface ResponseBlock {
  type: 'summary' | 'explanation' | 'evidence';
  sentences: EvidenceSentence[];
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  responseBlocks?: ResponseBlock[];
  groundingStatus?: 'grounded' | 'partial' | 'refused';
}

export interface ConversationState {
  messages: ChatMessage[];
  currentQuery: string;
  isGenerating: boolean;
  pipelineSteps: PipelineStep[];
  retrievedChunks: DocumentChunk[];
  highlightedChunkId: string | null;
  pinnedChunkIds: string[];
}
