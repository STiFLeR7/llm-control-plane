from typing import List

from app.embeddings.encoder import EmbeddingEncoder
from app.config import settings


class ApiEmbeddingEncoder(EmbeddingEncoder):
    """
    API-based embedding encoder.
    Used only when explicitly configured.
    """

    def __init__(self):
        if not settings.embedding_api_key:
            raise RuntimeError("Embedding API key not configured")

        self.provider = settings.embedding_api_provider
        self.api_key = settings.embedding_api_key

    def encode(self, texts: List[str]) -> List[List[float]]:
        # Placeholder: implementation depends on provider
        # Gemini / OpenAI / others can be plugged here
        raise NotImplementedError("API embedding backend not wired yet")
