import re
from config.settings import settings
from config.logging_config import log

# --------------------------------------------------
# Noise / Structure Detection Helpers
# --------------------------------------------------

def is_math_heavy(text):
    """
    Detect equation-heavy or symbol-heavy chunks.
    """

    math_patterns = [
        r"[∑∫±≈≠∞√λμσΩωτθπ]",
        r"[0-9]+\s*[-+*/=]\s*[0-9]+",
        r"\([a-z]\s*[-+*/]\s*[a-z]\)",
        r"[A-Za-z]\s*\([tnk]\)"
    ]

    return any(re.search(p, text) for p in math_patterns)


def looks_like_definition(text):
    """
    Detect generic definition-style phrasing.
    Domain neutral.
    """

    definition_patterns = [
        r"is defined as",
        r"can be defined as",
        r"refers to",
        r"can be described as",
        r"is characterized by",
        r"is the process of",
        r"represents",
        r"denotes",
        r"in other words"
    ]

    return any(re.search(p, text.lower()) for p in definition_patterns)


def looks_like_weak_intro(text):
    """
    Detect weak textbook narration / boilerplate.
    """

    weak_patterns = [
        r"in this chapter",
        r"we will see",
        r"as discussed earlier",
        r"in the following section",
        r"the goal of this section",
        r"we begin our discussion"
    ]

    return any(re.search(p, text.lower()) for p in weak_patterns)


def is_short_and_clean(text):
    """
    Reward concise readable explanatory chunks.
    """

    return (
        40 < len(text) < 400
        and "\n" not in text
    )


def looks_like_noise(text):
    """
    Detect OCR garbage / page artifacts.
    """

    text = text.strip()

    if len(text) < 25:
        return True

    alpha_ratio = (
        sum(c.isalpha() for c in text)
        / max(len(text), 1)
    )

    if alpha_ratio < 0.45:
        return True

    return False


# --------------------------------------------------
# Main Chunk Scoring Logic
# --------------------------------------------------

def score_chunk(text, meta, distance):

    heading = "Unknown Section"
    page = "Unknown"

    if meta is not None:
        heading = meta.get("heading", "Unknown Section")
        page = meta.get("page", "Unknown")

    text_low = text.lower()

    score = 1.0 / (1.0 + distance)

    if looks_like_definition(text_low):
        score += 0.30

    if looks_like_weak_intro(text_low):
        score -= 0.20

    if looks_like_noise(text_low):
        score -= 0.60

    if is_math_heavy(text_low):
        score -= 0.15

    if is_short_and_clean(text_low):
        score += 0.10

    return score, heading, page


# --------------------------------------------------
# Main Reranker
# --------------------------------------------------

def rerank(results, top_k=None):
    top_k = top_k or settings.reranker_top_k

    rescored = []

    for item in results:

        if item is None or len(item) < 3:
            continue

        text, dist, meta = item

        if not text or not text.strip():
            continue

        score, heading, page = score_chunk(
            text,
            meta,
            dist
        )

        rescored.append(
            (
                text,
                score,
                {
                    "heading": heading,
                    "page": page
                }
            )
        )

    rescored.sort(key=lambda x: -x[1])

    ranked = rescored[:top_k]
    log.info(f"rerank | input={len(results)} | output={len(ranked)}")
    return ranked