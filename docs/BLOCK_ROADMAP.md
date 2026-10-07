# MIRA Staged Engineering Roadmap

MIRA is built strictly **block-by-block**. Each block establishes concrete, verifiable milestones before moving to the next.

---

## Block Breakdown

```
[Block 1: Foundation] ────> [Block 2: Brain Core] ────> [Block 3: Medical RAG]
                                                              │
[Block 6: 3D Character] <─── [Block 5: Voice Pipeline] <─── [Block 4: Healthcare Tools]
         │
[Block 7: External API & MediVerse Gateway]
```

### ✅ Block 1: Project Foundation (Current Block)
- **Goal:** Establish the complete, professional, standalone architecture and safety sentinel.
- **Deliverables:**
  - Independent project setup (zero external dependencies).
  - Strongly-typed configurations (`config/settings.py`).
  - Immutable product identity (`PRODUCT_IDENTITY`).
  - Clinical safety guardrails (`src/safety/rules.py`, `src/safety/red_flags.py`).
  - 4-Tier triage evaluation engine (`src/safety/triage.py`).
  - MIRA persona traits and dynamic prompt generator (`src/brain/personality.py`).
  - Foundational abstractions for Memory, Reasoning, Character, Voice, Tools, and Knowledge.
  - FastAPI service with `/health`, `/api/v1/info`, `/api/v1/verify-safety`, `/api/v1/triage-evaluate`.
  - Comprehensive automated test suite passing with 100% coverage of foundational rules.

---

### ⏳ Block 2: Brain Core & Clinical Reasoning
- **Goal:** Stateful clinical reasoning and natural dialogue orchestration.
- **Scope:**
  - Multi-turn conversation management.
  - Symptom inquiry decomposition.
  - LLM provider integration with prompt templates.
  - Working memory state persistence.

---

### ⏳ Block 3: Knowledge Base & Medical RAG
- **Goal:** Grounded clinical retrieval against verified healthcare guidelines.
- **Scope:**
  - Vector embeddings and vector store indexing.
  - Ingestion of CDC, WHO, and clinical guideline corpora.
  - Source citation generation in MIRA responses.

---

### ⏳ Block 4: Healthcare Tool Engine & Integrations
- **Goal:** Actionable execution of healthcare logistical tools.
- **Scope:**
  - Hospital discovery and geographic lookup.
  - Doctor search and specialty filtering.
  - Appointment scheduling assistance protocol.
  - Emergency ambulance dispatch workflow triggering.

---

### ⏳ Block 5: Voice Pipeline & Custom MIRA Voice
- **Goal:** Real-time conversational speech interaction.
- **Scope:**
  - Streaming Speech-to-Text (STT) ingestion.
  - Text-to-Speech (TTS) synthesis using custom MIRA nurse voice profile.
  - WebSocket full-duplex audio stream.

---

### ⏳ Block 6: Interactive Character & Avatar
- **Goal:** Visual AI companion with emotional presence and lip synchronization.
- **Scope:**
  - 3D character expression controller (warm, concerned, serious).
  - Real-time viseme mapping for accurate lip synchronization.
  - Emotional micro-reactions.

---

### ⏳ Block 7: MIRA API & External Integrations Gateway
- **Goal:** Expose enterprise-grade API contracts to external platforms.
- **Scope:**
  - External platform client adapters (e.g., MediVerse integration).
  - Client SDKs for web and mobile applications.
  - Production rate limiting, telemetry, and clinical compliance auditing.
