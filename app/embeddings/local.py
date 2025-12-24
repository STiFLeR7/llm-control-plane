from typing import List
from sentence_transformers import SentenceTransformer

from app.embeddings.encoder import EmbeddingEncoder


class LocalEmbeddingEncoder(EmbeddingEncoder):
    """
    Local CPU/GPU embedding encoder.
    Deterministic and offline.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def encode(self, texts: List[str]) -> List[List[float]]:
        vectors = self.model.encode(texts, normalize_embeddings=True)
        return vectors.tolist()
