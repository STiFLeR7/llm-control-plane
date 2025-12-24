from app.config import settings
from app.embeddings.encoder import EmbeddingEncoder
from app.embeddings.local import LocalEmbeddingEncoder
from app.embeddings.api import ApiEmbeddingEncoder


def get_embedding_encoder() -> EmbeddingEncoder:
    if settings.embedding_backend == "local":
        return LocalEmbeddingEncoder()

    if settings.embedding_backend == "api":
        return ApiEmbeddingEncoder()

    raise ValueError(f"Unknown embedding backend: {settings.embedding_backend}")
