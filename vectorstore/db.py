import os
import chromadb
from chromadb.config import Settings
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "db")

os.makedirs(DB_PATH, exist_ok=True)

chroma = chromadb.PersistentClient(
    path=DB_PATH
)

collection = chroma.get_or_create_collection("campus_docs")


def sanitize_metadata(md):
    """
    Ensure metadata values are Chroma-safe.
    Only allow primitive types and no None values.
    """

    heading = md.get("heading") or "Unknown Section"
    page = md.get("page")

    try:
        page = int(page)
    except:
        page = 0

    return {
        "heading": str(heading),
        "page": page
    }


def add_chunks(docs, embeddings, batch_size=800):

    ids = [str(i) for i in range(len(docs))]

    for i in range(0, len(docs), batch_size):

        batch = docs[i:i+batch_size]

        batch_ids = ids[i:i+batch_size]
        batch_docs = [d["text"] for d in batch]
        batch_emb = embeddings[i:i+batch_size]

        # sanitize metadata safely
        batch_meta = [sanitize_metadata(d) for d in batch]

        collection.add(
            ids=batch_ids,
            documents=batch_docs,
            embeddings=batch_emb,
            metadatas=batch_meta
        )

    print(f"Indexed {len(docs)} chunks → stored safely with metadata")

def search(query_embedding, k=5):
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )


def count_chunks():
    return collection.count()
def split_into_paragraphs(text):
    
    text = re.sub(r'\n+', '\n', text)
    parts = [p.strip() for p in text.split("\n") if p.strip()]
    return parts


def detect_headings(paragraphs):
    chunks = []
    current_heading = "Unknown Section"

    for p in paragraphs:

        
        if len(p) < 80 and p.isupper():
            current_heading = p
            continue

        chunks.append({
            "heading": current_heading,
            "text": p
        })

    return chunks


def semantic_chunk(paragraphs, max_tokens=800):
    """
    Combine paragraphs into semantically meaningful chunks
    without cutting sentences mid-way
    """

    chunks = []
    buffer = ""
    meta_heading = None

    for p in paragraphs:

        text = p["text"]

        if len(buffer) + len(text) < max_tokens:
            buffer += "\n" + text
            meta_heading = p["heading"]
        else:
            chunks.append({
                "heading": meta_heading,
                "chunk": buffer.strip()
            })
            buffer = text
            meta_heading = p["heading"]

    if buffer:
        chunks.append({
            "heading": meta_heading,
            "chunk": buffer.strip()
        })

    return chunks


def build_chunks(raw_text):
    paragraphs = split_into_paragraphs(raw_text)
    para_with_headings = detect_headings(paragraphs)
    chunks = semantic_chunk(para_with_headings)

    return chunks