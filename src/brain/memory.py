"""MIRA Memory Architecture Abstractions.

Defines foundational protocols for Short-Term Working Memory (session context)
and Long-Term Persistent Memory (patient profile, medical history, preferences).
"""

from typing import Protocol, runtime_checkable
from pydantic import BaseModel, Field
from src.core.contracts import MiraMessage


class PatientMemoryProfile(BaseModel):
    """Patient medical memory profile for long-term personalization."""
    patient_id: str
    preferred_name: str | None = None
    known_allergies: list[str] = Field(default_factory=list)
    chronic_conditions: list[str] = Field(default_factory=list)
    current_medications: list[str] = Field(default_factory=list)
    emergency_contact: str | None = None


@runtime_checkable
class ShortTermMemoryProvider(Protocol):
    """Protocol for managing in-session conversation history."""
    async def get_history(self, session_id: str, limit: int = 20) -> list[MiraMessage]:
        ...

    async def append_message(self, session_id: str, message: MiraMessage) -> None:
        ...

    async def clear_session(self, session_id: str) -> None:
        ...


@runtime_checkable
class LongTermMemoryProvider(Protocol):
    """Protocol for managing long-term patient health context across sessions."""
    async def get_profile(self, patient_id: str) -> PatientMemoryProfile | None:
        ...

    async def update_profile(self, profile: PatientMemoryProfile) -> None:
        ...


class InMemoryShortTermProvider:
    """In-memory baseline implementation of short-term memory."""
    def __init__(self) -> None:
        self._storage: dict[str, list[MiraMessage]] = {}

    async def get_history(self, session_id: str, limit: int = 20) -> list[MiraMessage]:
        messages = self._storage.get(session_id, [])
        return messages[-limit:]

    async def append_message(self, session_id: str, message: MiraMessage) -> None:
        if session_id not in self._storage:
            self._storage[session_id] = []
        self._storage[session_id].append(message)

    async def clear_session(self, session_id: str) -> None:
        self._storage.pop(session_id, None)
