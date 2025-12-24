# Explanation Model (v0.3)

Each response may include:

- status: ALLOW | ABSTAIN
- reason_code:
  - policy_block
  - low_confidence
  - no_evidence
  - safe_to_answer
- confidence: float (0.0–1.0)
- evidence_count: integer
- answer: string | null

The UI must:

- Never invent explanations
- Never hide refusals
- Never rephrase reason codes creatively
