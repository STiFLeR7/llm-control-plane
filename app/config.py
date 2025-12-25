import os
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Settings:
    # application
    app_name: str = "llm-control-plane"
    environment: str = "local"

    # logging
    log_dir: str = "logs"

    # embeddings
    embedding_backend: str = os.getenv("EMBEDDING_BACKEND", "local")
    embedding_dim: int = 384

    # bytez api
    bytez_api_key: Optional[str] = os.getenv("BYTEZ_API_KEY")
    bytez_embedding_model: str = os.getenv(
        "BYTEZ_EMBEDDING_MODEL",
        "sentence-transformers/all-MiniLM-L6-v2",
    )


settings = Settings()
