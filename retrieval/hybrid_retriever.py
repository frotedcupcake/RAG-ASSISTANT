from retrieval.query_decomposer import decompose_query
from vectorstore.db import search
from embeddings.embedder import embed


def deduplicate_results(results):
    """
    Remove duplicate chunks based on text content.
    Keep the best (lowest distance) version.
    """

    seen = {}

    for text, distance, meta in results:
        key = text.strip()

        if key not in seen or distance < seen[key][1]:
            seen[key] = (text, distance, meta)

    return list(seen.values())


def vector_search(query, k=5):
    """
    Run a single vector search for one query.
    """

    query_embedding = embed([query])[0]

    raw = search(query_embedding, k=k)

    documents = raw.get("documents", [[]])[0]
    distances = raw.get("distances", [[]])[0]
    metadatas = raw.get("metadatas", [[]])[0]

    results = []

    for doc, dist, meta in zip(documents, distances, metadatas):
        results.append((doc, dist, meta or {}))

    return results


def hybrid_retrieve(query, max_per_query=5):
    """
    Perform multi-query retrieval using query decomposition.
    """

    sub_queries = decompose_query(query)

    all_results = []

    for q in sub_queries:
        results = vector_search(q, k=max_per_query)
        all_results.extend(results)

    # remove duplicates
    return deduplicate_results(all_results)
