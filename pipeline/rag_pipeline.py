from retrieval.retriever import retrieve
from retrieval.reranker import rerank

def rag_answer(query):

    retrieved = retrieve(query)
    ranked = rerank(retrieved)

    context = "\n\n".join([c[0] for c in ranked])

    response = f"""
Question:
{query}

Answer (context aware):

{context}

Sources:
{[c[0][:40] + '...' for c in ranked]}
"""
    return response
