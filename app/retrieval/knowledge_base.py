from app.retrieval.documents import Document


KNOWLEDGE_BASE = [
    Document(
        id="ai_001",
        title="Artificial Intelligence",
        content=(
            "Artificial Intelligence (AI) refers to computer systems that "
            "can perform tasks that typically require human intelligence, "
            "such as learning, reasoning, and pattern recognition."
        ),
        source="internal:baseline_knowledge",
    ),
]
