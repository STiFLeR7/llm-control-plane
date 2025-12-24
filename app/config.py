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
    embedding_backend: str = "local"  # "local" | "api"
    embedding_dim: int = 384

    # api embeddings (optional)
    embedding_api_provider: Optional[str] = None
    embedding_api_key: Optional[str] = None


settings = Settings()
