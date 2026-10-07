"""MIRA Text-to-Speech (TTS) & Custom Voice Profile Abstractions.

Defines MIRA's signature acoustic profile and speech synthesis protocol.
"""

from typing import Protocol, runtime_checkable
from pydantic import BaseModel, Field


class MiraVoiceProfile(BaseModel):
    """Custom acoustic signature profile for MIRA."""
    voice_id: str = "mira-caring-nurse-v1"
    name: str = "MIRA Signature Voice"
    gender: str = "female"
    style: str = "Warm, calm, empathetic, and professional"
    pitch: float = Field(default=1.0, ge=0.5, le=1.5)
    speaking_rate: float = Field(default=1.0, ge=0.5, le=2.0)
    sample_rate_hz: int = 24000


MIRA_DEFAULT_VOICE = MiraVoiceProfile()


class SynthesizedAudio(BaseModel):
    """Output from text-to-speech synthesis."""
    audio_bytes: bytes
    audio_format: str = "audio/wav"
    sample_rate_hz: int = 24000
    duration_ms: int = 0


@runtime_checkable
class TTSProvider(Protocol):
    """Protocol for converting text into MIRA's synthesized voice."""
    async def synthesize(
        self,
        text: str,
        profile: MiraVoiceProfile = MIRA_DEFAULT_VOICE,
    ) -> SynthesizedAudio:
        ...
