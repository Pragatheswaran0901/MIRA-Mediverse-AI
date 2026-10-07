"""MIRA Real-Time Audio Streaming Contracts.

Defines streaming audio chunks and bidirectional WebSocket event schemas.
"""

from enum import Enum
from pydantic import BaseModel, Field


class AudioStreamEventType(str, Enum):
    """Event types for real-time voice streaming."""
    CHUNK = "audio_chunk"
    START = "stream_start"
    STOP = "stream_stop"
    ERROR = "stream_error"


class AudioStreamChunk(BaseModel):
    """Individual audio packet for real-time playback."""
    event: AudioStreamEventType = AudioStreamEventType.CHUNK
    chunk_index: int = Field(ge=0)
    data: bytes
    is_last: bool = False
