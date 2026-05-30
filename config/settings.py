from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    # Paths
    model_path: str = str(BASE_DIR / "models" / "mistral-7b-instruct-v0.2.Q4_K_M.gguf")
    db_path: str = str(BASE_DIR / "db")
    docs_dir: str = str(BASE_DIR / "docs")

    # LLM
    llm_n_ctx: int = 2048
    llm_n_threads: int = 6
    llm_max_tokens: int = 256
    llm_temperature: float = 0.2

    # Retrieval
    retrieval_top_k: int = 5
    reranker_top_k: int = 5
    context_max_chunks: int = 3
    context_min_chars: int = 300

    # Chunking
    chunk_min: int = 350
    chunk_max: int = 600
    chunk_overlap: int = 60

    # Grounding
    grounding_min_chars: int = 400
    grounding_min_score: float = 0.15
    grounding_min_overlap: float = 0.15

    # Embedding
    embedding_model: str = "all-MiniLM-L6-v2"

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    frontend_origins: list = ["http://localhost:8080", "http://localhost:5173"]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()