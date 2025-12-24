from typing import List


class EmbeddingEncoder:
    """
    Interface for text embedding.
    Implementation can be local or API-based.
    """

    def encode(self, texts: List[str]) -> List[List[float]]:
        raise NotImplementedError
