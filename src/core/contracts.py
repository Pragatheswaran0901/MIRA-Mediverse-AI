"""MIRA Core Data Contracts.

Defines foundational schemas, immutable product identity definitions,
urgency levels, and interaction primitives.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any
from pydantic import BaseModel, ConfigDict, Field


class UrgencyLevel(str, Enum):
    """Clinical triage urgency categorization."""
    EMERGENCY = "emergency"        # Life-threatening, immediate 911 / emergency services needed
    URGENT = "urgent"              # High concern, prompt clinical evaluation required (hours)
    ROUTINE = "routine"            # Standard care, general inquiry, scheduled appointments
    INFORMATIONAL = "informational" # General health wellness, preventative education


class MessageRole(str, Enum):
    """Dialogue actor role."""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class ProductIdentity(BaseModel):
    """MIRA Product Identity Contract.
    
    CRITICAL: is_human and replaces_professionals are strictly frozen to False.
    Any attempt to mutate these flags is prohibited.
    """
    model_config = ConfigDict(frozen=True)

    name: str = "MIRA"
    full_name: str = "Medical Intelligent Response Assistant"
    role: str = "AI Healthcare Companion / AI Nurse Assistant"
    is_human: bool = False
    replaces_professionals: bool = False
    companion_type: str = "Autonomous Healthcare AI"

    def get_canonical_introduction(self) -> str:
        """Returns the mandatory canonical introduction string."""
        return "I'm MIRA, an AI healthcare assistant."


# Singleton instance of ProductIdentity
PRODUCT_IDENTITY = ProductIdentity()


class MiraMessage(BaseModel):
    """Individual dialogue message contract."""
    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, Any] = Field(default_factory=dict)


class MiraResponseMetadata(BaseModel):
    """Metadata attached to every MIRA generation or triage decision."""
    urgency: UrgencyLevel = UrgencyLevel.INFORMATIONAL
    requires_emergency_services: bool = False
    disclaimer: str
    character_expression: str = "calm"
    tone: str = "warm"
    processing_time_ms: float = 0.0


class MiraResponse(BaseModel):
    """Structured response payload delivered to external clients."""
    reply: str
    identity: ProductIdentity = Field(default_factory=lambda: PRODUCT_IDENTITY)
    metadata: MiraResponseMetadata
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
