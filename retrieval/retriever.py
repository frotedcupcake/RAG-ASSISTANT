from embeddings.embedder import embed
from vectorstore.db import search

def retrieve(query, k=5):
    q_emb = embed([query])[0]
    results = search(q_emb, k=k)

    return list(zip(results["documents"][0], results["distances"][0]))
