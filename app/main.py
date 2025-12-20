from uuid import uuid4
from datetime import datetime, timezone

from app.core.risk_classifier import classify_risk
from app.core.policy_resolver import resolve_policy
from app.core.eligibility_gate import evaluate_eligibility
from app.retrieval.retriever import retrieve_context
from app.retrieval.confidence import score_confidence
from app.generation.generator import generate_answer
from app.audit.logger import audit_log


def handle_request(user_query: str) -> dict:
    """
    Handle a single user query through the LLM control pipeline.

    Deterministic, auditable, and safe by default.
    """
    request_id = str(uuid4())
    timestamp = datetime.now(timezone.utc).isoformat()

    # 1. Risk classification
    risk = classify_risk(user_query)

    # 2. Policy resolution
    policy = resolve_policy(risk)

    # 3. Grounded retrieval
    retrieval = retrieve_context(user_query, policy)

    # 4. Confidence scoring
    confidence = score_confidence(retrieval)

    # 5. Eligibility decision
    eligibility = evaluate_eligibility(policy, confidence)

    # 6. Controlled answer generation (only if allowed)
    answer = None
    if eligibility.decision.value == "ALLOW":
        answer = generate_answer(user_query, retrieval.documents)

    # 7. API-safe response (frontend & Docker ready)
    response = {
        "request_id": request_id,
        "status": eligibility.decision.value,
        "message": eligibility.reason,
        "answer": answer,
    }

    # 8. Mandatory audit logging (authoritative record)
    audit_log(
        request_id=request_id,
        timestamp=timestamp,
        user_query=user_query,
        risk=risk.to_dict(),
        policy=policy.to_dict(),
        retrieval=retrieval.to_dict(),
        confidence=confidence.to_dict(),
        decision=eligibility.to_dict(),
        response=response,
    )

    return response


if __name__ == "__main__":
    while True:
        query = input("query> ").strip()
        if not query:
            break
        print(handle_request(query))
