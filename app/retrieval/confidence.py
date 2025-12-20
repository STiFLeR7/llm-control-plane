from app.schemas.contracts import ConfidenceScore, RetrievalResult


def score_confidence(retrieval: RetrievalResult) -> ConfidenceScore:
    """
    Confidence is derived strictly from retrieval quality.
    """
    if not retrieval.documents:
        return ConfidenceScore(score=0.0)

    # In Phase 4, confidence == retrieval score
    return ConfidenceScore(score=retrieval.retrieval_score)
