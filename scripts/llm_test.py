from config.settings import settings
from llama_cpp import Llama

llm = Llama(
    model_path=settings.model_path,
    n_ctx=settings.llm_n_ctx,
    n_threads=settings.llm_n_threads,
)

response = llm(
    "Explain discrete signals in one sentence.",
    max_tokens=150,
    temperature=0.3,
)

print(response["choices"][0]["text"])