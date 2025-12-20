from app.schemas.contracts import RetrievalResult


def retrieve_context(query: str, policy) -> RetrievalResult:
    return RetrievalResult(
        documents=[],
        retrieval_score=0.0,
    )
