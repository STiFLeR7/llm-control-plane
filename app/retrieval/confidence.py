from app.schemas.contracts import ConfidenceScore, RetrievalResult


def score_confidence(retrieval: RetrievalResult) -> ConfidenceScore:
    return ConfidenceScore(score=retrieval.retrieval_score)
