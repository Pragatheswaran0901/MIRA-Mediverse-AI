"""MIRA Character Attention & Head Orientation Controller.

Governs cranial posture, subtle healthcare attentiveness, and natural biological rhythms:
- subtle head orientation toward canonical targets (USER, SCREEN, LEFT, RIGHT, UP, DOWN, CENTER)
- calm clinical respiratory rhythm (subtle thoracic elevation, 12-16 cycles/min)
- empathetic bedside listening nods (subtle, occasional, non-repetitive)
- gentle posture shifts (attentive forward inclination during patient speech)
"""

import math
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field


class AttentionTarget(str, Enum):
    """Canonical spatial attention targets for MIRA's head orientation."""
    USER = "USER"          # Centered attentive bedside orientation towards patient
    SCREEN = "SCREEN"      # Subtly oriented towards vitals/charts (-8.0 deg yaw, -3.0 deg pitch)
    LEFT = "LEFT"          # Natural turn to left (-14.0 deg yaw, 0 deg pitch)
    RIGHT = "RIGHT"        # Natural turn to right (+14.0 deg yaw, 0 deg pitch)
    UP = "UP"              # Upward cognitive contemplation (0 deg yaw, +6.0 deg pitch)
    DOWN = "DOWN"          # Downward clinical review (0 deg yaw, -6.0 deg pitch)
    CENTER = "CENTER"      # Upright neutral position (0, 0, 0)


TARGET_HEAD_COORDINATES: dict[AttentionTarget, tuple[float, float, float]] = {
    # (yaw_deg, pitch_deg, roll_deg)
    AttentionTarget.USER: (0.0, 0.0, 0.0),
    AttentionTarget.SCREEN: (-6.0, -2.5, 0.0),
    AttentionTarget.LEFT: (-10.0, 0.0, -1.0),
    AttentionTarget.RIGHT: (10.0, 0.0, 1.0),
    AttentionTarget.UP: (0.0, 5.0, 0.5),
    AttentionTarget.DOWN: (0.0, -5.0, 0.0),
    AttentionTarget.CENTER: (0.0, 0.0, 0.0),
}


class AttentionState(BaseModel):
    """Snapshot of active head orientation and respiratory rhythm."""
    model_config = ConfigDict(frozen=True)

    target: AttentionTarget = AttentionTarget.USER
    head_pitch_deg: float = Field(default=0.0, ge=-20.0, le=20.0)  # Down (-), Up (+)
    head_yaw_deg: float = Field(default=0.0, ge=-30.0, le=30.0)    # Left (-), Right (+)
    head_roll_deg: float = Field(default=0.0, ge=-15.0, le=15.0)   # Lateral tilt
    posture_lean: float = Field(default=0.0, ge=-1.0, le=1.0)      # Forward lean ratio
    breathing_offset_y: float = Field(default=0.0, ge=-0.02, le=0.02)
    breathing_scale: float = Field(default=1.0, ge=0.98, le=1.02)
    is_nodding: bool = False


