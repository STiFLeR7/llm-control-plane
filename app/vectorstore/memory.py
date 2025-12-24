import numpy as np
from typing import List, Tuple

from app.vectorstore.store import VectorStore


class InMemoryVectorStore(VectorStore):
    def __init__(self):
        self.vectors: dict[str, np.ndarray] = {}

    def upsert(self, ids: List[str], vectors: List[List[float]]) -> None:
        for i, v in zip(ids, vectors):
            self.vectors[i] = np.array(v)

    def search(self, vector: List[float], k: int) -> List[Tuple[str, float]]:
        query = np.array(vector)
        scores = []

        for doc_id, vec in self.vectors.items():
            score = float(np.dot(query, vec))
            scores.append((doc_id, score))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:k]
