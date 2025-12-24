from app.retrieval.documents import Document


KNOWLEDGE_BASE = [
    Document(
        id="ai_001",
        title="Artificial Intelligence (General)",
        content=(
            "Artificial Intelligence (AI) refers to computer systems that "
            "can perform tasks that typically require human intelligence, "
            "including learning, reasoning, and pattern recognition."
        ),
        source="internal:baseline_knowledge",
        reliability=0.9,
    ),
    Document(
        id="ai_002",
        title="Artificial Intelligence (Overview)",
        content=(
            "AI is a field of computer science focused on building systems "
            "that can simulate intelligent behavior such as perception, "
            "decision-making, and problem-solving."
        ),
        source="internal:overview",
        reliability=0.85,
    ),
]
