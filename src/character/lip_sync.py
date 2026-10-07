"""MIRA Character Lip Synchronization Contracts.

Defines foundational viseme schemas and audio-to-mouth animation frame contracts.
"""

from enum import Enum
from pydantic import BaseModel, Field


class VisemeId(str, Enum):
    """Standard Oculus / MPEG-4 compatible viseme identifiers."""
    SIL = "sil"  # Silence
    PP = "PP"    # p, b, m
    FF = "FF"    # f, v
    TH = "TH"    # th
    DD = "DD"    # t, d, n
    KK = "kk"    # k, g, ng
    CH = "CH"    # ch, j, sh
    SS = "SS"    # s, z
    NN = "nn"    # n, l
    RR = "RR"    # r
    AA = "aa"    # a (car)
    E = "E"      # e (bed)
    I = "I"      # i (tip)
    O = "O"      # o (top)
    U = "U"      # u (book)


class VisemeFrame(BaseModel):
    """Timed viseme target for lip sync rendering."""
    timestamp_ms: int = Field(ge=0)
    viseme: VisemeId
    weight: float = Field(default=1.0, ge=0.0, le=1.0)


class LipSyncTrack(BaseModel):
    """Complete lip sync sequence synchronized with synthesized voice audio."""
    duration_ms: int
    frames: list[VisemeFrame] = Field(default_factory=list)
