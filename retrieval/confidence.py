import re


def looks_like_definition(sentence):
    """
    Language patterns commonly used in definitions.
    These are domain-neutral and do not inject meaning.
    """

    s = sentence.lower()

    return any([
        "is defined as" in s,
        "is the process of" in s,
        "refers to" in s,
        "can be described as" in s,
        "is characterized by" in s,
        "represents" in s,
        "denotes" in s,
        "is a form of" in s,
        "is a type of" in s,
    ])


def looks_like_weak_intro(sentence):

    s = sentence.lower()

    return any([
        "in this chapter" in s,
        "we will see" in s,
        "as discussed earlier" in s,
        "in the following section" in s,
        "we begin our discussion" in s
    ])


def is_formula_heavy(sentence):
    return len(re.findall(r"[∑∫=/*+\-\^]", sentence)) > 6


def is_extreme_length(sentence):
    return len(sentence) < 25 or len(sentence) > 300


# ------------------------------
# Confidence scoring model
# ------------------------------

def compute_confidence(sentences):
    """
    Computes confidence score ∈ [0,1]
    based on textual clarity & definition-likeness.

    This does NOT hallucinate or infer meaning.
    It only evaluates sentence quality.
    """

    if not sentences:
        return 0.0

    score = 0

    for s in sentences:

        # strong definition tone → reward
        if looks_like_definition(s):
            score += 2

        # weak narrative intro → penalize
        if looks_like_weak_intro(s):
            score -= 2

        # healthy sentence length → reward
        if 40 < len(s) < 220:
            score += 1

        # penalize formula-noise blocks
        if is_formula_heavy(s):
            score -= 1

        # penalize unclear fragments
        if is_extreme_length(s):
            score -= 1

    # normalize to range 0–1
    return max(0.0, min(score / 6.0, 1.0))
