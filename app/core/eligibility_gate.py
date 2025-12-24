from app.schemas.contracts import EligibilityDecision, Decision, ReasonCode


def evaluate_eligibility(policy, confidence) -> EligibilityDecision:
    if not policy.generation_allowed:
        return EligibilityDecision(
            decision=Decision.ABSTAIN,
            reason="Generation not permitted by policy",
            reason_code=ReasonCode.POLICY_BLOCK,
        )

    if confidence.score < policy.min_confidence:
        return EligibilityDecision(
            decision=Decision.ABSTAIN,
            reason="Confidence below required threshold",
            reason_code=ReasonCode.LOW_CONFIDENCE,
        )

    return EligibilityDecision(
        decision=Decision.ALLOW,
        reason="All conditions satisfied",
        reason_code=ReasonCode.SAFE_TO_ANSWER,
    )
