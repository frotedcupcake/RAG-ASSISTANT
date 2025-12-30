import math

KEYWORD_BONUS = [
    "definition",
    "is defined as",
    "we define",
    "can be described as",
    "signal is",
    "system is"
]

def score_chunk(text, meta, distance):

    # fallback defaults if metadata missing
    if meta is None:
        heading = "Unknown Section"
    else:
        heading = meta.get("heading", "Unknown Section")

    text_low = text.lower()
    heading_low = heading.lower()

    score = -distance  # base vector similarity

    # prefer heading-matching terms
    if any(w in heading_low for w in ["signal", "system", "convolution"]):
        score += 1.2

    # definitional phrasing bonus
    KEYWORD_BONUS = [
        "is defined as",
        "we define",
        "can be described as",
        "refers to",
        "a signal is",
        "a system is"
    ]

    for k in KEYWORD_BONUS:
        if k in text_low:
            score += 1.5

    # prefer tighter chunks
    score -= math.log(len(text_low) + 1)

    return score



def rerank(results):

    rescored = []

    for txt, dist, meta in results:

        rescored.append(
            (
                txt,
                score_chunk(txt, meta, dist),
                meta or {"heading": "Unknown Section", "page": 0}
            )
        )

    rescored.sort(key=lambda x: -x[1])

    return rescored[:3]
