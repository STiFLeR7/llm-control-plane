from typing import List, Optional

from bytez import Bytez

from app.embeddings.encoder import EmbeddingEncoder
from app.config import settings


class BytezEmbeddingEncoder(EmbeddingEncoder):
    """
    Bytez API embedding encoder using the official Bytez SDK.
    Uses model.run() for feature extraction (embeddings).
    """

    def __init__(self, model_override: Optional[str] = None, api_key: Optional[str] = None):
        self.api_key = api_key or settings.bytez_api_key
        if not self.api_key:
            raise RuntimeError("BYTEZ_API_KEY not configured")

        self.model_id = model_override or settings.bytez_embedding_model
        if not self.model_id:
            raise RuntimeError("BYTEZ_EMBEDDING_MODEL not configured")

        self.sdk = Bytez(self.api_key)

    def _extract_embedding(self, result):
        """Normalize Bytez response shape to a list of floats."""
        err = getattr(result, "error", None)
        if err:
            raise RuntimeError(f"Bytez error: {err}")

        if hasattr(result, "output"):
            output = result.output
        elif hasattr(result, "data"):
            output = result.data
        elif isinstance(result, dict):
            output = result.get("output") or result.get("data") or result.get("embeddings")
        else:
            output = result

        if not isinstance(output, list):
            raise RuntimeError(f"Unexpected Bytez response format: {result}")

        return output

    def encode(self, texts: List[str]) -> List[List[float]]:
        model = self.sdk.model(self.model_id)

        embeddings: List[List[float]] = []
        for text in texts:
            result = model.run(text)
            embeddings.append(self._extract_embedding(result))

        return embeddings
