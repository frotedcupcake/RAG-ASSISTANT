from embeddings.embedder import embed
from vectorstore.db import search

def retrieve(query, k=10):

    q_emb = embed([query])[0]
    res = search(q_emb, k=k)

    docs = res["documents"][0]
    dists = res["distances"][0]
    metas = res["metadatas"][0]

    return list(zip(docs, dists, metas))
