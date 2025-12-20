import re
from app.schemas.contracts import RiskAssessment, RiskCategory, RiskLevel


MEDICAL_KEYWORDS = {
    "symptom", "diagnosis", "treatment", "medicine", "dose", "therapy", "disease"
}

LEGAL_KEYWORDS = {
    "law", "legal", "court", "contract", "sue", "liability"
}

FINANCIAL_KEYWORDS = {
    "invest", "investment", "tax", "loan", "profit", "stock", "trading"
}

POLICY_KEYWORDS = {
    "hack", "bypass", "exploit", "illegal", "piracy"
}


def _contains_any(query: str, keywords: set[str]) -> bool:
    query = query.lower()
    return any(re.search(rf"\b{k}\b", query) for k in keywords)


def classify_risk(query: str) -> RiskAssessment:
    q = query.lower()

    if _contains_any(q, MEDICAL_KEYWORDS):
        return RiskAssessment(RiskCategory.MEDICAL, RiskLevel.HIGH)

    if _contains_any(q, LEGAL_KEYWORDS):
        return RiskAssessment(RiskCategory.LEGAL, RiskLevel.HIGH)

    if _contains_any(q, FINANCIAL_KEYWORDS):
        return RiskAssessment(RiskCategory.FINANCIAL, RiskLevel.MEDIUM)

    if _contains_any(q, POLICY_KEYWORDS):
        return RiskAssessment(RiskCategory.POLICY, RiskLevel.HIGH)

    # Ambiguous advice-seeking language
    if re.search(r"\b(should i|is it safe|what happens if)\b", q):
        return RiskAssessment(RiskCategory.GENERAL, RiskLevel.MEDIUM)

    return RiskAssessment(RiskCategory.GENERAL, RiskLevel.LOW)
