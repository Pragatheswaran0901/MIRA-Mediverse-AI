# MIRA (Medical Intelligent Response Assistant)

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com)
[![Pydantic v2](https://img.shields.io/badge/Pydantic-v2.8+-E92063.svg)](https://docs.pydantic.dev/)
[![Tests Passing](https://img.shields.io/badge/tests-28%20passed-brightgreen.svg)]()
[![Status](https://img.shields.io/badge/status-Block%201%3A%20Foundation-success.svg)]()

> **MIRA** is an independent, standalone AI healthcare companion and AI Nurse Assistant built from first principles.

---

## 🌟 Product Vision

MIRA is built to be an **intelligent, empathetic healthcare companion** rather than a generic chatbot. Over staged engineering blocks, MIRA will provide:

- **Natural Clinical Conversation:** Dialogue designed around bedside manner and clinical reasoning.
- **Symptom Triage & Guidance:** 4-tier triage severity classification (`EMERGENCY`, `URGENT`, `ROUTINE`, `INFORMATIONAL`).
- **Emergency Red-Flag Detection:** Immediate identification of acute life-threatening situations (cardiac, stroke FAST signs, respiratory distress).
- **Evidence-Based Knowledge:** RAG-grounded retrieval from trusted clinical medical guidelines.
- **Healthcare Tool Integrations:** Modular tools for hospital discovery, doctor lookup, appointment booking, and emergency ambulance dispatch.
- **Custom Signature Voice:** Warm, calm, real-time voice synthesis (`mira-caring-nurse-v1`).
- **Interactive Visual Character:** Real-time facial expressions, emotional reactions, and viseme lip synchronization.
- **Independent & Decoupled:** MIRA operates as an autonomous product. Downstream platforms (such as MediVerse) integrate cleanly as external consumers via MIRA's public API.

---

## 🧭 MIRA Personality & Directives

```
• Friendly like a trusted companion
• Caring like a nurse
• Intelligent like an AI
• Calm & empathetic
• Confident but not overconfident
• Concise and serious during emergencies
• Warm during normal conversation
• Never judgmental
• Never robotic
```

### Inviolable Safety Invariants:
1. **Never Claim to be Human:**
   - ✅ *Correct:* `"I'm MIRA, an AI healthcare assistant."`
   - ❌ *Incorrect:* `"I'm your human nurse."`
2. **Never Pretend to Replace Licensed Professionals:**
   - MIRA does not replace doctors, nurses, or emergency medical services.
   - Clinical red flags immediately activate emergency protocols directing the user to dial 911 / 112 / 999.

---

## 🏛️ Architecture

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

## 📁 Repository Structure

```
MIRA/
├── .env.example                     # Environment configuration template
├── .gitignore                       # Git ignore specifications
├── pyproject.toml                   # Project metadata and dependencies
├── requirements.txt                 # Pinned dependencies
├── README.md                        # Project root documentation
├── docs/
│   ├── ARCHITECTURE.md              # Exhaustive multi-tier architecture design
│   ├── PERSONALITY_GUIDELINES.md    # Persona rules and linguistic standards
│   ├── SAFETY_AND_TRIAGE_POLICY.md  # 4-tier triage model & red flags
│   └── BLOCK_ROADMAP.md             # Phased engineering roadmap
├── config/
│   ├── __init__.py
│   └── settings.py                  # Pydantic BaseSettings environment loader
├── src/
│   ├── __init__.py
│   ├── core/                        # Data contracts, identity, context, exceptions
│   ├── brain/                       # Persona engine, memory & reasoning protocols
│   ├── safety/                      # Red-flag detector, triage engine, disclaimers
│   ├── character/                   # Expression states, reactions, lip sync visemes
│   ├── voice/                       # STT, TTS voice profile, streaming contracts
│   ├── tools/                       # Decoupled healthcare tool registry & base classes
│   ├── knowledge/                   # Evidence-based medical guideline retrieval
│   ├── api/                         # FastAPI routes (health, info, safety verify)
│   └── main.py                      # Application server entrypoint
└── tests/
    ├── test_foundation.py           # Settings and immutable identity tests
    ├── test_safety.py               # Red flag detection and safety invariant tests
    ├── test_personality.py          # Persona traits and prompt modulation tests
    └── test_api.py                  # API endpoint integration tests
```

---

## 🚀 Quick Start

### 1. Environment Setup
```powershell
# Create and activate virtual environment
py -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment
```powershell
Copy-Item .env.example .env
```

### 3. Run Automated Test Suite
```powershell
.\.venv\Scripts\pytest.exe -v
```

### 4. Launch MIRA API Server
```powershell
.\.venv\Scripts\python.exe -m src.main
```
Server runs at `http://127.0.0.1:8000`. Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

---

## 📡 API Endpoints (Block 1)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Subsystem readiness and health status |
| `GET` | `/api/v1/info` | Product identity, persona traits, and architecture tiers |
| `POST` | `/api/v1/verify-safety` | Audits candidate text for safety policy compliance |
| `POST` | `/api/v1/triage-evaluate` | Evaluates symptom severity into 4-tier triage classification |

---

## 🛣️ Development Roadmap

- [x] **Block 1: Project Foundation** *(Current)*
- [ ] **Block 2: Brain Core & Clinical Reasoning**
- [ ] **Block 3: Knowledge Base & Medical RAG**
- [ ] **Block 4: Healthcare Tool Engine & Integrations**
- [ ] **Block 5: Voice Pipeline & Custom MIRA Voice**
- [ ] **Block 6: Interactive Character & Avatar**
- [ ] **Block 7: MIRA API & External Integrations Gateway**
