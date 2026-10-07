# MIRA Architecture Blueprint

## 1. System Philosophy & Independence

**MIRA (Medical Intelligent Response Assistant)** is an independent, standalone AI healthcare product designed from first principles as an interactive AI healthcare companion and AI Nurse Assistant.

### Key Architectural Tenet: Complete Decoupling
- **Standalone Autonomy:** MIRA operates as an independent service with its own reasoning engine, safety sentinel, knowledge base, and API.
- **No External Upstream Dependencies:** MIRA contains **zero** dependencies on external consumer platforms such as MediVerse.
- **Clean Gateway Model:** MediVerse and future healthcare platforms will connect to MIRA purely as external API clients or downstream consumers via the MIRA API.

---

## 2. Multi-Tier Architecture Diagram

```
                         MIRA
                          │
             ┌────────────┼────────────┐
             │            │            │
           BRAIN       CHARACTER      VOICE
             │            │            │
        Reasoning      Animation       STT
        Knowledge      Expressions     TTS
        Context        Reactions       Voice ID
        Memory         Lip Sync
             │
             └────────────┬────────────┘
                          │
                     MIRA CORE
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
      SAFETY            TOOLS           KNOWLEDGE
        │                 │                 │
      Triage          Healthcare        RAG
      Escalation      Integrations      Guidelines
      Red Flags       External APIs     Medical KB
        │                 │                 │
        └─────────────────┼─────────────────┘
                          │
                      MIRA API
                          │
                External Applications
                          │
                 ┌────────┴────────┐
                 │                 │
             MediVerse        Future Apps
```

---

## 3. Tier Breakdown & Subsystems

### Tier 1: Interaction & Perception Layer

The interaction layer governs how MIRA perceives, expresses, and communicates with the patient:

#### A. BRAIN
- **Reasoning (`src/brain/reasoning.py`):** Multi-step clinical deconstruction, differential consideration, and evidence evaluation before response generation.
- **Personality (`src/brain/personality.py`):** System prompt engineering that enforces bedside manner, emotional warmth, and urgency-based tone modulation.
- **Memory (`src/brain/memory.py`):**
  - *Short-Term Memory:* Current conversational turn context, reported symptoms, active emotional state.
  - *Long-Term Memory:* Longitudinal patient health profile, chronic conditions, medication allergies, and historical interaction preferences.
- **Context (`src/core/context.py`):** Turn-by-turn state tracker storing active urgency classification and clinical red-flag triggers.

#### B. CHARACTER
- **Expressions (`src/character/expressions.py`):** Emotional facial states (`WARM`, `CALM`, `EMPATHETIC`, `CONCERNED`, `SERIOUS`, `LISTENING`).
- **Reactions:** Event-driven behavioral transitions based on triage severity.
- **Lip Synchronization (`src/character/lip_sync.py`):** MPEG-4 / Oculus compatible viseme frame contracts synchronized with acoustic speech generation.

#### C. VOICE
- **Speech-to-Text / STT (`src/voice/stt.py`):** Real-time audio stream transcription with confidence scoring.
- **Text-to-Speech / TTS (`src/voice/tts.py`):** Speech synthesis adhering to the custom **MIRA Signature Voice Profile** (`mira-caring-nurse-v1`), balancing warmth, clarity, and pacing.
- **Streaming Audio (`src/voice/stream.py`):** Bidirectional low-latency audio packet delivery.

---

### Tier 2: MIRA Core

MIRA Core represents the medical intellect, clinical safety governor, and operational tooling:

#### A. SAFETY
- **Identity Invariant Enforcement (`src/safety/rules.py`):** Strict verification ensuring MIRA **never** claims to be human ("I'm MIRA, an AI healthcare assistant").
- **Professional Non-Replacement (`src/safety/rules.py`):** Strict verification ensuring MIRA **never** pretends to replace doctors, nurses, or emergency dispatchers.
- **Clinical Red-Flag Catalog (`src/safety/red_flags.py`):** Pattern-matched detection of life-threatening indicators (cardiac, acute stroke FAST signs, severe respiratory distress, anaphylaxis, massive trauma).
- **Clinical Triage Engine (`src/safety/triage.py`):** 4-tier triage priority classification (`EMERGENCY`, `URGENT`, `ROUTINE`, `INFORMATIONAL`).
- **Regulatory Disclaimers (`src/safety/disclaimers.py`):** Context-aware medical legal disclaimers.

#### B. TOOLS
- **Tool Registry (`src/tools/registry.py`):** Decoupled execution orchestrator.
- **Base Healthcare Tool (`src/tools/base.py`):** Standard abstract contracts for future capabilities:
  - Hospital discovery
  - Doctor lookup & availability
  - Appointment scheduling assistance
  - Ambulance and emergency workflow activation

#### C. KNOWLEDGE
- **Evidence-Based RAG (`src/knowledge/base.py`):** Protocol for clinical guideline document retrieval.
- **Medical KB Registry (`src/knowledge/registry.py`):** Verified references (AHA, CDC, WHO guidelines) for clinical grounding.

---

### Tier 3: MIRA API & External Ecosystem

- **FastAPI Core (`src/api/`):** Asynchronous, high-performance web service providing REST endpoints and WebSocket protocols.
- **Decoupled Consumer Gateway:** External platforms (e.g., MediVerse, mobile apps, clinic portals) communicate exclusively over clean OpenAPI contracts without internal coupling.
