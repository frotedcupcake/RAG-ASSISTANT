import json
import re
import statistics
from pathlib import Path

from pipeline.rag_pipeline import rag_answer


EVAL_DATASET = "eval/benchmark.json"


def load_benchmark():
    with open(EVAL_DATASET, "r") as f:
        return json.load(f)


def extract_answer_text(rag_output):
    """
    Pull only the main answer text from synthesized output.
    """
    match = re.search(r"Answer:\n(.+?)\n\nIntuition", rag_output, re.S)
    if match:
        return match.group(1).strip()

    # fallback: return whole text
    return rag_output


def score_answer(answer, expected_keywords):
    """
    Score 0–1 based on keyword coverage.
    Soft-matching to handle textbook wording differences.
    """

    answer_low = answer.lower()

    hits = 0
    for kw in expected_keywords:
        if kw.lower() in answer_low:
            hits += 1

    if len(expected_keywords) == 0:
            return 0

    return hits / len(expected_keywords)


def evaluate_query(entry):
    query = entry["query"]
    keywords = entry["expected_keywords"]

    print(f"\n🔎 Evaluating: {query}")

    rag_output = rag_answer(query)

    answer_text = extract_answer_text(rag_output)

    score = score_answer(answer_text, keywords)

    result = {
        "query": query,
        "score": round(score, 3),
        "status": (
            "GOOD" if score >= 0.7
            else "OK" if score >= 0.4
            else "WEAK"
        )
    }

    print(f"Score: {result['score']}  →  {result['status']}")

    return result


def run_evaluation():
    data = load_benchmark()

    results = []
    for entry in data:
        result = evaluate_query(entry)
        results.append(result)

    scores = [r["score"] for r in results]

    print("\n──────────── Evaluation Summary ────────────")

    print(f"Queries Evaluated: {len(results)}")
    print(f"Avg Score: {round(statistics.mean(scores), 3)}")
    print(f"Median Score: {round(statistics.median(scores), 3)}")
    print(f"High Quality (>0.7): {sum(s >= 0.7 for s in scores)}")
    print(f"Weak (<0.4): {sum(s < 0.4 for s in scores)}")

    print("\nDetailed Results:")
    for r in results:
        print(f" - {r['query']}: {r['score']} ({r['status']})")


if __name__ == "__main__":
    run_evaluation()
