import math
import re
KEYWORD_BONUS = [
    "definition",
    "is defined as",
    "we define",
    "can be described as",
    "signal is",
    "system is"
]
import math


def score_chunk(text, meta, distance):

    heading = "Unknown Section"
    page = "Unknown"

    if meta is not None:
        heading = meta.get("heading", "Unknown Section")
        page = meta.get("page", "Unknown")

    text_low = text.lower()
    heading_low = heading.lower()

    # base score from vector similarity
    score = -distance

    # prefer conceptual sections
    if any(w in heading_low for w in ["introduction", "overview", "signal", "system", "convolution"]):
        score += 1.2

    # definition-style phrasing bonus
    DEFINITION_PATTERNS = [
        "is defined as",
        "we define",
        "refers to",
        "can be described as",
        "in other words",
        "a signal is",
        "a system is"
    ]

    for phrase in DEFINITION_PATTERNS:
        if phrase in text_low:
            score += 1.5

    # penalize overly long chunks (less precise)
    score -= math.log(len(text_low) + 1)

    return score, heading, page


def rerank(results):
    """
    Expected input format:
        [
          (text, distance, metadata),
          ...
        ]
    """

    rescored = []

    for item in results:

        # handle any bad tuples gracefully
        if item is None or len(item) < 3:
            continue

        text, dist, meta = item

        score, heading, page = score_chunk(text, meta, dist)

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

    # sort by best score
    rescored.sort(key=lambda x: -x[1])

    # return top 3
    return rescored[:3]

def is_math_heavy(text):
    """Detects equations / symbols / formula regions."""
    math_patterns = [
        r"[∑∫±≈≠∞√λμσΩωτθπ]",
        r"[0-9]+\s*[-+*/=]\s*[0-9]+",
        r"\([a-z]\s*[-+*/]\s*[a-z]\)",
        r"[A-Za-z]\s*\([tnk]\)"
    ]
    return any(re.search(p, text) for p in math_patterns)


def looks_like_example(text):
    """Detect example, case study, worked problem text."""
    return bool(re.search(
        r"(example|case|consider|suppose|let us|illustration|figure)",
        text.lower()
    ))


def looks_like_definition(text):
    """Detect definition-style language."""
    return bool(re.search(
        r"(is defined as|can be defined as|refers to|is the process of|"
        r"is called|we define|in other words|is the operation that)",
        text.lower()
    ))


def looks_like_intro(text):
    """Detect conceptual explanation / section intro tone."""
    return bool(re.search(
        r"(in this section|in this chapter|we will see that|"
        r"the goal of this section|we introduce|we discuss)",
        text.lower()
    ))


def is_short_and_clean(text):
    """Boost short crisp definition-like statements."""
    return 40 < len(text) < 400 and "\n" not in text
    
