import re
from retrieval.definition_detector import (
    looks_like_definition,
    looks_like_weak_intro
)


def split_sentences(text):
    return [s.strip() for s in re.split(r"[.?!]\s+", text) if s.strip()]


def extract_definition_sentences(text, max_sentences=3):

    sentences = split_sentences(text)
    scored = []

    for s in sentences:
        score = 0

        if looks_like_definition(s):
            score += 3

        if looks_like_weak_intro(s):
            score -= 2

        if len(re.findall(r"[∑∫=/+*-]", s)) > 4:
            score -= 2

        if 40 < len(s) < 220:
            score += 1

        scored.append((s, score))

    scored.sort(key=lambda x: -x[1])

    return [s for s, _ in scored[:max_sentences]]


def score_definition_quality(def_sentences):

    if not def_sentences:
        return 0

    score = 0

    for s in def_sentences:

        if looks_like_definition(s):
            score += 2

        if looks_like_weak_intro(s):
            score -= 1

        if 40 < len(s) < 220:
            score += 1

        if len(re.findall(r"[∑∫=/+*-]", s)) > 4:
            score -= 1

    return max(0.0, min(score / 6.0, 1.0))


# ---------------- helper to avoid backslash inside f-strings ----------------
def bullet_block(defs):
    return "\n".join(f"• {d}" for d in defs[:3])


# ---------------- main report generator ----------------
def build_comparison_report(primary, alternatives):

    primary_text, primary_meta, primary_defs, primary_score = primary

    primary_bullets = bullet_block(primary_defs)

    alt_blocks = []

    for text, meta, defs, score in alternatives:

        alt_bullets = bullet_block(defs)

        alt_blocks.append(
            f"""
Alternative Definition
— {meta.get('heading','Unknown Section')} (pg {meta.get('page','?')})
Confidence: {round(score,2)}

{alt_bullets}
"""
        )

    return f"""
Selected Definition
— {primary_meta.get('heading','Unknown Section')} (pg {primary_meta.get('page','?')})
Confidence: {round(primary_score,2)}

{primary_bullets}

──────────
Comparison Notes:

The system compared multiple candidate definitions and chose the most conceptually precise excerpt based on:

• definitional phrasing
• conceptual clarity
• minimal noise / worked examples
• low formula distraction

──────────
Other Relevant Sources:

{''.join(alt_blocks)}
"""
