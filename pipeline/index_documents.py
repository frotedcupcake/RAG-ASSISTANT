from ingest.pdf_loader import load_pdf
from preprocess.cleaner import clean_text
from chunking.chunker import build_chunks
from embeddings.embedder import embed
from vectorstore.db import add_chunks


def index_pdf(path):

    print(f"\n📄 Indexing document: {path}")

    pages = load_pdf(path)

    docs = []

    for p in pages:

        
        cleaned = clean_text(p["text"])
        semantic_chunks = build_chunks(cleaned)

        for ch in semantic_chunks:
            docs.append({
                "text": ch["chunk"],
                "heading": ch["heading"],
                "page": p["page"]
            })

    if not docs:
        print("⚠️ No chunks generated — check PDF parsing")
        return

    
    texts = [d["text"] for d in docs]
    embeddings = embed(texts)

    
    add_chunks(docs, embeddings)

    print(f"✅ Indexed {len(docs)} semantic chunks from {path}")
