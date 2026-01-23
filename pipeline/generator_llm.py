from llama_cpp import Llama

llm = Llama(
    model_path="/Users/adityasachan/Documents/rag-assistant/models/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
    n_ctx=4096,
    n_threads=6
)

def generate_answer(query, context):
    """
    Strict RAG answer generation.
    The model is forbidden from using prior knowledge.
    """

    prompt = f"""
You are a retrieval-augmented assistant.

STRICT RULES:
- You MUST answer ONLY using the information in CONTEXT.
- You MUST NOT use prior knowledge.
- You MUST NOT guess or infer beyond the text.
- If the CONTEXT does not clearly contain the answer,
  respond EXACTLY with:

"The provided documents do not contain this information."

CONTEXT:
{context}

QUESTION:
{query}

ANSWER:
"""

    response = llm(
        prompt,
        max_tokens=256,
        temperature=0.2,
        stop=["</s>"]
    )

    return response["choices"][0]["text"].strip()
