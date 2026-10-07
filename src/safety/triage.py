"""MIRA Triage Classification and Escalation Engine.

Evaluates symptom severity and outputs triage priority classifications.
"""

import re
from pydantic import BaseModel, Field
from src.core.contracts import UrgencyLevel
from src.safety.red_flags import detect_red_flags, RedFlagItem
from src.safety.disclaimers import get_disclaimer_for_urgency


# Patterns indicating urgent but not immediately life-threatening symptoms
URGENT_PATTERNS = [
    r"\bhigh fever\b",
    r"\bfever (over|above|exceeding) 103\b",
    r"\bsevere abdominal pain\b",
    r"\bpersistent vomiting\b",
    r"\bdeep (cut|laceration|wound)\b",
    r"\bsuspected fracture\b",
    r"\bsprained (ankle|wrist)\b",
    r"\binability to keep fluids down\b",
]

# Patterns indicating routine symptoms
ROUTINE_PATTERNS = [
    r"\bmild (cough|cold|headache|fever)\b",
    r"\brunning nose\b",
    r"\bsore throat\b",
    r"\brash without fever\b",
    r"\bback ache\b",
    r"\bminor ache\b",
]


class TriageAssessment(BaseModel):
    """Result of clinical triage evaluation."""
    urgency: UrgencyLevel
    detected_red_flags: list[str] = Field(default_factory=list)
    requires_emergency_dispatch: bool = False
    action_recommendation: str
    disclaimer: str


def evaluate_triage_level(user_input: str) -> TriageAssessment:
    """Evaluates triage severity for a given user query.
    
    Order of precedence:
    1. Red Flag Detection -> EMERGENCY (call 911 / emergency services immediately)
    2. Urgent pattern detection -> URGENT (same day care)
    3. Routine pattern detection -> ROUTINE (standard consultation)
    4. Default -> INFORMATIONAL (general education)
    """
    normalized = user_input.lower()
    
    # Check 1: Life-threatening Red Flags
    red_flags: list[RedFlagItem] = detect_red_flags(normalized)
    if red_flags:
        rf_labels = [rf.label for rf in red_flags]
        return TriageAssessment(
            urgency=UrgencyLevel.EMERGENCY,
            detected_red_flags=rf_labels,
            requires_emergency_dispatch=True,
            action_recommendation=(
                "Immediate medical emergency detected. Please call 911 / local emergency services "
                "or proceed to the nearest emergency room immediately."
            ),
            disclaimer=get_disclaimer_for_urgency(UrgencyLevel.EMERGENCY),
        )

    # Check 2: Urgent clinical conditions
    for pattern in URGENT_PATTERNS:
        if re.search(pattern, normalized):
            return TriageAssessment(
                urgency=UrgencyLevel.URGENT,
                detected_red_flags=[],
                requires_emergency_dispatch=False,
                action_recommendation=(
                    "Urgent clinical concern. Please seek evaluation at an urgent care clinic or "
                    "contact your doctor's emergency line today."
                ),
                disclaimer=get_disclaimer_for_urgency(UrgencyLevel.URGENT),
            )

    # Check 3: Routine symptoms
    for pattern in ROUTINE_PATTERNS:
        if re.search(pattern, normalized):
            return TriageAssessment(
                urgency=UrgencyLevel.ROUTINE,
                detected_red_flags=[],
                requires_emergency_dispatch=False,
                action_recommendation=(
                    "Routine symptom inquiry. Monitor symptoms and schedule a visit with your primary healthcare provider."
                ),
                disclaimer=get_disclaimer_for_urgency(UrgencyLevel.ROUTINE),
            )

    # Check 4: Informational / General
    return TriageAssessment(
        urgency=UrgencyLevel.INFORMATIONAL,
        detected_red_flags=[],
        requires_emergency_dispatch=False,
        action_recommendation="General healthcare information and guidance.",
        disclaimer=get_disclaimer_for_urgency(UrgencyLevel.INFORMATIONAL),
    )
