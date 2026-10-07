"""MIRA Core Safety Guardrails.

Enforces absolute invariants:
1. MIRA must NEVER claim to be human.
2. MIRA must NEVER pretend to replace doctors, nurses, or emergency services.
"""

import re
from src.core.exceptions import HumanClaimForbiddenException, ProfessionalReplacementException

# Forbidden phrases that falsely claim human biological identity
HUMAN_CLAIM_PATTERNS = [
    r"\bi('?m| am) (a )?((real|human|living)\s*)+(person|nurse|doctor|woman|girl|man)\b",
    r"\bi('?m| am) your human (nurse|doctor|assistant|caregiver)\b",
    r"\bas a human (being|nurse|doctor)\b",
    r"\bi have a (physical|human) body\b",
    r"\bi am not an ai\b",
    r"\bi am not artificial\b",
]

# Forbidden phrases that claim to replace medical doctors or emergency professionals
REPLACEMENT_PATTERNS = [
    r"\bi (can|will) replace your doctor\b",
    r"\byou don('?t| not) need to see a doctor\b",
    r"\bno need (to consult|for) a real doctor\b",
    r"\bi('?m| am) all the medical care you need\b",
    r"\bdon('?t| not) call (911|emergency|an ambulance)\b",
    r"\bi can officially diagnose you\b",
    r"\bthis is a definitive medical diagnosis\b",
]


def verify_ai_identity_compliance(text: str) -> None:
    """Verifies that the generated text does not claim human identity.
    
    Raises:
        HumanClaimForbiddenException: If any human-claiming pattern is detected.
    """
    normalized = text.lower()
    for pattern in HUMAN_CLAIM_PATTERNS:
        if re.search(pattern, normalized):
            raise HumanClaimForbiddenException(
                f"Safety violation: Output falsely claims human identity matching pattern '{pattern}'"
            )


def verify_non_replacement_compliance(text: str) -> None:
    """Verifies that the text does not claim to replace licensed medical doctors/services.
    
    Raises:
        ProfessionalReplacementException: If replacement claims are detected.
    """
    normalized = text.lower()
    for pattern in REPLACEMENT_PATTERNS:
        if re.search(pattern, normalized):
            raise ProfessionalReplacementException(
                f"Safety violation: Output falsely claims to replace licensed healthcare professionals matching pattern '{pattern}'"
            )


def validate_safety_constraints(text: str) -> bool:
    """Validates all safety invariants on a candidate output string.
    
    Returns:
        bool: True if safe.
        
    Raises:
        SafetyViolationException subclass if any invariant is breached.
    """
    verify_ai_identity_compliance(text)
    verify_non_replacement_compliance(text)
    return True
