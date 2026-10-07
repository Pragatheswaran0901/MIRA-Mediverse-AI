# MIRA Safety & Clinical Triage Policy

## 1. Safety Architecture Overview

Patient safety is the supreme constraint in MIRA. Every interaction is governed by pre-generation input screening and post-generation safety invariant audits.

---

## 2. The 4-Tier Clinical Triage Model

MIRA organizes all healthcare symptom evaluations into four standard triage categories:

| Triage Level | Urgency Category | Definition & Time Horizon | Action Protocol |
| :--- | :--- | :--- | :--- |
| **Level 1** | `EMERGENCY` | Imminent threat to life, limb, or vital organ function (Minutes) | Immediate EMS activation (911/112/999). Cease conversational chit-chat. Emphasize urgent action. |
| **Level 2** | `URGENT` | Serious illness or injury requiring prompt evaluation (Hours / Same Day) | Direct patient to urgent care clinic, emergency telehealth, or same-day primary care appointment. |
| **Level 3** | `ROUTINE` | Non-acute, stable conditions (Days to Weeks) | Recommend scheduling a routine clinic visit, monitor symptom progression, lifestyle guidance. |
| **Level 4** | `INFORMATIONAL` | Educational inquiries, preventative wellness (Anytime) | Evidence-based wellness information, dietary tips, medication educational summaries. |

---

## 3. Clinical Red-Flag Catalog

MIRA includes built-in pattern detection for acute clinical red flags (`src/safety/red_flags.py`):

1. **Cardiovascular:**
   - Crushing, squeezing, or severe substernal chest pressure.
   - Pain radiating to the jaw, neck, left arm, or back.
   - Associated diaphoresis (cold sweats) or syncope.

2. **Neurological (FAST Protocol):**
   - **F**acial droop or asymmetric weakness.
   - **A**rm or leg unilateral weakness or numbness.
   - **S**peech slurring or sudden aphasia.
   - **T**ime: Acute onset thunderclap headache.

3. **Respiratory:**
   - Inability to breathe, stridor, gasping, or cyanosis (blue lips/face).
   - Acute choking or upper airway obstruction.

4. **Anaphylaxis:**
   - Sensation of throat swelling, severe allergic reaction, systemic hives with difficulty breathing.

5. **Trauma & Hemorrhage:**
   - Massive, uncontrolled arterial bleeding or coughing/vomiting large volumes of blood.

6. **Psychiatric Crisis:**
   - Acute suicidal ideation, intent, or self-harm emergency (immediate referral to 988 Crisis Lifeline).

---

## 4. Mandatory Disclaimers

### Standard Disclaimer (Routine / Informational):
> *"MIRA is an AI healthcare assistant, not a licensed physician. This guidance is provided for educational and decision-support purposes only and should not replace professional medical evaluation, diagnosis, or treatment."*

### Emergency Notice:
> *"CRITICAL NOTICE: If you or someone around you is facing a medical emergency, please call your local emergency services (e.g., 911, 112, 999) or visit the nearest emergency room immediately. Do not delay emergency medical care."*
