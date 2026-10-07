"""MIRA Product Specification & Blueprint Info Route."""

from fastapi import APIRouter
from pydantic import BaseModel
from config.settings import get_settings
from src.core.contracts import PRODUCT_IDENTITY, ProductIdentity
from src.brain.personality import PERSONALITY_TRAITS

router = APIRouter(prefix="/api/v1", tags=["Product Information"])


class ArchitectureTierInfo(BaseModel):
    """Description of an architectural tier."""
    name: str
    components: list[str]
    description: str


class MiraInfoResponse(BaseModel):
    """Complete product and architectural info response."""
    identity: ProductIdentity
    canonical_introduction: str
    personality_traits: dict[str, str]
    current_block: str
    architecture: list[ArchitectureTierInfo]
    external_integration_policy: str


@router.get("/info", response_model=MiraInfoResponse)
async def get_mira_info() -> MiraInfoResponse:
    """Returns canonical product specifications, architecture, and persona traits."""
    settings = get_settings()
    return MiraInfoResponse(
        identity=PRODUCT_IDENTITY,
        canonical_introduction=PRODUCT_IDENTITY.get_canonical_introduction(),
        personality_traits={
            "companion_style": PERSONALITY_TRAITS.companion_style,
            "clinical_care": PERSONALITY_TRAITS.clinical_care,
            "intellect": PERSONALITY_TRAITS.intellect,
            "temperament": PERSONALITY_TRAITS.temperament,
            "normal_conversation": PERSONALITY_TRAITS.communication_normal,
            "urgent_communication": PERSONALITY_TRAITS.communication_urgent,
            "emergency_communication": PERSONALITY_TRAITS.communication_emergency,
            "non_judgmental": PERSONALITY_TRAITS.non_judgmental,
            "authentic_identity": PERSONALITY_TRAITS.authentic_identity,
        },
        current_block=settings.current_block,
        architecture=[
            ArchitectureTierInfo(
                name="Tier 1: Interaction Layer",
                components=["Brain (Reasoning, Memory, Context)", "Character (Animation, Expressions, Lip Sync)", "Voice (STT, TTS, Voice ID)"],
                description="User-facing perception, reasoning, emotional expression, and acoustic interaction.",
            ),
            ArchitectureTierInfo(
                name="Tier 2: MIRA Core",
                components=["Safety (Triage, Escalation, Red Flags)", "Tools (Healthcare Integrations, External APIs)", "Knowledge (RAG, Guidelines, Medical KB)"],
                description="Governs medical safety, evidence-based clinical reasoning, and tool execution.",
            ),
            ArchitectureTierInfo(
                name="Tier 3: MIRA API & External Ecosystem",
                components=["MIRA REST API", "WebSocket Streaming", "Decoupled External Adapters (e.g. MediVerse, Future Apps)"],
                description="Contract-driven gateway connecting external healthcare clients without internal dependencies.",
            ),
        ],
        external_integration_policy=(
            "MIRA is a completely standalone AI healthcare product. "
            "External platforms (such as MediVerse or other healthcare ecosystems) "
            "interact strictly as consumers via the decoupled MIRA API without introducing "
            "upstream code or API dependencies into MIRA core."
        ),
    )
