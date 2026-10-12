"""MIRA Character Facial Expression System.

Defines the future-ready facial expression abstraction with FACS-compatible morph target
weights, healthcare-calibrated subtleties, and smooth interpolation dynamics.
"""

from enum import Enum
from pydantic import BaseModel, ConfigDict, Field


class FacialExpressionId(str, Enum):
    """Canonical facial expressions for MIRA avatar."""
    NEUTRAL = "NEUTRAL"
    HAPPY = "HAPPY"
    CURIOUS = "CURIOUS"
    ATTENTIVE = "ATTENTIVE"
    THINKING = "THINKING"
    CONCERNED = "CONCERNED"
    SERIOUS = "SERIOUS"
    REASSURING = "REASSURING"
    CALM = "CALM"
    EMERGENCY = "EMERGENCY"


class ExpressionMorphWeights(BaseModel):
    """FACS-compatible blendshape parameter targets for realistic facial expressions.
    
    All weights are clamped to subtle, natural human ranges (0.0 to 1.0) appropriate
    for a professional healthcare clinician, strictly avoiding exaggerated cartoon caricatures.
    """
    model_config = ConfigDict(frozen=True)

    brow_inner_up: float = Field(default=0.0, ge=0.0, le=1.0)
    brow_down_concern: float = Field(default=0.0, ge=0.0, le=1.0)
    brow_outer_up: float = Field(default=0.0, ge=0.0, le=1.0)
    eye_squint: float = Field(default=0.0, ge=0.0, le=1.0)
    eye_wide: float = Field(default=0.0, ge=0.0, le=1.0)
    cheek_raise: float = Field(default=0.0, ge=0.0, le=1.0)
    mouth_smile_warmth: float = Field(default=0.0, ge=0.0, le=1.0)
    lip_corner_depress: float = Field(default=0.0, ge=0.0, le=1.0)
    lip_press: float = Field(default=0.0, ge=0.0, le=1.0)
    jaw_clench_firm: float = Field(default=0.0, ge=0.0, le=1.0)
    head_tilt_bias_deg: float = Field(default=0.0, ge=-5.0, le=5.0)


# Curated, professional, subtle healthcare expression configurations
CANONICAL_EXPRESSION_PRESETS: dict[FacialExpressionId, ExpressionMorphWeights] = {
    FacialExpressionId.NEUTRAL: ExpressionMorphWeights(
        brow_inner_up=0.05,
        brow_down_concern=0.0,
        brow_outer_up=0.0,
        eye_squint=0.05,
        eye_wide=0.0,
        cheek_raise=0.05,
        mouth_smile_warmth=0.1,  # Pleasant baseline bedside readiness
        lip_corner_depress=0.0,
        lip_press=0.0,
        jaw_clench_firm=0.0,
        head_tilt_bias_deg=0.0,
    ),
    FacialExpressionId.HAPPY: ExpressionMorphWeights(
        brow_inner_up=0.1,
        brow_down_concern=0.0,
        brow_outer_up=0.1,
        eye_squint=0.25,
        eye_wide=0.0,
        cheek_raise=0.35,
        mouth_smile_warmth=0.45,  # Warm empathetic smile, never exaggerated grin
        lip_corner_depress=0.0,
        lip_press=0.0,
        jaw_clench_firm=0.0,
        head_tilt_bias_deg=1.5,
    ),
    FacialExpressionId.CURIOUS: ExpressionMorphWeights(
        brow_inner_up=0.25,
        brow_down_concern=0.0,
        brow_outer_up=0.3,
        eye_squint=0.1,
        eye_wide=0.15,
        cheek_raise=0.1,
        mouth_smile_warmth=0.15,
        lip_corner_depress=0.0,
        lip_press=0.05,
        jaw_clench_firm=0.0,
        head_tilt_bias_deg=2.0,
    ),
    FacialExpressionId.ATTENTIVE: ExpressionMorphWeights(
        brow_inner_up=0.15,
        brow_down_concern=0.1,
        brow_outer_up=0.05,
        eye_squint=0.12,
        eye_wide=0.1,
        cheek_raise=0.1,
        mouth_smile_warmth=0.12,
        lip_corner_depress=0.0,
        lip_press=0.05,
        jaw_clench_firm=0.0,
        head_tilt_bias_deg=1.0,
    ),
    FacialExpressionId.THINKING: ExpressionMorphWeights(
        brow_inner_up=0.2,
        brow_down_concern=0.15,
        brow_outer_up=0.1,
        eye_squint=0.2,
        eye_wide=0.0,
        cheek_raise=0.05,
        mouth_smile_warmth=0.05,
        lip_corner_depress=0.0,
        lip_press=0.15,
        jaw_clench_firm=0.05,
        head_tilt_bias_deg=-1.5,
    ),
    FacialExpressionId.CONCERNED: ExpressionMorphWeights(
        brow_inner_up=0.45,
        brow_down_concern=0.35,
        brow_outer_up=0.0,
        eye_squint=0.18,
        eye_wide=0.15,
        cheek_raise=0.05,
        mouth_smile_warmth=0.0,
        lip_corner_depress=0.15,
        lip_press=0.2,
        jaw_clench_firm=0.1,
        head_tilt_bias_deg=1.0,
    ),
    FacialExpressionId.SERIOUS: ExpressionMorphWeights(
        brow_inner_up=0.1,
        brow_down_concern=0.4,
        brow_outer_up=0.0,
        eye_squint=0.1,
        eye_wide=0.25,
        cheek_raise=0.0,
        mouth_smile_warmth=0.0,
        lip_corner_depress=0.1,
        lip_press=0.3,
        jaw_clench_firm=0.25,
        head_tilt_bias_deg=0.0,
    ),
    FacialExpressionId.REASSURING: ExpressionMorphWeights(
        brow_inner_up=0.15,
        brow_down_concern=0.0,
        brow_outer_up=0.1,
        eye_squint=0.2,
        eye_wide=0.0,
        cheek_raise=0.25,
        mouth_smile_warmth=0.35,
        lip_corner_depress=0.0,
        lip_press=0.0,
        jaw_clench_firm=0.0,
        head_tilt_bias_deg=1.8,
    ),
    FacialExpressionId.CALM: ExpressionMorphWeights(
        brow_inner_up=0.05,
        brow_down_concern=0.0,
        brow_outer_up=0.0,
        eye_squint=0.08,
        eye_wide=0.0,
        cheek_raise=0.08,
        mouth_smile_warmth=0.18,
        lip_corner_depress=0.0,
        lip_press=0.0,
        jaw_clench_firm=0.0,
        head_tilt_bias_deg=0.5,
    ),
    FacialExpressionId.EMERGENCY: ExpressionMorphWeights(
        brow_inner_up=0.3,
        brow_down_concern=0.5,
        brow_outer_up=0.15,
        eye_squint=0.0,
        eye_wide=0.45,  # Wide attentive alertness
        cheek_raise=0.0,
        mouth_smile_warmth=0.0,
        lip_corner_depress=0.1,
        lip_press=0.35,
        jaw_clench_firm=0.3,
        head_tilt_bias_deg=0.0,
    ),
}


