"""MIRA Character Asset Foundation & Animation API Endpoints.

Provides public inspection endpoints for canonical identity contracts, data-driven states,
multi-layer stack, animation readiness hooks, reference verification, and runtime animation controls.
"""

from typing import Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from src.character.animation_hooks import (
    ANIMATION_CAPABILITY_ARCHITECTURE,
    MiraAnimationCapabilityArchitecture,
)
from src.character.controller import (
    STATE_PRIORITIES,
    CharacterFrameState,
    MiraAnimationController,
)
from src.character.events import MiraEvent, MiraEventBus
from src.character.identity import (
    MIRA_CHARACTER_IDENTITY,
    MiraCharacterIdentity,
)
from src.character.layers import (
    CANONICAL_LAYER_STACK,
    MiraCharacterLayerStack,
)
from src.character.states import (
    MiraStateDefinition,
    MiraVisualState,
    get_all_states,
)

router = APIRouter(prefix="/api/v1/character", tags=["character"])

# Global shared animation controller instance for API interactions
GLOBAL_EVENT_BUS = MiraEventBus()
GLOBAL_ANIMATION_CONTROLLER = MiraAnimationController(
    initial_state=MiraVisualState.IDLE,
    event_bus=GLOBAL_EVENT_BUS,
)


class StateTransitionRequest(BaseModel):
    """Payload to request an animation state change."""
    state: MiraVisualState
    force: bool = False


class StateTransitionResponse(BaseModel):
    """Result of requested state transition."""
    success: bool
    current_state: MiraVisualState
    priority: int
    message: str


class EventDispatchPayload(BaseModel):
    """Payload to dispatch a character event."""
    event: MiraEvent
    source: str = "api"
    metadata: dict[str, Any] = Field(default_factory=dict)


@router.get("/identity", response_model=MiraCharacterIdentity)
async def get_character_identity() -> MiraCharacterIdentity:
    """Returns the immutable canonical MIRA character identity contract."""
    return MIRA_CHARACTER_IDENTITY


@router.get("/states", response_model=list[MiraStateDefinition])
async def list_character_states() -> list[MiraStateDefinition]:
    """Returns the 13 canonical data-driven character states."""
    return get_all_states()


@router.get("/layers", response_model=MiraCharacterLayerStack)
async def get_character_layers() -> MiraCharacterLayerStack:
    """Returns the 10-layer visual architecture stack."""
    return CANONICAL_LAYER_STACK


@router.get("/animation-hooks", response_model=MiraAnimationCapabilityArchitecture)
async def get_animation_hooks() -> MiraAnimationCapabilityArchitecture:
    """Returns the future animation compatibility architecture contracts."""
    return ANIMATION_CAPABILITY_ARCHITECTURE


@router.get("/verify-reference")
async def verify_canonical_reference() -> dict[str, Any]:
    """Verifies that MIRA_FACE_MODEL exists on disk and its SHA256 checksum matches."""
    is_valid = MIRA_CHARACTER_IDENTITY.verify_asset_integrity()
    return {
        "model_name": MIRA_CHARACTER_IDENTITY.visual_reference.model_name,
        "version": MIRA_CHARACTER_IDENTITY.character_version,
        "expected_sha256": MIRA_CHARACTER_IDENTITY.visual_reference.canonical_sha256,
        "is_valid": is_valid,
        "status": "CANONICAL_ANCHOR_VERIFIED" if is_valid else "VERIFICATION_FAILED",
    }


@router.get("/priorities")
async def get_state_priorities() -> dict[str, int]:
    """Returns the canonical state priority hierarchy table."""
    return {state.value: prio for state, prio in STATE_PRIORITIES.items()}


@router.get("/telemetry", response_model=CharacterFrameState)
async def get_character_telemetry() -> CharacterFrameState:
    """Returns live telemetry snapshot of character subsystems (eye, head, expression, lip-sync)."""
    return GLOBAL_ANIMATION_CONTROLLER.update(0.016)


@router.post("/state", response_model=StateTransitionResponse)
async def set_character_state(req: StateTransitionRequest) -> StateTransitionResponse:
    """Requests transition to a new visual state with strict priority enforcement."""
    success = GLOBAL_ANIMATION_CONTROLLER.set_state(req.state, force=req.force)
    current = GLOBAL_ANIMATION_CONTROLLER.current_state
    priority = GLOBAL_ANIMATION_CONTROLLER.current_priority
    if success:
        return StateTransitionResponse(
            success=True,
            current_state=current,
            priority=priority,
            message=f"Successfully transitioned to state {current.value}",
        )
    return StateTransitionResponse(
        success=False,
        current_state=current,
        priority=priority,
        message=(
            f"State transition to {req.state.value} rejected due to higher active priority "
            f"({current.value} = {priority} > {req.state.value} = {STATE_PRIORITIES.get(req.state, 0)})."
        ),
    )


@router.post("/event")
async def post_character_event(req: EventDispatchPayload) -> dict[str, Any]:
    """Publishes a character event onto the event bus driving decoupled state transitions."""
    GLOBAL_EVENT_BUS.publish(req.event, source=req.source, metadata=req.metadata)
    return {
        "event": req.event.value,
        "current_state": GLOBAL_ANIMATION_CONTROLLER.current_state.value,
        "priority": GLOBAL_ANIMATION_CONTROLLER.current_priority,
    }


@router.post("/interrupt")
async def trigger_interruption() -> dict[str, Any]:
    """Triggers immediate patient conversational barge-in interruption."""
    GLOBAL_ANIMATION_CONTROLLER.interrupt()
    return {
        "status": "INTERRUPTED",
        "current_state": GLOBAL_ANIMATION_CONTROLLER.current_state.value,
        "priority": GLOBAL_ANIMATION_CONTROLLER.current_priority,
    }
