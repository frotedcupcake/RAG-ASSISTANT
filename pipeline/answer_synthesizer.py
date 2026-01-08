import re


def normalize(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_key_phrases(sentence):
    """
    Extract the conceptual subject by finding:
    - leading noun phrases
    - X is Y patterns
    - term → attribute relations
    """

    # Extract before "is / refers to / represents"
    m = re.search(r"^(.*?)( is| refers to| represents| denotes)", sentence, re.I)
    if m:
        return normalize(m.group(1))

    # Remove examples / cases
    sentence = re.sub(r"(for example|for instance|consider|suppose).*", "", sentence, flags=re.I)

    # Trim trailing descriptive tails
    sentence = re.sub(r"(which .*|that .*|where .*|when .*|as .*|because .*|therefore .*|hence .*|thus.*)$", "", sentence, flags=re.I)

    return normalize(sentence)


def compress_explanation(sentence):
    """
    Reduce sentence complexity by:
    - removing nested clauses
    - collapsing qualifiers
    - stripping citations & brackets
    """

    sentence = re.sub(r"\([^)]*\)", "", sentence)      # remove parentheses
    sentence = re.sub(r"\[[^\]]*\]", "", sentence)     # remove citations

    # remove filler phrases
    sentence = re.sub(r"\b(in essence|in particular|in general|in practice|in many cases)\b", "", sentence, flags=re.I)

    # collapse multi-clause chains
    sentence = re.sub(r"(,?\s*(which|that|where|when).*)$", "", sentence, flags=re.I)

    return normalize(sentence)


def abstract_relationship(sentence):
    """
    Identify conceptual relationships WITHOUT adding wording:

    Example transformations:

    x is defined as interaction between a and b
      → interaction between a and b

    y describes mapping from p to q
      → mapping from p to q
    """

    sentence = sentence.lower()

    patterns = [
        r"is defined as (.*)",
        r"is a measure of (.*)",
        r"is obtained by (.*)",
        r"can be viewed as (.*)",
        r"describes (.*)",
        r"represents (.*)",
        r"corresponds to (.*)",
        r"relates (.*)",
        r"involves (.*)",
    ]

    for p in patterns:
        m = re.search(p, sentence)
        if m:
            return normalize(m.group(1))

    return None


def build_intuition(sentences):
    """
    Generate intuition by:

    1) picking the most conceptual sentence
    2) extracting subject phrase
    3) compressing definition
    4) abstracting relationship meaning

    No templates. No canned text.
    """

    if not sentences:
        return None

    s = sentences[0]

    s = normalize(s)
    core = extract_key_phrases(s)
    compressed = compress_explanation(s)

    relational = abstract_relationship(s)

    # Priority: relationship meaning > compressed form > core noun phrase
    if relational:
        return relational

    if compressed:
        return compressed

    return core
