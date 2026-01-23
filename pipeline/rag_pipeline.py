from retrieval.hybrid_retriever import hybrid_retrieve
from retrieval.reranker import rerank
from pipeline.generator_llm import generate_answer


# -------------------------------
# Context Builder
# -------------------------------

def build_context(ranked_chunks, max_chunks=3):
    merged_context = []

    for text, score, meta in ranked_chunks[:max_chunks]:
        merged_context.append(text)

    return "\n\n".join(merged_context)


# -------------------------------
# Context Strength Check
# -------------------------------

def context_is_strong(ranked_chunks, context_text):
    """
    Practical RAG grounding check:
    - Enough retrieved chunks
    - Enough textual evidence
    """

    if not ranked_chunks:
        return False

    # at least 1 solid chunk
    if len(ranked_chunks) < 1:
        return False

    # enough text to ground an answer
    if len(context_text.strip()) < 300:
        return False

    return True


# -------------------------------
# Main RAG Pipeline
# -------------------------------

def rag_answer(query):

    # 1️⃣ Retrieve
    retrieved = hybrid_retrieve(query)

    if not retrieved:
        return f"""
Question:
{query}

❌ No relevant content found in the knowledge base.
"""

    # 2️⃣ Rerank
    ranked = rerank(retrieved)

    if not ranked:
        return f"""
Question:
{query}

❌ No relevant content found in the knowledge base.
"""

    # 3️⃣ Build context first
    context = build_context(ranked)

    # 4️⃣ Validate context strength
    if not context_is_strong(ranked, context):
        return f"""
Question:
{query}

❌ No relevant content found in the knowledge base.
"""

    # 5️⃣ Generate grounded answer ONLY now
    llm_answer = generate_answer(query, context)

    return f"""
Question:
{query}

{llm_answer}
"""
