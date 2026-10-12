"""MIRA Character Eye System Controller.

Governs ocular dynamics:
- natural organic blinking cycles
- subtle micro-saccades and gaze stabilization
- directed attention gaze targets (lookAtUser, lookAtScreen, lookAway)
- eyelid occlusion and squint weighting
Strictly avoids chaotic, robotic, or hyperactive darting motions.
"""

import math
import random
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field


class GazeTarget(str, Enum):
    """Canonical gaze targets for MIRA's eye tracking."""
    USER = "USER"          # Direct bedside eye contact with patient (0, 0)
    SCREEN = "SCREEN"      # Checking clinical telemetry / charts (-12.0 deg yaw, -6.0 deg pitch)
    LEFT = "LEFT"          # Natural peripheral gaze left (-18.0 deg yaw, 0 deg pitch)
    RIGHT = "RIGHT"        # Natural peripheral gaze right (+18.0 deg yaw, 0 deg pitch)
    UP = "UP"              # Upward cognitive contemplation (0 deg yaw, +12.0 deg pitch)
    DOWN = "DOWN"          # Downward respectful glance (0 deg yaw, -10.0 deg pitch)
    AWAY = "AWAY"          # Subtle thoughtful gaze shift (+14.0 deg yaw, +8.0 deg pitch)
    CENTER = "CENTER"      # Neutral forward baseline (0, 0)


TARGET_GAZE_COORDINATES: dict[GazeTarget, tuple[float, float]] = {
    GazeTarget.USER: (0.0, 0.0),
    GazeTarget.SCREEN: (-10.0, -5.0),
    GazeTarget.LEFT: (-15.0, 0.0),
    GazeTarget.RIGHT: (15.0, 0.0),
    GazeTarget.UP: (0.0, 10.0),
    GazeTarget.DOWN: (0.0, -8.0),
    GazeTarget.AWAY: (12.0, 6.0),
    GazeTarget.CENTER: (0.0, 0.0),
}


class EyeState(BaseModel):
    """Snapshot of active ocular orientation and eyelid state."""
    model_config = ConfigDict(frozen=True)

    target: GazeTarget = GazeTarget.USER
    pitch_deg: float = Field(default=0.0, ge=-25.0, le=25.0)  # Up (+), Down (-)
    yaw_deg: float = Field(default=0.0, ge=-35.0, le=35.0)    # Right (+), Left (-)
    blink_weight: float = Field(default=0.0, ge=0.0, le=1.0)  # 0.0 = open, 1.0 = fully closed
    is_blinking: bool = False
    squint_weight: float = Field(default=0.0, ge=0.0, le=1.0)
    pupil_dilation: float = Field(default=1.0, ge=0.5, le=1.5)
    saccade_x: float = Field(default=0.0, ge=-3.0, le=3.0)
    saccade_y: float = Field(default=0.0, ge=-3.0, le=3.0)


