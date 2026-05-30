
from llama_cpp import Llama
from config.settings import settings
from config.logging_config import log

llm = Llama(model_path=settings.model_path, n_ctx=settings.llm_n_ctx, n_threads=settings.llm_n_threads)


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
    log.info(f"generate | tokens={response['usage']['total_tokens']} | query='{query[:50]}'")
    return response["choices"][0]["text"].strip()