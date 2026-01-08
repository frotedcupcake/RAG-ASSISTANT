import re

DEFINITION_PATTERNS = [
    r"\bis defined as\b",
    r"\bcan be defined as\b",
    r"\bis described as\b",
    r"\brefers to\b",
    r"\bis the process of\b",
    r"\bis the operation of\b",
    r"\bis a type of\b",
    r"\bis a form of\b",
    r"\bis a signal that\b",
    r"\bin which\b"
]

WEAK_CONTEXT_PATTERNS = [
    "in this chapter",
    "we will see",
    "as discussed earlier",
    "in the previous section",
    "figure",
    "illustrated in",
    "example",
    "case of",
    "context of"
]


def looks_like_definition(text: str) -> bool:
    t = text.lower()

    # strong definition markers
    for p in DEFINITION_PATTERNS:
        if re.search(p, t):
            return True

    return False


def looks_like_weak_intro(text: str) -> bool:
    t = text.lower()

    for p in WEAK_CONTEXT_PATTERNS:
        if p in t:
            return True

    return False
