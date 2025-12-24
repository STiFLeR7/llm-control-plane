from app.schemas.contracts import ConfidenceScore, RetrievalResult


def score_confidence(retrieval: RetrievalResult) -> ConfidenceScore:
    """
    Phase 6B confidence guardrails:
    - embeddings do not increase confidence
    - low candidate diversity caps confidence
    """

    if not retrieval.documents:
        return ConfidenceScore(score=0.0)

    base = retrieval.retrieval_score

    # Guard 1: single candidate = limited certainty
    if retrieval.candidate_count == 1:
        base = min(base, 0.6)

    # Guard 2: absolute ceiling
    confidence = min(base, 0.9)

    return ConfidenceScore(score=round(confidence, 2))
