import re
from app.schemas.contracts import RiskAssessment, RiskCategory, RiskLevel


MEDICAL_KEYWORDS = {
    "symptom", "diagnosis", "treatment", "medicine", "dose", "therapy", "disease"
}

LEGAL_KEYWORDS = {
    "law", "legal", "court", "contract", "sue", "liability"
}

FINANCIAL_KEYWORDS = {
    "invest", "investment", "tax", "loan", "profit", "stock", "trading", "startup"
}

POLICY_KEYWORDS = {
    "hack", "bypass", "exploit", "illegal", "piracy"
}

ADVICE_PATTERNS = [
    r"\bshould i\b",
    r"\bis it a good idea\b",
    r"\bwhat should i do\b",
    r"\bshould we\b",
    r"\bshould one\b",
]


def _contains_any(query: str, keywords: set[str]) -> bool:
    return any(re.search(rf"\b{k}\b", query) for k in keywords)


def _is_advice_seeking(query: str) -> bool:
    return any(re.search(pattern, query) for pattern in ADVICE_PATTERNS)


def classify_risk(query: str) -> RiskAssessment:
    q = query.lower()

    # 1. Policy violations (always highest priority)
    if _contains_any(q, POLICY_KEYWORDS):
        return RiskAssessment(RiskCategory.POLICY, RiskLevel.HIGH)

    # 2. Explicit advice / decision intent
    if _is_advice_seeking(q):
        if _contains_any(q, FINANCIAL_KEYWORDS):
            return RiskAssessment(RiskCategory.FINANCIAL, RiskLevel.HIGH)
        return RiskAssessment(RiskCategory.GENERAL, RiskLevel.MEDIUM)

    # 3. Domain-specific risks
    if _contains_any(q, MEDICAL_KEYWORDS):
        return RiskAssessment(RiskCategory.MEDICAL, RiskLevel.HIGH)

    if _contains_any(q, LEGAL_KEYWORDS):
        return RiskAssessment(RiskCategory.LEGAL, RiskLevel.HIGH)

    if _contains_any(q, FINANCIAL_KEYWORDS):
        return RiskAssessment(RiskCategory.FINANCIAL, RiskLevel.MEDIUM)

    # 4. Default
    return RiskAssessment(RiskCategory.GENERAL, RiskLevel.LOW)
