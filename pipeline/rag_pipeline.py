from retrieval.retriever import retrieve
from retrieval.reranker import rerank

def format_answer(query, ranked):

    sections = []

    for txt, score, meta in ranked:

        section = f"""
📌 **Section:** {meta['heading']}
📄 **Page:** {meta['page']}

{txt}
"""
        sections.append(section)

    return f"""
Question:
{query}

Answer (based on retrieved context):

{sections[0]}

──────────
Other relevant references:

{''.join(sections[1:])}
"""
    

def rag_answer(query):

    retrieved = retrieve(query)
    ranked = rerank(retrieved)

    return format_answer(query, ranked)
