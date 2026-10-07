"""MIRA Character Emotional & Facial Expression Schemas.

Defines foundational expression states, mood transitions, and contextual reaction schemas.
"""

from enum import Enum
from pydantic import BaseModel, Field
from src.core.contracts import UrgencyLevel


class CharacterExpression(str, Enum):
    """Facial expression and posture states for MIRA avatar."""
    WARM = "warm"              # Friendly smile, attentive posture
    CALM = "calm"              # Neutral reassurance, steady eye contact
    EMPATHETIC = "empathetic"  # Gentle tilt, soft concern
    CONCERNED = "concerned"    # Serious brow, attentive focus
    SERIOUS = "serious"        # Firm, urgent posture, wide alert eyes
    LISTENING = "listening"    # Slight nod, responsive attention
    THINKING = "thinking"      # Brief gaze upward or focused contemplation


class CharacterReaction(BaseModel):
    """Event payload emitted to client character renderers."""
    expression: CharacterExpression = CharacterExpression.WARM
    intensity: float = Field(default=1.0, ge=0.0, le=1.0)
    transition_duration_ms: int = Field(default=300, ge=0)
    blink_rate_hz: float = Field(default=0.3, ge=0.0)


def map_urgency_to_expression(urgency: UrgencyLevel) -> CharacterExpression:
    """Maps conversational urgency level to MIRA's default facial expression."""
    if urgency == UrgencyLevel.EMERGENCY:
        return CharacterExpression.SERIOUS
    elif urgency == UrgencyLevel.URGENT:
        return CharacterExpression.CONCERNED
    elif urgency == UrgencyLevel.ROUTINE:
        return CharacterExpression.EMPATHETIC
    return CharacterExpression.WARM
