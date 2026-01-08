from llama_cpp import Llama

llm = Llama(
    model_path="/Users/adityasachan/Documents/rag-assistant/models/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
    n_ctx=4096,
    n_threads=6
)

response = llm(
    "Explain discete signals in one sentence.",
    max_tokens=150,
    temperature=0.3
)

print(response["choices"][0]["text"])
