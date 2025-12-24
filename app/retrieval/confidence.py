from app.schemas.contracts import ConfidenceScore, RetrievalResult


def score_confidence(retrieval: RetrievalResult) -> ConfidenceScore:
    """
    Phase 5 confidence heuristic:
    - multiple documents increase confidence
    - higher source reliability increases confidence
    - single weak document limits confidence
    """
    if not retrieval.documents:
        return ConfidenceScore(score=0.0)

    doc_count = len(retrieval.documents)

    # reliability is already embedded in retrieval_score indirectly
    base = retrieval.retrieval_score

    # redundancy bonus
    redundancy_bonus = min(0.2 * (doc_count - 1), 0.4)

    confidence = min(base + redundancy_bonus, 1.0)

    return ConfidenceScore(score=round(confidence, 2))
