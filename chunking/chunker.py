import re

MIN_CHUNK = 350
MAX_CHUNK = 600
CHUNK_OVERLAP = 60


# ----------------------------------------------------
# Step 1 — Normalize & split into logical paragraphs
# ----------------------------------------------------
def split_into_paragraphs(text):
    """
    Convert raw OCR/scanned PDF text into clean paragraphs
    """

    # collapse repeated blank lines
    text = re.sub(r"\n\s*\n", "\n\n", text)

    paragraphs = [
        p.strip()
        for p in text.split("\n\n")
        if len(p.strip()) > 0
    ]

    return paragraphs


# ----------------------------------------------------
# Step 2 — Detect headings / section titles
# ----------------------------------------------------
def is_heading(line):
    """
    Identify headings like:
    - SECTION 2.1 DISCRETE SYSTEMS
    - 1.2 CONTINUOUS-TIME SIGNALS
    - CHAPTER 4 FOURIER SERIES
    """

    return (
        len(line) < 80
        and (
            line.isupper()
            or re.match(r"^\d+(\.\d+)*\s", line)
            or "CHAPTER" in line.upper()
        )
    )


def attach_headings(paragraphs):
    """
    Label each paragraph with the most recent heading
    """

    chunks = []
    current_heading = "Unknown Section"

    for p in paragraphs:

        if is_heading(p):
            current_heading = p
            continue

        chunks.append({
            "heading": current_heading,
            "text": p
        })

    return chunks


# ----------------------------------------------------
# Step 3 — Semantic grouping into meaning-units
# ----------------------------------------------------
def semantic_chunk(paragraphs):
    """
    Combine related paragraphs into chunks
    while avoiding oversize context blocks
    """

    chunks = []
    buffer = ""
    heading_meta = None

    for p in paragraphs:

            text = p["text"]

            candidate = (buffer + "\n" + text).strip()

            # if adding paragraph makes chunk too large → flush
            if len(candidate) > MAX_CHUNK:

                if len(buffer) > 0:
                    chunks.append({
                        "heading": heading_meta,
                        "chunk": buffer.strip()
                    })

                buffer = text
                heading_meta = p["heading"]

            else:
                buffer = candidate
                heading_meta = p["heading"]

    # flush remaining buffer
    if len(buffer) > 0:
        chunks.append({
            "heading": heading_meta,
            "chunk": buffer.strip()
        })

    return chunks


# ----------------------------------------------------
# Step 4 — Add small overlap for context continuity
# ----------------------------------------------------
def add_overlap(chunks):
    overlapped = []

    for i, ch in enumerate(chunks):

        if i == 0:
            overlapped.append(ch)
            continue

        prev = chunks[i - 1]["chunk"]

        tail = prev[-CHUNK_OVERLAP:]

        overlapped.append({
            "heading": ch["heading"],
            "chunk": (tail + " " + ch["chunk"]).strip()
        })

    return overlapped


# ----------------------------------------------------
# PUBLIC API
# ----------------------------------------------------
def build_chunks(raw_text):
    """
    Full semantic chunking pipeline:

    1) normalize & split text
    2) attach headings as metadata
    3) group into conceptual meaning-units
    4) add overlap for context smoothness
    """

    paragraphs = split_into_paragraphs(raw_text)

    paragraphs_headed = attach_headings(paragraphs)

    semantic_chunks = semantic_chunk(paragraphs_headed)

    final_chunks = add_overlap(semantic_chunks)

    return final_chunks
