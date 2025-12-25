from app.embeddings.factory import get_embedding_encoder
from app.vectorstore.memory import InMemoryVectorStore
from app.retrieval.knowledge_base import KNOWLEDGE_BASE


class RetrievalIndex:
    def __init__(self):
        self.store = InMemoryVectorStore()

        # Default encoder for indexing
        encoder = get_embedding_encoder()
        texts = [doc.content for doc in KNOWLEDGE_BASE]
        ids = [doc.id for doc in KNOWLEDGE_BASE]

        vectors = encoder.encode(texts)
        self.store.upsert(ids, vectors)

    def search(self, query: str, k: int, embedding_model: str | None = None):
        encoder = get_embedding_encoder(embedding_model)  # UPDATED
        query_vec = encoder.encode([query])[0]
        return self.store.search(query_vec, k)
