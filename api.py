import time
from typing import List, Dict, Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from retrieval.hybrid_retriever import hybrid_retrieve
from retrieval.reranker import rerank
from pipeline.generator_llm import generate_answer
from typing import Optional


# -----------------------------------
# FastAPI App
# -----------------------------------

app = FastAPI(
    title="Glass-Box RAG API",
    description="Transparent, grounded Retrieval-Augmented Generation API",
    version="1.0.0"
)

# -----------------------------------
# CORS (REQUIRED for frontend)
# -----------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",   # Next.js / Lovable
        "http://localhost:5173",   # Vite (optional)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------
# Request / Response Models
# -----------------------------------

class QueryRequest(BaseModel):
    question: str


class ChunkDebug(BaseModel):
    text: str
    score: float
    heading: str
    page: Any


class AskResponse(BaseModel):
    answer: str
    grounded: bool
    refusal_reason: Optional[str]

    latency: Dict[str, float]
    retrieved_chunks: List[ChunkDebug]
    reranked_chunks: List[ChunkDebug]


# -----------------------------------
# Helpers
# -----------------------------------

def build_context(ranked_chunks, max_chunks: int = 3) -> str:
    """
    Merge top-k reranked chunks into a single context block
    """
    return "\n\n".join(text for text, _, _ in ranked_chunks[:max_chunks])


def context_is_strong(ranked_chunks, context_text: str) -> bool:
    """
    Conservative grounding check
    """
    if not ranked_chunks:
        return False

    if len(context_text.strip()) < 300:
        return False

    return True


# -----------------------------------
# Main API Endpoint
# -----------------------------------

@app.post("/ask", response_model=AskResponse)
def ask(req: QueryRequest):

    timings: Dict[str, float] = {}

    # 1️⃣ Retrieval
    t0 = time.time()
    retrieved = hybrid_retrieve(req.question)
    timings["retrieval"] = round(time.time() - t0, 3)

    if not retrieved:
        return AskResponse(
            answer="No relevant content found in the knowledge base.",
            grounded=False,
            refusal_reason="No documents retrieved",
            latency=timings,
            retrieved_chunks=[],
            reranked_chunks=[]
        )

    retrieved_debug = [
        ChunkDebug(
            text=text[:500],
            score=score,
            heading=meta.get("heading", "Unknown"),
            page=meta.get("page", "?")
        )
        for text, score, meta in retrieved[:5]
    ]

    # 2️⃣ Reranking
    t1 = time.time()
    ranked = rerank(retrieved)
    timings["reranking"] = round(time.time() - t1, 3)

    if not ranked:
        return AskResponse(
            answer="No relevant content found in the knowledge base.",
            grounded=False,
            refusal_reason="Reranker filtered all candidates",
            latency=timings,
            retrieved_chunks=retrieved_debug,
            reranked_chunks=[]
        )

    reranked_debug = [
        ChunkDebug(
            text=text[:500],
            score=score,
            heading=meta.get("heading", "Unknown"),
            page=meta.get("page", "?")
        )
        for text, score, meta in ranked[:3]
    ]

    # 3️⃣ Context Build
    context = build_context(ranked)

    if not context_is_strong(ranked, context):
        return AskResponse(
            answer="No relevant content found in the knowledge base.",
            grounded=False,
            refusal_reason="Context too weak for grounded answer",
            latency=timings,
            retrieved_chunks=retrieved_debug,
            reranked_chunks=reranked_debug
        )

    # 4️⃣ Generation (STRICTLY grounded)
    t2 = time.time()
    answer = generate_answer(req.question, context)
    timings["generation"] = round(time.time() - t2, 3)

    return AskResponse(
        answer=answer,
        grounded=True,
        refusal_reason=None,
        latency=timings,
        retrieved_chunks=retrieved_debug,
        reranked_chunks=reranked_debug
    )
