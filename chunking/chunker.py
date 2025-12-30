def chunk_text(text, chunk_size=400, overlap=100):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        chunks.append(chunk.strip())
        start = end - overlap

    return chunks
