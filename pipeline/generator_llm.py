from llama_cpp import Llama

llm = Llama(
    model_path="/Users/adityasachan/Documents/rag-assistant/models/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
    n_ctx=4096,
    n_threads=6
)

SYSTEM_PROMPT = """
You are an academic assistant. Use ONLY the provided context.
Do not hallucinate. If the answer is unclear, say so.

Explain the concept clearly:
• 1–2 line definition
• short intuition
• optional formal statement

Cite page numbers when present.
"""

def generate_answer(query, context):

    prompt = f"""
{SYSTEM_PROMPT}

Question:
{query}

Context:
{context}

Answer:
"""

    response = llm(
        prompt,
        max_tokens=400,
        temperature=0.2,
        top_p=0.95
    )

    return response["choices"][0]["text"].strip()
