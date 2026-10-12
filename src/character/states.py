"""MIRA Character Visual State System.

Defines the 13 canonical, data-driven character states for MIRA avatar rendering.
Provides state metadata, clinical intent mappings, and animation readiness hooks.
"""

from enum import Enum
from typing import Any
from pydantic import BaseModel, ConfigDict, Field
from src.core.contracts import UrgencyLevel


class MiraVisualState(str, Enum):
    """Canonical character visual states for MIRA."""
    IDLE = "IDLE"              # Baseline calm readiness, observing bedside
    GREETING = "GREETING"      # Welcoming reception, warm introduction
    LISTENING = "LISTENING"    # Active clinical attentiveness, capturing patient speech
    THINKING = "THINKING"      # Clinical evaluation, guideline cross-referencing
    SPEAKING = "SPEAKING"      # Active delivery of guidance or advice
    FRIENDLY = "FRIENDLY"      # Warm companionship, rapport building
    CONCERNED = "CONCERNED"    # Heightened clinical focus, probing symptom onset
    SERIOUS = "SERIOUS"        # Urgent medical posture, firm instruction
    REASSURING = "REASSURING"  # Empathetic comfort, soothing patient distress
    EMERGENCY = "EMERGENCY"    # Acute red-flag posture, immediate critical directive
    ESCALATING = "ESCALATING"  # Severity transition in progress, protocol elevating
    CALMING = "CALMING"        # Deliberate breathing pacing, anxiety de-escalation
    COMPLETED = "COMPLETED"    # Interaction conclusion, pleasant resolution


class MiraStateDefinition(BaseModel):
    """Data-driven specification for an individual MIRA character state."""
    model_config = ConfigDict(frozen=True)

    state: MiraVisualState
    display_name: str
    description: str
    clinical_intent: str
    accent_color: str
    ui_halo_mode: str
    urgency_alignment: UrgencyLevel
    animation_hints: dict[str, Any] = Field(default_factory=dict)
    layer_hooks: dict[str, Any] = Field(default_factory=dict)


