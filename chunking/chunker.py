import re

# ----------------------------------------------------
# Step 1 — Split into cleaned paragraphs
# ----------------------------------------------------
def split_into_paragraphs(text):
    # normalize line spacing
    text = re.sub(r'\n+', '\n', text)

    paragraphs = [
        p.strip() for p in text.split("\n")
        if p.strip()
    ]

    return paragraphs


# ----------------------------------------------------
# Step 2 — Detect section / heading labels
# ----------------------------------------------------
def detect_headings(paragraphs):
    chunks = []
    current_heading = "Unknown Section"

    for p in paragraphs:

        # heading heuristics
        is_heading = (
            len(p) < 80 and p.isupper()
        ) or (
            re.match(r"^[0-9]+\.", p)
        )

        if is_heading:
            current_heading = p
            continue

        chunks.append({
            "heading": current_heading,
            "text": p
        })

    return chunks


# ----------------------------------------------------
# Step 3 — Group related paragraphs into semantic chunks
# ----------------------------------------------------
def semantic_chunk(paragraphs, max_chars=1200):

    chunks = []
    buffer = ""
    heading_meta = None

    for p in paragraphs:

        text = p["text"]

        # keep paragraphs grouped without cutting mid-sentence
        if len(buffer) + len(text) < max_chars:
            buffer += "\n" + text
            heading_meta = p["heading"]
        else:
            chunks.append({
                "heading": heading_meta,
                "chunk": buffer.strip()
            })
            buffer = text
            heading_meta = p["heading"]

    if buffer:
        chunks.append({
            "heading": heading_meta,
            "chunk": buffer.strip()
        })

    return chunks


# ----------------------------------------------------
# Public API
# ----------------------------------------------------
def build_chunks(raw_text):
    """
    Full semantic chunking pipeline
    """

    paragraphs = split_into_paragraphs(raw_text)
    para_with_headings = detect_headings(paragraphs)
    chunks = semantic_chunk(para_with_headings)

    return chunks
