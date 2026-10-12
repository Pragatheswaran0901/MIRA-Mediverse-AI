"""MIRA Character Lip Sync Controller Architecture.

Prepares the formal phonetic and audio synchronization interface connecting:
voice audio stream -> phoneme/viseme timing -> mouth blendshapes -> facial cadence.
"""

from enum import Enum
from pydantic import BaseModel, ConfigDict, Field
from src.character.lip_sync import LipSyncTrack, VisemeFrame, VisemeId


class MouthShapeWeights(BaseModel):
    """Mouth morph targets driving phonetic viseme mouth openings and shapes."""
    model_config = ConfigDict(frozen=True)

    jaw_open: float = Field(default=0.0, ge=0.0, le=1.0)
    lip_pucker: float = Field(default=0.0, ge=0.0, le=1.0)
    lip_funnel: float = Field(default=0.0, ge=0.0, le=1.0)
    lip_wide: float = Field(default=0.0, ge=0.0, le=1.0)
    lip_press: float = Field(default=0.0, ge=0.0, le=1.0)
    current_viseme: VisemeId = VisemeId.SIL


# Canonical phonetic mouth mappings for Oculus / MPEG-4 visemes
VISEME_MORPH_TARGETS: dict[VisemeId, MouthShapeWeights] = {
    VisemeId.SIL: MouthShapeWeights(jaw_open=0.0, lip_pucker=0.0, lip_funnel=0.0, lip_wide=0.0, lip_press=0.0, current_viseme=VisemeId.SIL),
    VisemeId.PP: MouthShapeWeights(jaw_open=0.05, lip_pucker=0.0, lip_funnel=0.0, lip_wide=0.0, lip_press=0.8, current_viseme=VisemeId.PP),
    VisemeId.FF: MouthShapeWeights(jaw_open=0.15, lip_pucker=0.0, lip_funnel=0.1, lip_wide=0.1, lip_press=0.4, current_viseme=VisemeId.FF),
    VisemeId.TH: MouthShapeWeights(jaw_open=0.2, lip_pucker=0.0, lip_funnel=0.1, lip_wide=0.2, lip_press=0.0, current_viseme=VisemeId.TH),
    VisemeId.DD: MouthShapeWeights(jaw_open=0.3, lip_pucker=0.0, lip_funnel=0.0, lip_wide=0.3, lip_press=0.0, current_viseme=VisemeId.DD),
    VisemeId.KK: MouthShapeWeights(jaw_open=0.35, lip_pucker=0.0, lip_funnel=0.0, lip_wide=0.2, lip_press=0.0, current_viseme=VisemeId.KK),
    VisemeId.CH: MouthShapeWeights(jaw_open=0.25, lip_pucker=0.3, lip_funnel=0.3, lip_wide=0.1, lip_press=0.0, current_viseme=VisemeId.CH),
    VisemeId.SS: MouthShapeWeights(jaw_open=0.15, lip_pucker=0.0, lip_funnel=0.0, lip_wide=0.35, lip_press=0.0, current_viseme=VisemeId.SS),
    VisemeId.NN: MouthShapeWeights(jaw_open=0.25, lip_pucker=0.0, lip_funnel=0.0, lip_wide=0.25, lip_press=0.0, current_viseme=VisemeId.NN),
    VisemeId.RR: MouthShapeWeights(jaw_open=0.3, lip_pucker=0.4, lip_funnel=0.2, lip_wide=0.0, lip_press=0.0, current_viseme=VisemeId.RR),
    VisemeId.AA: MouthShapeWeights(jaw_open=0.7, lip_pucker=0.0, lip_funnel=0.2, lip_wide=0.2, lip_press=0.0, current_viseme=VisemeId.AA),
    VisemeId.E: MouthShapeWeights(jaw_open=0.45, lip_pucker=0.0, lip_funnel=0.0, lip_wide=0.45, lip_press=0.0, current_viseme=VisemeId.E),
    VisemeId.I: MouthShapeWeights(jaw_open=0.25, lip_pucker=0.0, lip_funnel=0.0, lip_wide=0.5, lip_press=0.0, current_viseme=VisemeId.I),
    VisemeId.O: MouthShapeWeights(jaw_open=0.55, lip_pucker=0.4, lip_funnel=0.5, lip_wide=0.0, lip_press=0.0, current_viseme=VisemeId.O),
    VisemeId.U: MouthShapeWeights(jaw_open=0.3, lip_pucker=0.7, lip_funnel=0.3, lip_wide=0.0, lip_press=0.0, current_viseme=VisemeId.U),
}


