from app.embeddings.factory import get_embedding_encoder
from app.vectorstore.memory import InMemoryVectorStore
from app.retrieval.knowledge_base import KNOWLEDGE_BASE


class RetrievalIndex:
    def __init__(self):
        self.encoder = get_embedding_encoder()
        self.store = InMemoryVectorStore()

        texts = [doc.content for doc in KNOWLEDGE_BASE]
        ids = [doc.id for doc in KNOWLEDGE_BASE]

        vectors = self.encoder.encode(texts)
        self.store.upsert(ids, vectors)

    def search(self, query: str, k: int = 3):
        query_vec = self.encoder.encode([query])[0]
        return self.store.search(query_vec, k)
