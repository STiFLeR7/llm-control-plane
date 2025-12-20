Good. We now **freeze the system design**.
No code yet. This is the contract every file must obey.

Below is the **exact content** for
`docs/architecture/SYSTEM_DESIGN.md`
You can copy-paste this verbatim.

---

# LLM Control Plane — System Design

## 1. Purpose

This document defines the **authoritative system design** for the LLM Control Plane.

The goal of the system is **not** to improve LLM intelligence.
The goal is to **control, constrain, audit, and safely fail** LLM behavior in production.

The LLM is treated as a bounded, probabilistic component.
The system is deterministic and authoritative.

No component may bypass this design.

---

## 2. Core Design Principles

These principles are enforced structurally, not by convention.

1. **Control over creativity**
   Predictable behavior is prioritized over fluent output.

2. **Explicit failure is success**
   Abstention, refusal, and clarification are valid end states.

3. **Deterministic gating**
   All decisions about answering occur *outside* the model.

4. **Grounding before generation**
   No factual generation without verified sources.

5. **Traceability by default**
   Every inference must be reconstructable after the fact.

6. **Readable, production-grade code**
   Any engineer should understand the system in one sitting.

---

## 3. High-Level Request Pipeline

The system executes as a **strict linear pipeline**.

```
User Query
  → Risk Classification
  → Policy Resolution
  → Grounded Retrieval
  → Retrieval Confidence Scoring
  → Answer Eligibility Gate
      → (Abstain | Clarify | Generate)
  → Response Packaging
  → Audit Logging
```

No step is optional.
No step may be skipped.

---

## 4. Component Responsibilities & Contracts

### 4.1 Risk Classification Layer

**Location:** `app/core/risk_classifier.py`

**Responsibility**
Classify the incoming query by domain and risk level *before* any retrieval or generation.

**Inputs**

* raw user query (string)

**Outputs**

```json
{
  "risk_category": "medical | legal | financial | policy | general",
  "risk_level": "high | medium | low"
}
```

**Failure Modes**

* Unknown category → default to `policy + high`
* Ambiguous intent → escalate risk, never downgrade

No model calls are allowed here.

---

### 4.2 Policy Resolver

**Location:** `app/core/policy_resolver.py`

**Responsibility**
Translate risk classification into **allowed system behavior**.

**Inputs**

* risk category
* risk level

**Outputs**

```json
{
  "mode": "strict | conservative | normal",
  "min_confidence": 0.0–1.0,
  "retrieval_required": true | false,
  "generation_allowed": true | false
}
```

**Failure Modes**

* Missing policy → deny generation
* Conflicting rules → stricter policy wins

This is a deterministic rules engine.

---

### 4.3 Grounded Retrieval Layer

**Location:** `app/retrieval/retriever.py`

**Responsibility**
Retrieve verifiable context required to answer the query.

**Inputs**

* user query
* policy constraints

**Outputs**

```json
{
  "documents": [...],
  "retrieval_score": 0.0–1.0
}
```

**Hard Rule**
If retrieval is required and zero documents are found → generation is forbidden.

Retrieval failure is not an error. It is a valid system outcome.

---

### 4.4 Retrieval Confidence Scoring

**Location:** `app/retrieval/confidence.py`

**Responsibility**
Quantify trustworthiness of retrieved context.

**Inputs**

* retrieved documents
* retrieval metadata

**Outputs**

```json
{
  "confidence_score": 0.0–1.0
}
```

**Failure Modes**

* Insufficient signal → low confidence
* Conflicting sources → confidence penalty

Confidence is computed, not guessed.

---

### 4.5 Answer Eligibility Gate

**Location:** `app/core/eligibility_gate.py`

**Responsibility**
Make the final decision on whether the system may answer.

**Inputs**

* policy output
* confidence score

**Outputs**

```json
{
  "decision": "ALLOW | ABSTAIN | CLARIFY",
  "reason": "human-readable explanation"
}
```

**Critical Rule**
No LLM call is allowed unless this gate returns `ALLOW`.

This is the most important control point in the system.

---

### 4.6 Policy-Aware Generation

**Location:** `app/generation/generator.py`

**Responsibility**
Generate responses *only* within system-approved constraints.

**Inputs**

* user query
* grounded context
* policy mode

**Outputs**

* model-generated text (bounded)

**Constraints**

* No speculation
* No unsupported facts
* Mode-specific strictness applied

The model produces text.
The system owns authority.

---

### 4.7 Audit & Observability Layer

**Location:** `app/audit/logger.py`

**Responsibility**
Persist a complete, immutable trace of every request.

**Logged Fields (minimum)**

```json
{
  "request_id",
  "timestamp",
  "user_query",
  "risk_category",
  "policy_mode",
  "retrieval_score",
  "confidence_score",
  "decision",
  "response_type",
  "model_output"
}
```

If it is not logged, it did not happen.

---

## 5. Chat Continuity & State Rehydration

This system supports **conversation continuation**, not free-form memory.

Persisted state includes:

* last valid pipeline state
* active policy mode
* conversation context hash
* system configuration version

On new chat:

* attempt safe rehydration
* resume from last valid state
* if recovery fails → explicitly state loss of context

Silent resets are forbidden.

---

## 6. Designed Failure Scenarios (Examples)

* No reliable sources → abstain
* High-risk + low confidence → refuse
* Ambiguous query → request clarification

Failure is an intentional output, not a fallback.

---

## 7. Phase-1 Exit Criteria

Phase 1 is complete only if:

* All components have clear responsibilities
* Inputs / outputs are unambiguous
* Failure modes are documented
* No code contradicts this document

Only after this is frozen do we proceed to implementation.

---

**This system is not about proving AI is powerful.
It is about proving AI can be controlled.**

---
