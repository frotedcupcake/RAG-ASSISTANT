import os
import chromadb
from chromadb.config import Settings

# ----------------------------------------
# Resolve persistent DB path
# ----------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "db")

os.makedirs(DB_PATH, exist_ok=True)

# ----------------------------------------
# Use PersistentClient (supports persistence)
# ----------------------------------------
chroma = chromadb.PersistentClient(
    path=DB_PATH
)

# ----------------------------------------
# Load / create collection
# ----------------------------------------
collection = chroma.get_or_create_collection("campus_docs")


# ----------------------------------------
# Add chunks in batches + auto-persist
# ----------------------------------------
def add_chunks(docs, embeddings, batch_size=1000):
    ids = [str(i) for i in range(len(docs))]

    for i in range(0, len(docs), batch_size):

        batch_docs = docs[i:i + batch_size]
        batch_emb = embeddings[i:i + batch_size]
        batch_ids = ids[i:i + batch_size]

        collection.add(
            ids=batch_ids,
            documents=batch_docs,
            embeddings=batch_emb
        )

    # PersistentClient automatically saves to disk
    print(f"Indexed {len(docs)} chunks → stored in {DB_PATH}")


# ----------------------------------------
# Query / similarity search
# ----------------------------------------
def search(query_embedding, k=5):
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )


# ----------------------------------------
# Debug helper
# ----------------------------------------
def count_chunks():
    return collection.count()
