import re
from app.schemas.contracts import RetrievalResult
from app.retrieval.knowledge_base import KNOWLEDGE_BASE


def _normalize(text: str) -> set[str]:
    """
    Normalize text into lowercase alphanumeric tokens.
    """
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def retrieve_context(query: str, policy) -> RetrievalResult:
    """
    Deterministic keyword-based retrieval against a controlled knowledge base.
    """
    if not policy.retrieval_required:
        return RetrievalResult(documents=[], retrieval_score=0.0)

    query_tokens = _normalize(query)
    matched_docs = []

    for doc in KNOWLEDGE_BASE:
        doc_tokens = _normalize(doc.content)
        if query_tokens & doc_tokens:
            matched_docs.append(doc)

    score = min(len(matched_docs) / len(KNOWLEDGE_BASE), 1.0) if matched_docs else 0.0

    return RetrievalResult(
        documents=[doc.content for doc in matched_docs],
        retrieval_score=score,
    )