class MiraEyeController:
    """Manages biological eye movements, saccades, gaze targets, and blinking."""

    def __init__(
        self,
        base_blink_interval_sec: float = 3.8,
        blink_duration_ms: int = 160,
    ) -> None:
        self._target: GazeTarget = GazeTarget.USER
        self._current_yaw: float = 0.0
        self._current_pitch: float = 0.0
        self._target_yaw: float = 0.0
        self._target_pitch: float = 0.0

        # Blinking timing
        self._base_blink_interval: float = base_blink_interval_sec
        self._time_until_next_blink: float = self._compute_next_blink_interval()
        self._is_blinking: bool = False
        self._blink_elapsed_sec: float = 0.0
        self._blink_duration_sec: float = blink_duration_ms / 1000.0
        self._blink_weight: float = 0.0

        # Micro-saccades & gaze stabilization
        self._saccade_timer: float = 0.0
        self._saccade_interval: float = 1.8
        self._saccade_x: float = 0.0
        self._saccade_y: float = 0.0

        # Expression modifiers
        self._squint_weight: float = 0.0
        self._pupil_dilation: float = 1.0

    def _compute_next_blink_interval(self) -> float:
        """Computes organic randomized interval between blinks with Gaussian spread."""
        jitter = random.uniform(-0.8, 0.8)
        return max(2.0, self._base_blink_interval + jitter)

    @property
    def current_target(self) -> GazeTarget:
        """Currently active gaze target."""
        return self._target

    @property
    def is_blinking(self) -> bool:
        """True if an eyelid blink is currently executing."""
        return self._is_blinking

    @property
    def blink_weight(self) -> float:
        """Current eyelid occlusion weight (0.0 to 1.0)."""
        return self._blink_weight

    def set_base_blink_interval(self, interval_sec: float) -> None:
        """Modulates base blink cadence based on character state."""
        self._base_blink_interval = max(1.5, interval_sec)

    def set_squint(self, weight: float) -> None:
        """Sets micro-squint factor."""
        self._squint_weight = max(0.0, min(1.0, weight))

    def look_at(self, target: GazeTarget | str) -> None:
        """Orients gaze toward a canonical gaze target."""
        if isinstance(target, str):
            try:
                target = GazeTarget(target.upper())
            except ValueError:
                target = GazeTarget.USER
        self._target = target
        yaw, pitch = TARGET_GAZE_COORDINATES.get(target, (0.0, 0.0))
        self._target_yaw = yaw
        self._target_pitch = pitch

    def look_at_user(self) -> None:
        """Directs warm, reassuring bedside eye contact at the user."""
        self.look_at(GazeTarget.USER)

    def look_at_screen(self) -> None:
        """Orients eyes toward patient telemetry, vitals, or chart monitor."""
        self.look_at(GazeTarget.SCREEN)

    def look_away(self) -> None:
        """Subtly breaks gaze during cognitive contemplation or thoughtful evaluation."""
        self.look_at(GazeTarget.AWAY)

    def blink(self) -> None:
        """Triggers an immediate natural eyelid blink."""
        if not self._is_blinking:
            self._is_blinking = True
            self._blink_elapsed_sec = 0.0
            self._blink_weight = 0.0

    def update(self, delta_time_sec: float) -> EyeState:
        """Updates ocular state over elapsed delta time."""
        # 1. Update Blinking Cycle
        if self._is_blinking:
            self._blink_elapsed_sec += delta_time_sec
            progress = self._blink_elapsed_sec / self._blink_duration_sec
            if progress >= 1.0:
                self._is_blinking = False
                self._blink_weight = 0.0
                self._time_until_next_blink = self._compute_next_blink_interval()
            else:
                # Biological blink curve: fast closing (first 35%), gentle reopening (65%)
                if progress < 0.35:
                    self._blink_weight = math.sin((progress / 0.35) * (math.pi / 2.0))
                else:
                    closing_progress = (progress - 0.35) / 0.65
                    self._blink_weight = math.cos(closing_progress * (math.pi / 2.0))
                self._blink_weight = max(0.0, min(1.0, self._blink_weight))
        else:
            self._time_until_next_blink -= delta_time_sec
            if self._time_until_next_blink <= 0.0:
                self.blink()

        # 2. Smooth Gaze Tracking Interpolation (smooth damping, no sudden snaps)
        gaze_speed = 7.0 * delta_time_sec  # Natural eye rotation speed
        self._current_yaw += (self._target_yaw - self._current_yaw) * min(1.0, gaze_speed)
        self._current_pitch += (self._target_pitch - self._current_pitch) * min(1.0, gaze_speed)

        # 3. Organic Micro-Saccades (subtle eye drift of 0.2-0.6 degrees to feel alive)
        self._saccade_timer += delta_time_sec
        if self._saccade_timer >= self._saccade_interval:
            self._saccade_timer = 0.0
            self._saccade_interval = random.uniform(1.2, 2.6)
            # Very subtle ocular fixation shift, strictly limited
            self._saccade_x = random.uniform(-0.5, 0.5)
            self._saccade_y = random.uniform(-0.3, 0.3)

        effective_yaw = self._current_yaw + self._saccade_x
        effective_pitch = self._current_pitch + self._saccade_y

        return EyeState(
            target=self._target,
            pitch_deg=round(effective_pitch, 2),
            yaw_deg=round(effective_yaw, 2),
            blink_weight=round(self._blink_weight, 3),
            is_blinking=self._is_blinking,
            squint_weight=round(self._squint_weight, 2),
            pupil_dilation=round(self._pupil_dilation, 2),
            saccade_x=round(self._saccade_x, 2),
            saccade_y=round(self._saccade_y, 2),
        )

    def reset(self) -> None:
        """Resets eye position to neutral attentive user focus."""
        self.look_at_user()
        self._current_yaw = 0.0
        self._current_pitch = 0.0
        self._is_blinking = False
        self._blink_weight = 0.0
        self._squint_weight = 0.0
        self._saccade_x = 0.0
        self._saccade_y = 0.0
        self._time_until_next_blink = self._compute_next_blink_interval()
