"""MIRA Interaction Context.

Maintains transient state during conversation turns, including detected urgency,
dialogue history, and clinical safety triggers.
"""

from datetime import datetime, timezone
from uuid import uuid4
from pydantic import BaseModel, Field
from src.core.contracts import MiraMessage, UrgencyLevel


class MiraInteractionContext(BaseModel):
    """Context state for a conversation session turn."""
    session_id: str = Field(default_factory=lambda: str(uuid4()))
    patient_id: str | None = None
    messages: list[MiraMessage] = Field(default_factory=list)
    current_urgency: UrgencyLevel = UrgencyLevel.INFORMATIONAL
    detected_red_flags: list[str] = Field(default_factory=list)
    escalated_to_emergency: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def add_message(self, message: MiraMessage) -> None:
        """Appends a message to the context history."""
        self.messages.append(message)

    def mark_emergency(self, red_flags: list[str]) -> None:
        """Escalates context to immediate emergency state."""
        self.current_urgency = UrgencyLevel.EMERGENCY
        self.escalated_to_emergency = True
        self.detected_red_flags.extend(red_flags)
