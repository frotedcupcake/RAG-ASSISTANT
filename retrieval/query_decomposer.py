import re


def normalize_query(query: str) -> str:
    """
    Clean and normalize query text.
    """
    query = query.strip()
    query = re.sub(r"\s+", " ", query)
    return query


def extract_key_phrases(query: str):
    """
    Extract candidate key phrases from the query.
    Very light NLP (no hardcoding to domain).
    """

    # remove punctuation
    cleaned = re.sub(r"[^\w\s]", "", query.lower())

    tokens = cleaned.split()

    # remove very short tokens
    tokens = [t for t in tokens if len(t) > 2]

    return tokens


def decompose_query(query: str):
    """
    Break a single user query into multiple focused sub-queries.

    Example:
    "what is convolution in signal processing"

    →
    [
      "convolution",
      "definition of convolution",
      "convolution in signal processing",
      "convolution intuition"
    ]
    """

    query = normalize_query(query)
    key_terms = extract_key_phrases(query)

    sub_queries = set()

    # original query always included
    sub_queries.add(query)

    # definition-focused queries
    for term in key_terms:
        sub_queries.add(f"definition of {term}")
        sub_queries.add(f"{term} explanation")
        sub_queries.add(f"{term} concept")

    # intuition-focused query
    sub_queries.add(f"{query} intuition")

    # limit size to avoid explosion
    return list(sub_queries)[:8]
