"""MIRA Character Animation Event System.

Defines decoupled conversational, safety, and AI lifecycle events that drive
character animation without polluting the character subsystem with AI or medical logic.
"""

from collections.abc import Callable
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from pydantic import BaseModel, ConfigDict, Field


class MiraEvent(str, Enum):
    """Canonical events that drive MIRA character animation state and reactions."""
    USER_STARTED_SPEAKING = "USER_STARTED_SPEAKING"
    USER_STOPPED_SPEAKING = "USER_STOPPED_SPEAKING"
    USER_INTERRUPTED = "USER_INTERRUPTED"
    AI_PROCESSING = "AI_PROCESSING"
    AI_STARTED_SPEAKING = "AI_STARTED_SPEAKING"
    AI_STOPPED_SPEAKING = "AI_STOPPED_SPEAKING"
    EMERGENCY_DETECTED = "EMERGENCY_DETECTED"
    TRIAGE_ESCALATING = "TRIAGE_ESCALATING"
    CLINICAL_CONCERN_RAISED = "CLINICAL_CONCERN_RAISED"
    REASSURANCE_TRIGGERED = "REASSURANCE_TRIGGERED"
    SESSION_CONCLUDED = "SESSION_CONCLUDED"
    RESET_REQUESTED = "RESET_REQUESTED"


class MiraEventPayload(BaseModel):
    """Structured payload transmitted when a character event fires."""
    model_config = ConfigDict(frozen=True)

    event_type: MiraEvent
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    source: str = "system"
    metadata: dict[str, Any] = Field(default_factory=dict)


class MiraEventBus:
    """Decoupled event publisher/subscriber bus for character animation coordination.
    
    Permits future engines (MiraConversationEngine, MiraVoiceEngine, MiraSafetyEngine)
    to drive MIRA's physical presentation without coupling low-level animation logic.
    """

    def __init__(self) -> None:
        self._subscribers: dict[MiraEvent, list[Callable[[MiraEventPayload], None]]] = {
            event: [] for event in MiraEvent
        }
        self._wildcard_subscribers: list[Callable[[MiraEventPayload], None]] = []
        self._history: list[MiraEventPayload] = []

    def subscribe(
        self,
        event_type: MiraEvent,
        callback: Callable[[MiraEventPayload], None],
    ) -> Callable[[], None]:
        """Subscribes a listener to a specific event type. Returns an unsubscribe callable."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

        def unsubscribe() -> None:
            if callback in self._subscribers.get(event_type, []):
                self._subscribers[event_type].remove(callback)

        return unsubscribe

    def subscribe_all(
        self,
        callback: Callable[[MiraEventPayload], None],
    ) -> Callable[[], None]:
        """Subscribes a wildcard listener receiving all character events."""
        self._wildcard_subscribers.append(callback)

        def unsubscribe() -> None:
            if callback in self._wildcard_subscribers:
                self._wildcard_subscribers.remove(callback)

        return unsubscribe

    def publish(
        self,
        event_type: MiraEvent,
        source: str = "system",
        metadata: dict[str, Any] | None = None,
    ) -> MiraEventPayload:
        """Emits an event to all registered subscribers."""
        payload = MiraEventPayload(
            event_type=event_type,
            source=source,
            metadata=metadata or {},
        )
        self._history.append(payload)

        # Notify specific subscribers
        for callback in list(self._subscribers.get(event_type, [])):
            try:
                callback(payload)
            except Exception:
                pass

        # Notify wildcard subscribers
        for callback in list(self._wildcard_subscribers):
            try:
                callback(payload)
            except Exception:
                pass

        return payload

    @property
    def event_history(self) -> list[MiraEventPayload]:
        """Returns chronological history of emitted events."""
        return list(self._history)

    def clear_history(self) -> None:
        """Clears recorded event history."""
        self._history.clear()
