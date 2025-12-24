from app.schemas.contracts import PolicyDecision, RiskLevel


def resolve_policy(risk) -> PolicyDecision:
    if risk.level == RiskLevel.HIGH:
        return PolicyDecision(
            mode="strict",
            min_confidence=0.85,
            retrieval_required=True,
            generation_allowed=False,
        )

    if risk.level == RiskLevel.MEDIUM:
        return PolicyDecision(
            mode="conservative",
            min_confidence=0.7,
            retrieval_required=True,
            generation_allowed=True,
        )

    return PolicyDecision(
        mode="normal",
        min_confidence=0.5,
        retrieval_required=True,
        generation_allowed=True,
    )
