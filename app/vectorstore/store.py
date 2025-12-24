from typing import List, Tuple


class VectorStore:
    """
    Deterministic vector search interface.
    """

    def upsert(self, ids: List[str], vectors: List[List[float]]) -> None:
        raise NotImplementedError

    def search(self, vector: List[float], k: int) -> List[Tuple[str, float]]:
        raise NotImplementedError
