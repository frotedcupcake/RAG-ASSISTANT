from ingest.pdf_loader import load_pdf
from preprocess.cleaner import clean_text
from chunking.chunker import chunk_text
from embeddings.embedder import embed
from vectorstore.db import add_chunks

def index_pdf(path):

    pages = load_pdf(path)

    chunks = []
    for p in pages:
        cleaned = clean_text(p["text"])
        page_chunks = chunk_text(cleaned)

        for ch in page_chunks:
            chunks.append(ch)

    embeddings = embed(chunks)
    from vectorstore.db import add_chunks
    add_chunks(chunks, embeddings)

    print(f"Indexed {len(chunks)} chunks from {path}")
