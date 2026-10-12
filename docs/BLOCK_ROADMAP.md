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

### ✅ Block 1: Project Foundation (Completed)
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

### ✅ Block 2: Character Asset Foundation (Completed)
- **Goal:** Establish canonical visual identity anchor, multi-layer architecture, and data-driven state system for MIRA character.
- **Canonical Anchor:** `MIRA_FACE_MODEL` (`MIRA_FACE_MODEL_v1`, SHA256: `bf3b7cdc290d28ca7500b3d55679cbd98a397b4ec873dd86e8c910c46d1b44dc`).
- **Deliverables:**
  - Standardized character asset pipeline (`assets/mira/identity`, `reference`, `character`, `face`, `expressions`, `animation`, `audio`).
  - Immutable character identity contract (`src/character/identity.py`, `MIRA_CHARACTER_IDENTITY`).
  - 13 canonical data-driven character states (`src/character/states.py`, `IDLE`, `GREETING`, `LISTENING`, `THINKING`, `SPEAKING`, `FRIENDLY`, `CONCERNED`, `SERIOUS`, `REASSURING`, `EMERGENCY`, `ESCALATING`, `CALMING`, `COMPLETED`).
  - 10-layer visual stack (`src/character/layers.py`: BACKGROUND, BODY, UNIFORM, HEAD, HAIR, FACE, EYES, EYEBROWS, MOUTH, ACCESSORIES).
  - Reusable decoupled component (`src/character/component.py`, `MiraCharacter`, strict separation of AI logic).
  - Responsive Web Component & CSS (`src/character/static/mira-character.js`, `mira-character.css`).
  - Interactive viewer console (`/character`, `src/character/static/viewer.html`).
  - Dormant future animation capability contracts (`src/character/animation_hooks.py`).
  - 5 Character API endpoints (`/api/v1/character/*`).
  - 100% passing tests (41/41 tests passing).

---

### ⏳ Block 3: Brain Core & Clinical Reasoning
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