# Exhaustive data-driven registry of all 13 states
CHARACTER_STATE_REGISTRY: dict[MiraVisualState, MiraStateDefinition] = {
    MiraVisualState.IDLE: MiraStateDefinition(
        state=MiraVisualState.IDLE,
        display_name="Bedside Idle",
        description="Neutral clinical presence, attentive baseline posture.",
        clinical_intent="Available and ready to assist patient without intrusion.",
        accent_color="#0D9488",  # Clinical teal
        ui_halo_mode="subtle_teal",
        urgency_alignment=UrgencyLevel.INFORMATIONAL,
        animation_hints={
            "breathing_rate_cpm": 14,
            "blink_interval_sec": 3.8,
            "head_tilt_deg": 0.0,
            "eye_contact_ratio": 0.85,
        },
        layer_hooks={"expression_key": "baseline_calm", "posture_key": "neutral_upright"},
    ),
    MiraVisualState.GREETING: MiraStateDefinition(
        state=MiraVisualState.GREETING,
        display_name="Warm Greeting",
        description="Welcoming smile, slight head bow of reception.",
        clinical_intent="Establish immediate trust and compassionate bedside rapport.",
        accent_color="#F472B6",  # Gentle rose pink
        ui_halo_mode="warm_pink",
        urgency_alignment=UrgencyLevel.INFORMATIONAL,
        animation_hints={
            "breathing_rate_cpm": 15,
            "blink_interval_sec": 3.2,
            "head_tilt_deg": 1.5,
            "eye_contact_ratio": 0.95,
        },
        layer_hooks={"expression_key": "warm_smile", "posture_key": "welcoming_incline"},
    ),
    MiraVisualState.LISTENING: MiraStateDefinition(
        state=MiraVisualState.LISTENING,
        display_name="Active Listening",
        description="Slight forward attention, focused gaze, receptive posture.",
        clinical_intent="Attentively capturing patient symptoms and history.",
        accent_color="#3B82F6",  # Attentive blue
        ui_halo_mode="listening_blue",
        urgency_alignment=UrgencyLevel.ROUTINE,
        animation_hints={
            "breathing_rate_cpm": 13,
            "blink_interval_sec": 4.0,
            "head_tilt_deg": 2.0,
            "eye_contact_ratio": 0.98,
        },
        layer_hooks={"expression_key": "focused_receptive", "posture_key": "forward_listen"},
    ),
    MiraVisualState.THINKING: MiraStateDefinition(
        state=MiraVisualState.THINKING,
        display_name="Clinical Reasoning",
        description="Subtle gaze contemplation, synthesizing clinical knowledge.",
        clinical_intent="Synthesizing triage criteria and protocol verification.",
        accent_color="#8B5CF6",  # Thoughtful purple
        ui_halo_mode="deliberate_purple",
        urgency_alignment=UrgencyLevel.ROUTINE,
        animation_hints={
            "breathing_rate_cpm": 12,
            "blink_interval_sec": 4.5,
            "head_tilt_deg": -1.0,
            "eye_contact_ratio": 0.70,
        },
        layer_hooks={"expression_key": "contemplative_focus", "posture_key": "neutral_centered"},
    ),
    MiraVisualState.SPEAKING: MiraStateDefinition(
        state=MiraVisualState.SPEAKING,
        display_name="Clinical Delivery",
        description="Articulate presence, steady eye contact, active communication.",
        clinical_intent="Delivering clear, accessible medical advice and next steps.",
        accent_color="#0EA5E9",  # Communication cyan
        ui_halo_mode="speaking_cyan",
        urgency_alignment=UrgencyLevel.ROUTINE,
        animation_hints={
            "breathing_rate_cpm": 16,
            "blink_interval_sec": 3.0,
            "head_tilt_deg": 0.5,
            "eye_contact_ratio": 0.92,
        },
        layer_hooks={"expression_key": "articulate_open", "posture_key": "communicative"},
    ),
    MiraVisualState.FRIENDLY: MiraStateDefinition(
        state=MiraVisualState.FRIENDLY,
        display_name="Companion Friendly",
        description="Gentle warmth, approachable demeanor, comforting presence.",
        clinical_intent="Alleviating feelings of loneliness and healthcare anxiety.",
        accent_color="#EC4899",  # Caring pink
        ui_halo_mode="caring_glow",
        urgency_alignment=UrgencyLevel.INFORMATIONAL,
        animation_hints={
            "breathing_rate_cpm": 14,
            "blink_interval_sec": 3.5,
            "head_tilt_deg": 2.0,
            "eye_contact_ratio": 0.90,
        },
        layer_hooks={"expression_key": "empathetic_smile", "posture_key": "gentle_incline"},
    ),
    MiraVisualState.CONCERNED: MiraStateDefinition(
        state=MiraVisualState.CONCERNED,
        display_name="Clinical Concern",
        description="Slightly softened brow, heightened focus, empathetic vigilance.",
        clinical_intent="Investigating concerning symptoms requiring close scrutiny.",
        accent_color="#F59E0B",  # Warning amber
        ui_halo_mode="vigilant_amber",
        urgency_alignment=UrgencyLevel.URGENT,
        animation_hints={
            "breathing_rate_cpm": 16,
            "blink_interval_sec": 3.0,
            "head_tilt_deg": 1.0,
            "eye_contact_ratio": 0.96,
        },
        layer_hooks={"expression_key": "clinical_concern", "posture_key": "attentive_lean"},
    ),
    MiraVisualState.SERIOUS: MiraStateDefinition(
        state=MiraVisualState.SERIOUS,
        display_name="Firm Clinical Directive",
        description="Direct upright posture, focused unblinking alert gaze.",
        clinical_intent="Delivering urgent, non-negotiable healthcare guidance.",
        accent_color="#EA580C",  # Alert orange
        ui_halo_mode="alert_orange",
        urgency_alignment=UrgencyLevel.URGENT,
        animation_hints={
            "breathing_rate_cpm": 18,
            "blink_interval_sec": 4.8,
            "head_tilt_deg": 0.0,
            "eye_contact_ratio": 0.99,
        },
        layer_hooks={"expression_key": "serious_firm", "posture_key": "authoritative_upright"},
    ),
    MiraVisualState.REASSURING: MiraStateDefinition(
        state=MiraVisualState.REASSURING,
        display_name="Reassurance & Comfort",
        description="Warm supportive posture, gentle affirming demeanor.",
        clinical_intent="De-escalating patient panic after initial triage evaluation.",
        accent_color="#E2C799",  # Sandal accent
        ui_halo_mode="reassuring_sandal",
        urgency_alignment=UrgencyLevel.ROUTINE,
        animation_hints={
            "breathing_rate_cpm": 12,
            "blink_interval_sec": 3.4,
            "head_tilt_deg": 1.5,
            "eye_contact_ratio": 0.92,
        },
        layer_hooks={"expression_key": "comforting_nod", "posture_key": "supportive_calm"},
    ),
    MiraVisualState.EMERGENCY: MiraStateDefinition(
        state=MiraVisualState.EMERGENCY,
        display_name="Emergency Escalation",
        description="Acute crisis posture, high alert presence, urgent directing.",
        clinical_intent="Life safety priority: direct patient to 911 / emergency services.",
        accent_color="#DC2626",  # Emergency red
        ui_halo_mode="crisis_red_pulse",
        urgency_alignment=UrgencyLevel.EMERGENCY,
        animation_hints={
            "breathing_rate_cpm": 20,
            "blink_interval_sec": 5.0,
            "head_tilt_deg": 0.0,
            "eye_contact_ratio": 1.0,
        },
        layer_hooks={"expression_key": "acute_emergency", "posture_key": "urgent_command"},
    ),
    MiraVisualState.ESCALATING: MiraStateDefinition(
        state=MiraVisualState.ESCALATING,
        display_name="Triage Escalating",
        description="Heightening alertness, shifting from routine to urgent posture.",
        clinical_intent="Transitioning patient into elevated clinical triage queue.",
        accent_color="#D97706",  # Escalation amber
        ui_halo_mode="escalation_amber",
        urgency_alignment=UrgencyLevel.URGENT,
        animation_hints={
            "breathing_rate_cpm": 17,
            "blink_interval_sec": 3.2,
            "head_tilt_deg": 0.5,
            "eye_contact_ratio": 0.97,
        },
        layer_hooks={"expression_key": "escalating_alert", "posture_key": "vigilant_shift"},
    ),
    MiraVisualState.CALMING: MiraStateDefinition(
        state=MiraVisualState.CALMING,
        display_name="Paced Calming",
        description="Deliberate slow rhythmic presence, guiding breathing.",
        clinical_intent="Assisting patient through anxiety attack or hyperventilation.",
        accent_color="#14B8A6",  # Gentle turquoise
        ui_halo_mode="calm_teal_breathe",
        urgency_alignment=UrgencyLevel.ROUTINE,
        animation_hints={
            "breathing_rate_cpm": 8,
            "blink_interval_sec": 4.2,
            "head_tilt_deg": 1.0,
            "eye_contact_ratio": 0.88,
        },
        layer_hooks={"expression_key": "soothing_guidance", "posture_key": "paced_breathe"},
    ),
    MiraVisualState.COMPLETED: MiraStateDefinition(
        state=MiraVisualState.COMPLETED,
        display_name="Session Completed",
        description="Satisfied closure, courteous parting, reassuring affirmation.",
        clinical_intent="Confirm patient well-being at the end of consultation.",
        accent_color="#10B981",  # Recovery emerald
        ui_halo_mode="completed_green",
        urgency_alignment=UrgencyLevel.INFORMATIONAL,
        animation_hints={
            "breathing_rate_cpm": 14,
            "blink_interval_sec": 3.6,
            "head_tilt_deg": 1.0,
            "eye_contact_ratio": 0.90,
        },
        layer_hooks={"expression_key": "courteous_farewell", "posture_key": "resting_calm"},
    ),
}


def get_state_definition(state: MiraVisualState | str) -> MiraStateDefinition:
    """Retrieves definition for given state or defaults to IDLE."""
    if isinstance(state, str):
        try:
            state = MiraVisualState(state.upper())
        except ValueError:
            return CHARACTER_STATE_REGISTRY[MiraVisualState.IDLE]
    return CHARACTER_STATE_REGISTRY.get(state, CHARACTER_STATE_REGISTRY[MiraVisualState.IDLE])


def get_all_states() -> list[MiraStateDefinition]:
    """Returns list of all 13 canonical state definitions."""
    return list(CHARACTER_STATE_REGISTRY.values())
