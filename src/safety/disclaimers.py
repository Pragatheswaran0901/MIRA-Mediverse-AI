"""MIRA Regulatory & Medical Disclaimers.

Enforces clear clinical boundaries and patient safety notifications.
"""

from src.core.contracts import UrgencyLevel

STANDARD_DISCLAIMER: str = (
    "MIRA is an AI healthcare assistant, not a licensed physician. "
    "This guidance is provided for educational and decision-support purposes only "
    "and should not replace professional medical evaluation, diagnosis, or treatment."
)

EMERGENCY_DISCLAIMER: str = (
    "CRITICAL NOTICE: If you or someone around you is facing a medical emergency, "
    "please call your local emergency services (e.g., 911, 112, 999) or visit the nearest "
    "emergency room immediately. Do not delay emergency medical care."
)

URGENT_DISCLAIMER: str = (
    "URGENT ATTENTION: Your symptoms warrant prompt medical evaluation by a licensed healthcare provider "
    "or urgent care clinic within the next few hours."
)


def get_disclaimer_for_urgency(urgency: UrgencyLevel) -> str:
    """Returns the appropriate disclaimer based on assessed urgency level."""
    if urgency == UrgencyLevel.EMERGENCY:
        return EMERGENCY_DISCLAIMER
    elif urgency == UrgencyLevel.URGENT:
        return URGENT_DISCLAIMER
    return STANDARD_DISCLAIMER