class MiraExpressionController:
    """Controls character facial expression morphing and smooth state interpolation."""

    def __init__(self, initial_expression: FacialExpressionId = FacialExpressionId.NEUTRAL) -> None:
        self._current_expression: FacialExpressionId = initial_expression
        self._target_expression: FacialExpressionId = initial_expression
        self._current_weights: ExpressionMorphWeights = CANONICAL_EXPRESSION_PRESETS[initial_expression]
        self._target_weights: ExpressionMorphWeights = CANONICAL_EXPRESSION_PRESETS[initial_expression]
        self._transition_duration_sec: float = 0.35
        self._transition_progress: float = 1.0

    @property
    def current_expression(self) -> FacialExpressionId:
        """Active facial expression identifier."""
        return self._current_expression

    @property
    def target_expression(self) -> FacialExpressionId:
        """Target expression undergoing transition."""
        return self._target_expression

    @property
    def current_weights(self) -> ExpressionMorphWeights:
        """Active FACS blendshape weights."""
        return self._current_weights

    def set_expression(
        self,
        expression: FacialExpressionId,
        transition_duration_sec: float = 0.35,
    ) -> None:
        """Transitions to the specified expression preset smoothly."""
        if expression not in CANONICAL_EXPRESSION_PRESETS:
            expression = FacialExpressionId.NEUTRAL

        if expression == self._target_expression and self._transition_progress >= 1.0:
            return

        self._target_expression = expression
        self._target_weights = CANONICAL_EXPRESSION_PRESETS[expression]
        self._transition_duration_sec = max(0.05, transition_duration_sec)
        self._transition_progress = 0.0

    def update(self, delta_time_sec: float) -> ExpressionMorphWeights:
        """Progresses expression interpolation over delta time."""
        if self._transition_progress >= 1.0:
            return self._current_weights

        self._transition_progress += delta_time_sec / self._transition_duration_sec
        if self._transition_progress >= 1.0:
            self._transition_progress = 1.0
            self._current_expression = self._target_expression
            self._current_weights = self._target_weights
            return self._current_weights

        # Smooth cubic ease-in-out interpolation: t^2 * (3 - 2t)
        t = self._transition_progress
        ease_t = t * t * (3.0 - 2.0 * t)

        w1 = self._current_weights
        w2 = self._target_weights

        def lerp(a: float, b: float) -> float:
            return a + (b - a) * ease_t

        interpolated = ExpressionMorphWeights(
            brow_inner_up=round(lerp(w1.brow_inner_up, w2.brow_inner_up), 4),
            brow_down_concern=round(lerp(w1.brow_down_concern, w2.brow_down_concern), 4),
            brow_outer_up=round(lerp(w1.brow_outer_up, w2.brow_outer_up), 4),
            eye_squint=round(lerp(w1.eye_squint, w2.eye_squint), 4),
            eye_wide=round(lerp(w1.eye_wide, w2.eye_wide), 4),
            cheek_raise=round(lerp(w1.cheek_raise, w2.cheek_raise), 4),
            mouth_smile_warmth=round(lerp(w1.mouth_smile_warmth, w2.mouth_smile_warmth), 4),
            lip_corner_depress=round(lerp(w1.lip_corner_depress, w2.lip_corner_depress), 4),
            lip_press=round(lerp(w1.lip_press, w2.lip_press), 4),
            jaw_clench_firm=round(lerp(w1.jaw_clench_firm, w2.jaw_clench_firm), 4),
            head_tilt_bias_deg=round(lerp(w1.head_tilt_bias_deg, w2.head_tilt_bias_deg), 2),
        )
        self._current_weights = interpolated
        return self._current_weights

    def reset(self) -> None:
        """Instantly resets to neutral baseline expression."""
        self._current_expression = FacialExpressionId.NEUTRAL
        self._target_expression = FacialExpressionId.NEUTRAL
        self._current_weights = CANONICAL_EXPRESSION_PRESETS[FacialExpressionId.NEUTRAL]
        self._target_weights = self._current_weights
        self._transition_progress = 1.0
