import re
from app.schemas.contracts import RetrievalResult
from app.retrieval.knowledge_base import KNOWLEDGE_BASE
from app.retrieval.index import RetrievalIndex


_index = RetrievalIndex()


def _normalize(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def retrieve_context(query: str, policy) -> RetrievalResult:
    if not policy.retrieval_required:
        return RetrievalResult(documents=[], retrieval_score=0.0, candidate_count=0)

    query_tokens = _normalize(query)

    # 1. Keyword filtering (authoritative)
    candidates = []
    for doc in KNOWLEDGE_BASE:
        doc_tokens = _normalize(doc.content)
        if query_tokens & doc_tokens:
            candidates.append(doc)

    if not candidates:
        return RetrievalResult(documents=[], retrieval_score=0.0, candidate_count=0)

    # 2. Embedding ranking (non-authoritative)
    ranked_ids = _index.search(query, k=len(candidates))
    ranked_map = {doc_id: score for doc_id, score in ranked_ids}

    # 3. Sort candidates by embedding similarity
    candidates.sort(
        key=lambda d: ranked_map.get(d.id, 0.0),
        reverse=True,
    )

    documents = [doc.content for doc in candidates]

    retrieval_score = len(documents) / len(KNOWLEDGE_BASE)

    return RetrievalResult(
        documents=documents,
        retrieval_score=retrieval_score,
        candidate_count=len(candidates),
    )
