# LLM Control Plane

> **Status: Phase 6B.7 — SUCCESSFULLY VALIDATED**  
> **Type: Controlled Inference Platform**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Validated-brightgreen)
![Architecture](https://img.shields.io/badge/Architecture-Event--Driven-orange)

## 📖 Overview

The **LLM Control Plane** is a deterministic, audit-first system designed to govern Large Language Model (LLM) interactions. Unlike standard RAG demos, this platform treats LLMs as optional *formatters* rather than decision agents. It enforces strict invariants around **risk**, **policy**, and **retrieval confidence** before any generation is allowed.

This system is built to solve the "last mile" problem of enterprise AI: **Control**. It ensures that:
- **Intent overrides evidence**: Advisory queries on sensitive topics (Financial, Medical, Legal) are blocked regardless of retrieved context.
- **No hallucination surface**: Nonsense queries result in confidence collapse and refusal.
- **Auditability**: Every decision—from risk classification to final eligibility—is logged authoritatively.

---

## 🏗 Architecture

The system operates on a linear, gated pipeline where every stage must pass for generation to occur.

```mermaid
graph TD
    UserQuery[User Query] --> RiskEngine[Risk Classifier]
    RiskEngine --> PolicyResolver[Policy Resolver]
    
    subgraph "Control Logic"
        PolicyResolver -->|Risk Level| EligibilityGate[Eligibility Gate]
        
        subgraph "Hybrid Retrieval"
            Retrieval[Retriever] -->|Keyword Filter| Candidates[Candidate Docs]
            Candidates -->|Embedding Rank| RankedDocs[Ranked Content]
        end
        
        RankedDocs --> Confidence[Confidence Scorer]
        Confidence -->|Score| EligibilityGate
    end

    EligibilityGate -->|ALLOW| Generator[LLM / Formatter]
    EligibilityGate -->|ABSTAIN| RefusalResponse[Refusal Message]
    
    Generator --> FinalResponse
    
    RiskEngine -.-> AuditLog[Audit Logger]
    PolicyResolver -.-> AuditLog
    Retrieval -.-> AuditLog
    EligibilityGate -.-> AuditLog
```

---

## 🚀 Key Features

### 1. Hybrid Retrieval Engine
Combines the precision of **embeddings** with the authority of **keyword filtering**.
- **Stage 1 (Filter)**: Hard keyword intersection to guarantee candidate relevance (`app/retrieval/retriever.py`).
- **Stage 2 (Rank)**: `sentence-transformers` (local) to rank candidates by semantic similarity.
- **Result**: Ranking improves recall, but does not override the fundamental keyword authority.

### 2. Deterministic Risk Classification
Uses a regex-driven heuristic engine (`app/core/risk_classifier.py`) to categorize intent.
- **Advisory Intent**: Questions like *"Should I invest?"* trigger high-risk flags.
- **Topic Separation**: Distinguishes between asking *about* "stocks" (Information) vs. asking for *advice* "should I buy stocks" (Advisory).

### 3. Policy Gating
Policy is the ultimate arbiter (`app/core/policy_resolver.py`).
- **High Risk**: Immediate `ABSTAIN`.
- **Low Confidence**: `ABSTAIN` (prevents hallucination on nonsense queries like "quantum pizza").
- **Allowed**: Only low-risk, high-confidence queries proceed to generation.

### 4. Confidence Scoring
Calculates a normalized confidence score based on retrieval density and semantic alignment (`app/retrieval/confidence.py`). This prevents the system from answering when it simply *doesn't know*.

---

## 🛠️ Validation Metrics (Phase 6B.7)

The system has been validated against three core invariants:

| Test Case | Query Type | Outcome | Reason |
| :--- | :--- | :--- | :--- |
| **Low-risk factual** | "What is AI?" | `ALLOW` | Keywords matched, Confidence high, Risk low. |
| **Advisory intent** | "Should I invest?" | `ABSTAIN` | **Intent detected**. Policy vetoed generation despite retrieval content. |
| **Nonsense** | "Explain quantum pizza" | `ABSTAIN` | **Confidence collapsed**. No grounded candidates found. |

**Key Takeaway**: Embeddings improved capability without weakening control. Intent overrides evidence.

---

## 🎨 UI & Demonstration

### Live Control Plane Console

The LLM Control Plane includes a modern, engineering-grade frontend that visualizes the governance pipeline in real-time.

#### Example 1: Factual Query (ALLOW)

![What is AI - ALLOW Response](assets/WhatisAI.png)

**System behavior:**
- Risk classification: **Low** (factual, informational intent)
- Confidence: **0.90** (strong retrieval match)
- Evidence: **Multiple sources** found and ranked
- **Decision**: `ALLOW` → Answer is rendered

---

#### Example 2: Advisory Query (ABSTAIN - Policy Block)

![Should I Invest - ABSTAIN Response](assets/ShouldIinvest.png)

**System behavior:**
- Risk classification: **High** (advisory intent detected)
- Policy: **Blocks** generation regardless of retrieval quality
- Confidence: **Irrelevant** (policy veto occurs first)
- Evidence: **Not evaluated** (intent override)
- **Decision**: `ABSTAIN` → Refusal message shown, answer suppressed

**Key insight**: Even with perfect retrieval, the system refuses. *This is by design.*

---

## 🛑 Why This System Refuses by Design

### The Core Principle

The LLM Control Plane treats **intent as the first-class decision gate**, not confidence or retrieval quality. This inverts the typical RAG architecture:

| Typical RAG | LLM Control Plane |
|-------------|-------------------|
| "If we can retrieve it, we can answer it" | "Intent first. Evidence second. Generation last." |
| Confidence → Allow | Policy + Risk → Confidence → Allow |
| Hallucination is a failure mode | Hallucination is prevented upstream |

### Why This Matters

#### 1. **Advisory Queries Are Fundamentally Unanswerable**

A question like *"Should I invest in tech stocks?"* is not a knowledge question—it's a judgment call.

- **What we can answer**: "What is the historical performance of tech stocks?"
- **What we cannot answer**: "Should *you* invest?"

The system detects this intent shift and refuses, not because it lacks information, but because the query requires domain expertise, personal financial context, and fiduciary responsibility. An AI system should never make that claim.

#### 2. **Policy Overrides Evidence**

Consider this scenario:
```
Query:     "What is the FDA approval process?"
Confidence: 0.95 (perfect retrieval)
Risk:      MEDICAL_ADVICE (advisory pattern detected)
Policy:    Immediate ABSTAIN
```

The system *could* answer. But the policy says: *"Not for medical advice, even if we're very confident."*

This is not a bug. **This is the point.** Risk assessment and policy belong in the control plane, not in the LLM's hands.

#### 3. **Refusals Are Intentional, Not Broken**

When you see `ABSTAIN`, it means:

- ✅ The system evaluated the query thoroughly
- ✅ One or more gates (risk, policy, confidence) were triggered
- ✅ A refusal was the correct decision
- ❌ The system did *not* fail silently or hallucinate

Contrast this with a typical LLM that says *"I can't answer that"* — which is actually just the model's learned politeness, not enforced governance.

### The Trade-off

**What we gain:**
- Trustworthiness (refusals are enforced, not learned)
- Auditability (every gate logs its decision)
- Predictability (behavior is deterministic)

**What we sacrifice:**
- Coverage (some queries are blocked, even if answerable)
- Optionality (the model cannot override policy)

This trade-off is **intentional** and is the entire reason this system exists.

---

## 💻 Tech Stack

- **Language**: Python 3.10+
- **Embeddings**: `sentence-transformers` (Local), support for API-based backends.
- **Vector Store**: In-Memory (for speed and determinism), extensible to FAISS/Chroma.
- **Architecture**: Modular, Interface-based (`app/core`, `app/retrieval`, `app/generation`).
- **Deployment**: Docker-ready structure (stateless application logic).

---

## ⚡ Quick Start

### Prerequisites
- Python 3.10+
- `pip`

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/llm-control-plane.git
   cd llm-control-plane
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   *Note: Ensure `sentence-transformers`, `numpy`, and standard utils are installed.*

3. **Run the Application**
   ```bash
   python -m app.main
   ```

### Configuration
Edit `app/config.py` to adjust system settings:

```python
@dataclass(frozen=True)
class Settings:
    environment: str = "local"
    embedding_backend: str = "local" # or "api"
    embedding_dim: int = 384     # aligned with all-MiniLM-L6-v2
```

---

## 📂 Directory Structure

```plaintext
llm-control-plane/
├── app/
│   ├── audit/          # Authoritative logging
│   ├── core/           # Risk, Policy, and Eligibility logic
│   ├── embeddings/     # Embedding factories (Local/API)
│   ├── generation/     # LLM integration point
│   ├── policies/       # Policy definitions
│   ├── retrieval/      # Hybrid retrieval engine
│   └── main.py         # Pipeline entry point
├── docs/               # Documentation
├── tests/              # Unit and integration tests
└── scripts/            # Setup and utility scripts
```

---

## 🤝 Contributing

1. **Audit First**: Any new feature must be logged in `app/audit`.
2. **Determinism**: Avoid introducing non-deterministic logic in `app/core`.
3. **Tests**: Run `pytest` before submitting PRs.

---

**© 2025 llm-control-plane | STiFLeR7**
