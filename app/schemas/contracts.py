from dataclasses import dataclass, asdict
from enum import Enum
from typing import List
from enum import Enum

class ReasonCode(str, Enum):
    POLICY_BLOCK = "policy_block"
    LOW_CONFIDENCE = "low_confidence"
    NO_EVIDENCE = "no_evidence"
    SAFE_TO_ANSWER = "safe_to_answer"
class RiskCategory(str, Enum):
    MEDICAL = "medical"
    LEGAL = "legal"
    FINANCIAL = "financial"
    POLICY = "policy"
    GENERAL = "general"


class RiskLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Decision(str, Enum):
    ALLOW = "ALLOW"
    ABSTAIN = "ABSTAIN"
    CLARIFY = "CLARIFY"


@dataclass(frozen=True)
class RiskAssessment:
    category: RiskCategory
    level: RiskLevel

    def to_dict(self) -> dict:
        return {
            "category": self.category.value,
            "level": self.level.value,
            "category": self.category.MEDICAL,
            "level": self.level.HIGH,
        }


@dataclass(frozen=True)
class PolicyDecision:
    mode: str
    min_confidence: float
    retrieval_required: bool
    generation_allowed: bool

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class RetrievalResult:
    documents: List[str]
    retrieval_score: float
    candidate_count: int  # NEW

    def to_dict(self) -> dict:
        return {
            "documents": self.documents,
            "retrieval_score": self.retrieval_score,
            "candidate_count": self.candidate_count,
        }

@dataclass(frozen=True)
class ConfidenceScore:
    score: float

    def to_dict(self) -> dict:
        return {"score": self.score}


@dataclass(frozen=True)
class EligibilityDecision:
    decision: Decision
    reason: str
    reason_code: ReasonCode

    def to_dict(self) -> dict:
        return {
            "decision": self.decision.value,
            "reason": self.reason,
            "reason_code": self.reason_code.value,
        }   
