import re

from retrieval.retriever import retrieve
from retrieval.reranker import rerank

from pipeline.generator_llm import generate_answer



def build_context(ranked_chunks, max_chunks=3):
    """
    ranked_chunks format:
       [(text, score, metadata), ...]
    """

    merged_context = []
    sources = []    

    for text, score, meta in ranked_chunks[:max_chunks]:

        heading = meta.get("heading", "Unknown Section")
        page = meta.get("page", "?")

        merged_context.append(text)

        sources.append(f"{heading} — Page {page}")

    return "\n\n".join(merged_context), sources



def rag_answer(query):

    
    retrieved = retrieve(query)

    if not retrieved:
        return f"""
Question:
{query}

No relevant content found in knowledge base.
"""

    
    ranked = rerank(retrieved)

    if not ranked:
        return f"""
Question:
{query}

Content retrieved, but no meaningful passages found.
"""

    
    context, sources = build_context(ranked)

    
    llm_answer = generate_answer(query, context)

    
    return f"""
Question:
{query}

{llm_answer}

──────────
Sources used:
{chr(10).join('• ' + s for s in sources)}
"""
