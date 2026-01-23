# pipeline/grounding.py

import re
from statistics import mean


def normalize_text(text: str) -> set:
    """
    Lowercase, remove punctuation, split into unique words
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    return set(text.split())


def is_grounded(query, ranked_chunks, top_k=3):
    """
    Decide whether the answer should be grounded in retrieved documents.

    Returns:
        grounded (bool)
        diagnostics (dict)
    """

    if not ranked_chunks:
        return False, {"reason": "no_chunks"}

    top_chunks = ranked_chunks[:top_k]

    # -----------------------------
    # Heuristic 1: Context length
    # -----------------------------
    total_chars = sum(len(text) for text, _, _ in top_chunks)

    # -----------------------------
    # Heuristic 2: Similarity score
    # (higher = better in your setup)
    # -----------------------------
    scores = [score for _, score, _ in top_chunks]
    avg_score = mean(scores) if scores else 0.0

    # -----------------------------
    # Heuristic 3: Lexical overlap
    # -----------------------------
    query_words = normalize_text(query)
    context_words = set()

    for text, _, _ in top_chunks:
        context_words |= normalize_text(text)

    overlap_ratio = (
        len(query_words & context_words) / max(len(query_words), 1)
    )

    # -----------------------------
    # Thresholds (tunable)
    # -----------------------------
    MIN_CHARS = 400
    MIN_SCORE = 0.15
    MIN_OVERLAP = 0.15

    passes = [
        total_chars >= MIN_CHARS,
        avg_score >= MIN_SCORE,
        overlap_ratio >= MIN_OVERLAP,
    ]

    grounded = passes.count(True) >= 2

    diagnostics = {
        "total_chars": total_chars,
        "avg_score": round(avg_score, 3),
        "overlap_ratio": round(overlap_ratio, 3),
        "passes": passes,
    }

    return grounded, diagnostics