class MiraAttentionController:
    """Manages head orientation, natural breathing cycle, and attentive bedside nods."""

    def __init__(
        self,
        breathing_rate_cpm: float = 14.0,
    ) -> None:
        self._target: AttentionTarget = AttentionTarget.USER
        self._current_yaw: float = 0.0
        self._current_pitch: float = 0.0
        self._current_roll: float = 0.0
        self._target_yaw: float = 0.0
        self._target_pitch: float = 0.0
        self._target_roll: float = 0.0

        # Posture lean (e.g. slight forward lean when listening)
        self._posture_lean: float = 0.0
        self._target_posture_lean: float = 0.0

        # Clinical respiratory cycle (14 CPM = 0.233 Hz)
        self._breathing_rate_cpm: float = breathing_rate_cpm
        self._breathing_phase: float = 0.0

        # Listening nod dynamics (occasional, subtle single/double nod)
        self._is_nodding: bool = False
        self._nod_elapsed_sec: float = 0.0
        self._nod_duration_sec: float = 1.1
        self._nod_amplitude_deg: float = 2.2
        self._nod_offset_pitch: float = 0.0

    @property
    def current_target(self) -> AttentionTarget:
        """Active spatial attention target."""
        return self._target

    @property
    def is_nodding(self) -> bool:
        """True if an attentive nod gesture is currently animating."""
        return self._is_nodding

    def set_breathing_rate(self, cpm: float) -> None:
        """Adjusts breathing rate (cycles per minute)."""
        self._breathing_rate_cpm = max(6.0, min(30.0, cpm))

    def set_target(self, target: AttentionTarget | str) -> None:
        """Orients head toward target."""
        if isinstance(target, str):
            try:
                target = AttentionTarget(target.upper())
            except ValueError:
                target = AttentionTarget.USER
        self._target = target
        yaw, pitch, roll = TARGET_HEAD_COORDINATES.get(target, (0.0, 0.0, 0.0))
        self._target_yaw = yaw
        self._target_pitch = pitch
        self._target_roll = roll

    def orient_to_user(self) -> None:
        """Directs head straight toward patient."""
        self.set_target(AttentionTarget.USER)

    def orient_to_screen(self) -> None:
        """Subtly angles head toward medical telemetry or charting display."""
        self.set_target(AttentionTarget.SCREEN)

    def set_posture_lean(self, lean: float) -> None:
        """Sets forward attentiveness lean (-1.0 to 1.0)."""
        self._target_posture_lean = max(-0.5, min(1.0, lean))

    def set_head_tilt(self, roll_deg: float) -> None:
        """Sets subtle compassionate head tilt (roll)."""
        self._target_roll = max(-6.0, min(6.0, roll_deg))

    def trigger_listening_nod(self) -> None:
        """Executes a single natural, gentle bedside acknowledgment nod."""
        if not self._is_nodding:
            self._is_nodding = True
            self._nod_elapsed_sec = 0.0
            self._nod_offset_pitch = 0.0

    def update(self, delta_time_sec: float) -> AttentionState:
        """Advances head orientation, breathing, and nodding over delta time."""
        # 1. Update Respiratory Cycle (very subtle clinical breathing rhythm)
        # Frequency = CPM / 60 Hz
        freq_hz = self._breathing_rate_cpm / 60.0
        self._breathing_phase += delta_time_sec * freq_hz * 2.0 * math.pi
        if self._breathing_phase > 2.0 * math.pi:
            self._breathing_phase -= 2.0 * math.pi

        # Very subtle amplitude: vertical chest rise ~0.006 (0.6%), scale 1.002
        breathe_sin = math.sin(self._breathing_phase)
        breathing_offset_y = breathe_sin * 0.005
        breathing_scale = 1.0 + (breathe_sin * 0.002)

        # 2. Update Listening Nod
        if self._is_nodding:
            self._nod_elapsed_sec += delta_time_sec
            progress = self._nod_elapsed_sec / self._nod_duration_sec
            if progress >= 1.0:
                self._is_nodding = False
                self._nod_offset_pitch = 0.0
            else:
                # Gentle bell-shaped dip in pitch: -sin(progress * pi) * amplitude
                self._nod_offset_pitch = -math.sin(progress * math.pi) * self._nod_amplitude_deg
        else:
            self._nod_offset_pitch = 0.0

        # 3. Smooth Damping to Target Orientation
        head_speed = 3.5 * delta_time_sec  # Gentle, deliberate human head motion
        self._current_yaw += (self._target_yaw - self._current_yaw) * min(1.0, head_speed)
        self._current_pitch += (self._target_pitch - self._current_pitch) * min(1.0, head_speed)
        self._current_roll += (self._target_roll - self._current_roll) * min(1.0, head_speed)
        self._posture_lean += (self._target_posture_lean - self._posture_lean) * min(1.0, head_speed)

        total_pitch = self._current_pitch + self._nod_offset_pitch

        return AttentionState(
            target=self._target,
            head_pitch_deg=round(total_pitch, 2),
            head_yaw_deg=round(self._current_yaw, 2),
            head_roll_deg=round(self._current_roll, 2),
            posture_lean=round(self._posture_lean, 3),
            breathing_offset_y=round(breathing_offset_y, 4),
            breathing_scale=round(breathing_scale, 4),
            is_nodding=self._is_nodding,
        )

    def reset(self) -> None:
        """Resets head orientation and posture to neutral user baseline."""
        self.set_target(AttentionTarget.USER)
        self._current_yaw = 0.0
        self._current_pitch = 0.0
        self._current_roll = 0.0
        self._target_yaw = 0.0
        self._target_pitch = 0.0
        self._target_roll = 0.0
        self._posture_lean = 0.0
        self._target_posture_lean = 0.0
        self._is_nodding = False
        self._nod_offset_pitch = 0.0
