from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class EvidenceBundle:
    query: str
    documents: List[str]
    confidence: float
