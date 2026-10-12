"""MIRA Character Future Animation Compatibility Architecture.

Defines the formal contracts, hooks, and parameter interfaces for:
- blinking
- eye movement
- eye direction
- subtle breathing
- head movement
- facial expressions
- mouth movement
- lip synchronization
- speaking animation
- listening animation
- emotional reactions
- interruption
- attention direction

NOTE: Per Block 2 requirements, these systems are architecturally prepared
and structured, but their execution remains dormant until future animation blocks.
"""

from pydantic import BaseModel, ConfigDict, Field


class BlinkingHookContract(BaseModel):
    """Readiness interface for natural eyelid blinking cycles."""
    model_config = ConfigDict(frozen=True)

    enabled: bool = False
    average_rate_hz: float = Field(default=0.28, ge=0.05, le=1.0)
    blink_duration_ms: int = Field(default=160, ge=80, le=400)
    micro_squint_factor: float = Field(default=0.0, ge=0.0, le=1.0)


class EyeMovementHookContract(BaseModel):
    """Readiness interface for natural saccadic eye drift and focus."""
    model_config = ConfigDict(frozen=True)

    enabled: bool = False
    saccade_frequency_hz: float = Field(default=0.4, ge=0.1, le=2.0)
    gaze_jitter_amplitude: float = Field(default=0.02, ge=0.0, le=0.1)
    pupil_dilation_factor: float = Field(default=1.0, ge=0.5, le=1.5)


class EyeDirectionHookContract(BaseModel):
    """Readiness interface for directed gaze orientation."""
    model_config = ConfigDict(frozen=True)

    enabled: bool = False
    target_pitch_deg: float = Field(default=0.0, ge=-30.0, le=30.0)
    target_yaw_deg: float = Field(default=0.0, ge=-45.0, le=45.0)
    eye_contact_weight: float = Field(default=0.9, ge=0.0, le=1.0)


class SubtleBreathingHookContract(BaseModel):
    """Readiness interface for natural, calming clinical respiratory rhythm."""
    model_config = ConfigDict(frozen=True)

    enabled: bool = False
    respiration_rate_cpm: float = Field(default=14.0, ge=6.0, le=30.0)
    chest_rise_scale: float = Field(default=0.012, ge=0.0, le=0.05)
    shoulder_settle_scale: float = Field(default=0.006, ge=0.0, le=0.03)


class HeadMovementHookContract(BaseModel):
    """Readiness interface for natural bedside head nod and orientation."""
    model_config = ConfigDict(frozen=True)

    enabled: bool = False
    tilt_roll_deg: float = Field(default=0.0, ge=-15.0, le=15.0)
    pitch_nod_deg: float = Field(default=0.0, ge=-20.0, le=20.0)
    yaw_turn_deg: float = Field(default=0.0, ge=-30.0, le=30.0)
    listening_nod_count: int = Field(default=0, ge=0, le=5)


class FacialExpressionsHookContract(BaseModel):
    """Readiness interface for multi-target facial morph weighting."""
    model_config = ConfigDict(frozen=True)

    enabled: bool = False
    expression_id: str = "calm_baseline"
    intensity: float = Field(default=1.0, ge=0.0, le=1.0)
    brow_inner_up: float = Field(default=0.0, ge=0.0, le=1.0)
    brow_down_concern: float = Field(default=0.0, ge=0.0, le=1.0)
    smile_warmth: float = Field(default=0.15, ge=0.0, le=1.0)


class MouthMovementHookContract(BaseModel):
    """Readiness interface for non-speech mouth motion (smile, breathe open)."""
    model_config = ConfigDict(frozen=True)

    enabled: bool = False
    jaw_open_ratio: float = Field(default=0.0, ge=0.0, le=1.0)
    lip_corner_pull: float = Field(default=0.0, ge=-1.0, le=1.0)
    lip_pucker: float = Field(default=0.0, ge=0.0, le=1.0)


