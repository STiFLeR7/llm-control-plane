from app.schemas.contracts import EligibilityDecision, Decision


def evaluate_eligibility(policy, confidence) -> EligibilityDecision:
    if not policy.generation_allowed:
        return EligibilityDecision(
            decision=Decision.ABSTAIN,
            reason="Generation not permitted by policy",
        )

    if confidence.score < policy.min_confidence:
        return EligibilityDecision(
            decision=Decision.ABSTAIN,
            reason="Confidence below required threshold",
        )

    return EligibilityDecision(
        decision=Decision.ALLOW,
        reason="All conditions satisfied",
    )