class MiraLipSyncController:
    """Controls mouth animation from audio streams, viseme tracks, or acoustic cadence."""

    def __init__(self) -> None:
        self._is_active: bool = False
        self._current_viseme: VisemeId = VisemeId.SIL
        self._current_weights: MouthShapeWeights = VISEME_MORPH_TARGETS[VisemeId.SIL]
        self._target_weights: MouthShapeWeights = VISEME_MORPH_TARGETS[VisemeId.SIL]

        # Viseme track playback state
        self._active_track: LipSyncTrack | None = None
        self._track_elapsed_ms: int = 0
        self._current_frame_index: int = 0

        # Acoustic energy cadence fallback (when visemes are not streamed)
        self._vocal_energy_rms: float = 0.0
        self._speech_cadence_wpm: int = 150

    @property
    def is_active(self) -> bool:
        """True if speech animation is currently active."""
        return self._is_active

    @property
    def current_viseme(self) -> VisemeId:
        """Active viseme target."""
        return self._current_viseme

    @property
    def current_weights(self) -> MouthShapeWeights:
        """Active mouth morph target weights."""
        return self._current_weights

    def load_track(self, track: LipSyncTrack) -> None:
        """Loads a pre-calculated viseme track synchronized with synthesized audio."""
        self._active_track = track
        self._track_elapsed_ms = 0
        self._current_frame_index = 0
        self._is_active = True

    def feed_viseme(self, viseme: VisemeId, weight: float = 1.0) -> None:
        """Accepts real-time streaming visemes from TTS voice engine."""
        self._is_active = (viseme != VisemeId.SIL)
        self._current_viseme = viseme
        base = VISEME_MORPH_TARGETS.get(viseme, VISEME_MORPH_TARGETS[VisemeId.SIL])
        w = max(0.0, min(1.0, weight))
        self._target_weights = MouthShapeWeights(
            jaw_open=round(base.jaw_open * w, 3),
            lip_pucker=round(base.lip_pucker * w, 3),
            lip_funnel=round(base.lip_funnel * w, 3),
            lip_wide=round(base.lip_wide * w, 3),
            lip_press=round(base.lip_press * w, 3),
            current_viseme=viseme,
        )

    def feed_audio_energy(self, energy_rms: float, cadence_wpm: int = 150) -> None:
        """Fallback acoustic cadence driver when visemes are uncomputed."""
        self._vocal_energy_rms = max(0.0, min(1.0, energy_rms))
        self._speech_cadence_wpm = max(80, min(240, cadence_wpm))
        self._is_active = (self._vocal_energy_rms > 0.05)

        if not self._is_active:
            self.stop()
            return

        # Derive natural jaw aperture from vocal energy
        jaw = min(0.65, self._vocal_energy_rms * 0.8)
        self._target_weights = MouthShapeWeights(
            jaw_open=round(jaw, 3),
            lip_pucker=0.0,
            lip_funnel=round(jaw * 0.3, 3),
            lip_wide=round(jaw * 0.2, 3),
            lip_press=0.0,
            current_viseme=VisemeId.AA if jaw > 0.3 else VisemeId.E,
        )

    def stop(self) -> None:
        """Halts mouth animation and returns lips to neutral resting position."""
        self._is_active = False
        self._active_track = None
        self._track_elapsed_ms = 0
        self._current_frame_index = 0
        self._vocal_energy_rms = 0.0
        self._current_viseme = VisemeId.SIL
        self._target_weights = VISEME_MORPH_TARGETS[VisemeId.SIL]

    def update(self, delta_time_sec: float) -> MouthShapeWeights:
        """Smoothly interpolates mouth blendshapes over elapsed delta time."""
        delta_ms = int(delta_time_sec * 1000.0)

        # 1. Track playback progression
        if self._active_track and self._is_active:
            self._track_elapsed_ms += delta_ms
            if self._track_elapsed_ms >= self._active_track.duration_ms:
                self.stop()
            else:
                # Find current viseme frame
                frames = self._active_track.frames
                while (
                    self._current_frame_index < len(frames) - 1
                    and frames[self._current_frame_index + 1].timestamp_ms <= self._track_elapsed_ms
                ):
                    self._current_frame_index += 1

                if self._current_frame_index < len(frames):
                    current_frame = frames[self._current_frame_index]
                    self.feed_viseme(current_frame.viseme, current_frame.weight)

        # 2. Smooth coarticulation damping towards target weights
        damping = 18.0 * delta_time_sec  # Fast, articulate lip response
        clamp_damping = min(1.0, damping)

        w1 = self._current_weights
        w2 = self._target_weights

        def lerp(a: float, b: float) -> float:
            return a + (b - a) * clamp_damping

        self._current_weights = MouthShapeWeights(
            jaw_open=round(lerp(w1.jaw_open, w2.jaw_open), 3),
            lip_pucker=round(lerp(w1.lip_pucker, w2.lip_pucker), 3),
            lip_funnel=round(lerp(w1.lip_funnel, w2.lip_funnel), 3),
            lip_wide=round(lerp(w1.lip_wide, w2.lip_wide), 3),
            lip_press=round(lerp(w1.lip_press, w2.lip_press), 3),
            current_viseme=self._target_weights.current_viseme,
        )
        return self._current_weights