class LipSyncHookContract(BaseModel):
    """Readiness interface for speech audio viseme lip synchronization."""
    model_config = ConfigDict(frozen=True)

    enabled: bool = False
    current_viseme: str = "silence"
    viseme_blend_weight: float = Field(default=0.0, ge=0.0, le=1.0)
    phoneme_timestamp_ms: int = Field(default=0, ge=0)


class SpeakingAnimationHookContract(BaseModel):
    """Readiness interface for active speaking gestures and head cadence."""
    model_config = ConfigDict(frozen=True)

    enabled: bool = False
    is_speaking: bool = False
    speech_cadence_wpm: int = Field(default=150, ge=80, le=260)
    vocal_energy_rms: float = Field(default=0.0, ge=0.0, le=1.0)


class ListeningAnimationHookContract(BaseModel):
    """Readiness interface for active patient listening behavior."""
    model_config = ConfigDict(frozen=True)

    enabled: bool = False
    is_listening: bool = False
    attentiveness_score: float = Field(default=1.0, ge=0.0, le=1.0)
    subtle_acknowledgment_pending: bool = False


class EmotionalReactionHookContract(BaseModel):
    """Readiness interface for clinical empathy and emotional modulation."""
    model_config = ConfigDict(frozen=True)

    enabled: bool = False
    valence: float = Field(default=0.2, ge=-1.0, le=1.0)
    arousal: float = Field(default=0.0, ge=-1.0, le=1.0)
    dominance: float = Field(default=0.3, ge=-1.0, le=1.0)
    empathy_score: float = Field(default=0.9, ge=0.0, le=1.0)


class InterruptionHookContract(BaseModel):
    """Readiness interface for instant patient barge-in and conversational halt."""
    model_config = ConfigDict(frozen=True)

    enabled: bool = False
    barge_in_detected: bool = False
    halt_latency_ms: int = Field(default=80, ge=0, le=500)
    snap_to_listening: bool = True


class AttentionDirectionHookContract(BaseModel):
    """Readiness interface for guiding MIRA's attention to charts or patient."""
    model_config = ConfigDict(frozen=True)

    enabled: bool = False
    poi_label: str = "patient_face"
    head_weight: float = Field(default=0.4, ge=0.0, le=1.0)
    eye_weight: float = Field(default=0.9, ge=0.0, le=1.0)


class MiraAnimationCapabilityArchitecture(BaseModel):
    """Central container registering all 13 future animation capability contracts.
    
    All contracts default to enabled=False in Block 2.
    """
    model_config = ConfigDict(frozen=True)

    architecture_version: str = "MIRA_ANIMATION_HOOKS_v1"
    is_dormant_in_block_2: bool = True

    blinking: BlinkingHookContract = Field(default_factory=BlinkingHookContract)
    eye_movement: EyeMovementHookContract = Field(default_factory=EyeMovementHookContract)
    eye_direction: EyeDirectionHookContract = Field(default_factory=EyeDirectionHookContract)
    subtle_breathing: SubtleBreathingHookContract = Field(
        default_factory=SubtleBreathingHookContract
    )
    head_movement: HeadMovementHookContract = Field(default_factory=HeadMovementHookContract)
    facial_expressions: FacialExpressionsHookContract = Field(
        default_factory=FacialExpressionsHookContract
    )
    mouth_movement: MouthMovementHookContract = Field(default_factory=MouthMovementHookContract)
    lip_sync: LipSyncHookContract = Field(default_factory=LipSyncHookContract)
    speaking_animation: SpeakingAnimationHookContract = Field(
        default_factory=SpeakingAnimationHookContract
    )
    listening_animation: ListeningAnimationHookContract = Field(
        default_factory=ListeningAnimationHookContract
    )
    emotional_reactions: EmotionalReactionHookContract = Field(
        default_factory=EmotionalReactionHookContract
    )
    interruption: InterruptionHookContract = Field(default_factory=InterruptionHookContract)
    attention_direction: AttentionDirectionHookContract = Field(
        default_factory=AttentionDirectionHookContract
    )


# Singleton container for future animation readiness
ANIMATION_CAPABILITY_ARCHITECTURE = MiraAnimationCapabilityArchitecture()
