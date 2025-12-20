from app.schemas.contracts import PolicyDecision, RiskLevel


def resolve_policy(risk) -> PolicyDecision:
    if risk.level == RiskLevel.HIGH:
        return PolicyDecision(
            mode="strict",
            min_confidence=0.8,
            retrieval_required=True,
            generation_allowed=False,
        )

    return PolicyDecision(
        mode="normal",
        min_confidence=0.3,
        retrieval_required=False,
        generation_allowed=True,
    )
