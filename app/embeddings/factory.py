from app.config import settings
from app.embeddings.local import LocalEmbeddingEncoder
from app.embeddings.bytez import BytezEmbeddingEncoder


def get_embedding_encoder(embedding_model: str | None = None):
    backend = settings.embedding_backend.lower()

    if backend == "local":
        return LocalEmbeddingEncoder()

    if backend == "bytez":
        return BytezEmbeddingEncoder(
            model_override=embedding_model
        )

    raise ValueError(f"Unknown embedding backend: {backend}")
