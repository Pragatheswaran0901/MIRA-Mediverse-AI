"""MIRA Speech-to-Text (STT) Abstractions.

Defines protocols and payload schemas for transcribing patient voice input.
"""

from typing import Protocol, runtime_checkable
from pydantic import BaseModel, Field


class STTTranscript(BaseModel):
    """Transcription output from audio input."""
    text: str
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    language: str = "en"
    duration_ms: int = 0
    is_final: bool = True


@runtime_checkable
class STTProvider(Protocol):
    """Protocol for transcribing speech audio into text."""
    async def transcribe(self, audio_bytes: bytes, sample_rate: int = 16000) -> STTTranscript:
        ...
