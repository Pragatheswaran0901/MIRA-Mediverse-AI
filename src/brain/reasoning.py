"""MIRA Clinical Reasoning Engine Abstraction.

Defines protocols for multi-step clinical reasoning, symptom decomposition,
and contextual response synthesis.
"""

from typing import Protocol, runtime_checkable
from pydantic import BaseModel, Field
from src.core.contracts import UrgencyLevel, MiraResponse
from src.core.context import MiraInteractionContext


class ClinicalReasoningPlan(BaseModel):
    """Structured clinical decomposition before generating patient response."""
    primary_symptoms: list[str] = Field(default_factory=list)
    differential_possibilities: list[str] = Field(default_factory=list)
    red_flag_checked: bool = True
    assessed_urgency: UrgencyLevel = UrgencyLevel.INFORMATIONAL
    requires_triage_escalation: bool = False
    suggested_questions: list[str] = Field(default_factory=list)


@runtime_checkable
class ClinicalReasoningEngine(Protocol):
    """Protocol for MIRA's reasoning core."""
    async def reason(self, context: MiraInteractionContext, user_text: str) -> ClinicalReasoningPlan:
        """Deconstructs user input into clinical reasoning plan."""
        ...

    async def generate_response(
        self,
        context: MiraInteractionContext,
        user_text: str,
        plan: ClinicalReasoningPlan,
    ) -> MiraResponse:
        """Synthesizes structured response adhering to personality and safety constraints."""
        ...
