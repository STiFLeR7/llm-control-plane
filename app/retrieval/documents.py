from dataclasses import dataclass


@dataclass(frozen=True)
class Document:
    id: str
    title: str
    content: str
    source: str
    reliability: float  # 0.0 – 1.0
