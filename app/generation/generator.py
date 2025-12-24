from app.generation.evidence import EvidenceBundle


def generate_answer(bundle: EvidenceBundle) -> str:
    """
    Phase 6B generator:
    - summarization only
    - no new facts
    - no advice
    """

    # Placeholder (no LLM yet)
    # For now, return the most representative document
    return bundle.documents[0]
