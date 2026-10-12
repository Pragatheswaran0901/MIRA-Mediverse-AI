"""Comprehensive unit test suite for MIRA Interactive Character Animation Foundation (Block 3).

Verifies all 10 core requirements:
1. IDLE state behavior & parameters
2. LISTENING state behavior & attentive focus
3. THINKING state behavior & cognitive contemplation
4. SPEAKING state behavior & speech cadence
5. CONCERNED state behavior & priority
6. EMERGENCY state behavior & maximum priority lock
7. State transitions across all 13 states
8. Animation priority enforcement:
   - EMERGENCY beats IDLE
   - SPEAKING beats IDLE
   - LISTENING beats IDLE
   - Lower priority cannot override higher priority (EMERGENCY cannot be overridden by IDLE)
9. Reset to IDLE & return_to_idle
10. Controller lifecycle (pause, resume, update progression, interruption handling)

Plus tests for EyeController, AttentionController, LipSyncController, EventBus, and API routes.
"""

import pytest
from httpx import ASGITransport, AsyncClient
from src.api.app import create_app
from src.character import (
    STATE_PRIORITIES,
    AttentionTarget,
    FacialExpressionId,
    GazeTarget,
    MiraAnimationController,
    MiraAttentionController,
    MiraCharacter,
    MiraEvent,
    MiraEventBus,
    MiraExpressionController,
    MiraEyeController,
    MiraLipSyncController,
    MiraVisualState,
    VisemeId,
)


@pytest.fixture
def controller():
    """Provides a fresh MiraAnimationController initialized to IDLE."""
    return MiraAnimationController(initial_state=MiraVisualState.IDLE)


@pytest.fixture
def app():
    """FastAPI test app fixture."""
    return create_app()


# ------------------------------------------------------------------------------
# 1. IDLE State Tests
# ------------------------------------------------------------------------------

def test_idle_state_baseline(controller: MiraAnimationController):
    """Verifies baseline IDLE state parameters, breathing, and gaze."""
    assert controller.current_state == MiraVisualState.IDLE
    assert controller.current_priority == 10

    frame = controller.update(0.1)
    assert frame.state == MiraVisualState.IDLE
    assert frame.is_paused is False
    assert frame.eye_state.target == GazeTarget.USER
    assert frame.attention_state.target == AttentionTarget.USER
    assert frame.attention_state.is_nodding is False
    assert frame.expression_weights.mouth_smile_warmth > 0.05
    assert frame.mouth_weights.jaw_open == 0.0


# ------------------------------------------------------------------------------
# 2. LISTENING State Tests
# ------------------------------------------------------------------------------

def test_listening_state_behavior(controller: MiraAnimationController):
    """Verifies attentive posture, forward lean, and listening nod."""
    controller.start_listening()
    assert controller.current_state == MiraVisualState.LISTENING
    assert controller.current_priority == 50

    frame = controller.update(0.05)
    assert frame.eye_state.target == GazeTarget.USER
    assert frame.attention_state.is_nodding is True  # Single gentle acknowledgment nod triggered
    assert frame.attention_state.posture_lean >= 0.0  # Attentive forward lean towards patient


# ------------------------------------------------------------------------------
# 3. THINKING State Tests
# ------------------------------------------------------------------------------

def test_thinking_state_behavior(controller: MiraAnimationController):
    """Verifies cognitive contemplation with subtle upward gaze shift."""
    controller.start_thinking()
    assert controller.current_state == MiraVisualState.THINKING
    assert controller.current_priority == 45

    frame = controller.update(0.1)
    # Eye target diverted away/upward during reflection
    assert frame.eye_state.target == GazeTarget.AWAY
    assert frame.mouth_weights.jaw_open == 0.0  # Not speaking while thinking


# ------------------------------------------------------------------------------
# 4. SPEAKING State Tests
# ------------------------------------------------------------------------------

def test_speaking_state_behavior(controller: MiraAnimationController):
    """Verifies clinical delivery posture and lip-sync readiness."""
    controller.start_speaking()
    assert controller.current_state == MiraVisualState.SPEAKING
    assert controller.current_priority == 60

    # Feed viseme to simulate speech
    controller.lip_sync_controller.feed_viseme(VisemeId.AA, weight=0.8)
    frame = controller.update(0.05)
    assert frame.mouth_weights.jaw_open > 0.1
    assert frame.eye_state.target == GazeTarget.USER


# ------------------------------------------------------------------------------
# 5. CONCERNED State Tests
# ------------------------------------------------------------------------------

def test_concerned_state_behavior(controller: MiraAnimationController):
    """Verifies heightened clinical vigilance and brow elevation."""
    controller.show_concern()
    assert controller.current_state == MiraVisualState.CONCERNED
    assert controller.current_priority == 70

    # Advance 0.4s so smooth expression interpolation completes
    frame = controller.update(0.4)
    assert frame.expression_weights.brow_inner_up > 0.1
    assert frame.expression_weights.brow_down_concern > 0.1


# ------------------------------------------------------------------------------
# 6. EMERGENCY State Tests
# ------------------------------------------------------------------------------

def test_emergency_state_behavior(controller: MiraAnimationController):
    """Verifies acute red-flag emergency posture and priority 100."""
    controller.show_emergency()
    assert controller.current_state == MiraVisualState.EMERGENCY
    assert controller.current_priority == 100

    # Advance 0.4s so smooth expression interpolation completes
    frame = controller.update(0.4)
    assert frame.expression_weights.eye_wide > 0.2
    assert frame.attention_state.breathing_scale > 0.99



# ------------------------------------------------------------------------------
# 7. State Transitions Across All 13 States
# ------------------------------------------------------------------------------

def test_transitions_across_all_thirteen_states(controller: MiraAnimationController):
    """Verifies valid transitions through all 13 canonical states."""
    all_states = list(MiraVisualState)
    assert len(all_states) == 13

    for state in all_states:
        success = controller.set_state(state, force=True)
        assert success is True
        assert controller.current_state == state

        frame = controller.update(0.016)
        assert frame.state == state


# ------------------------------------------------------------------------------
# 8. Animation Priority Enforcement Tests
# ------------------------------------------------------------------------------

def test_priority_hierarchy_ranking():
    """Verifies priority numerical ranking invariants."""
    assert STATE_PRIORITIES[MiraVisualState.EMERGENCY] == 100
    assert STATE_PRIORITIES[MiraVisualState.ESCALATING] == 90
    assert STATE_PRIORITIES[MiraVisualState.SERIOUS] == 80
    assert STATE_PRIORITIES[MiraVisualState.CONCERNED] == 70
    assert STATE_PRIORITIES[MiraVisualState.SPEAKING] == 60
    assert STATE_PRIORITIES[MiraVisualState.LISTENING] == 50
    assert STATE_PRIORITIES[MiraVisualState.THINKING] == 45
    assert STATE_PRIORITIES[MiraVisualState.IDLE] == 10

    # Invariants:
    # EMERGENCY > ESCALATING > CONCERNED > SPEAKING / LISTENING > IDLE
    assert STATE_PRIORITIES[MiraVisualState.EMERGENCY] > STATE_PRIORITIES[MiraVisualState.IDLE]
    assert STATE_PRIORITIES[MiraVisualState.SPEAKING] > STATE_PRIORITIES[MiraVisualState.IDLE]
    assert STATE_PRIORITIES[MiraVisualState.LISTENING] > STATE_PRIORITIES[MiraVisualState.IDLE]


def test_emergency_cannot_be_overridden_by_idle(controller: MiraAnimationController):
    """CRITICAL TEST: Verifies that EMERGENCY cannot be overridden by IDLE without force."""
    controller.show_emergency()
    assert controller.current_state == MiraVisualState.EMERGENCY

    # Attempt to transition to IDLE without force
    success = controller.set_state(MiraVisualState.IDLE, force=False)
    assert success is False
    assert controller.current_state == MiraVisualState.EMERGENCY

    # Attempt to transition to LISTENING without force
    success = controller.set_state(MiraVisualState.LISTENING, force=False)
    assert success is False
    assert controller.current_state == MiraVisualState.EMERGENCY


def test_speaking_beats_idle(controller: MiraAnimationController):
    """Verifies that SPEAKING (60) overrides IDLE (10)."""
    assert controller.current_state == MiraVisualState.IDLE
    success = controller.set_state(MiraVisualState.SPEAKING)
    assert success is True
    assert controller.current_state == MiraVisualState.SPEAKING


def test_listening_beats_idle(controller: MiraAnimationController):
    """Verifies that LISTENING (50) overrides IDLE (10)."""
    assert controller.current_state == MiraVisualState.IDLE
    success = controller.set_state(MiraVisualState.LISTENING)
    assert success is True
    assert controller.current_state == MiraVisualState.LISTENING


def test_speaking_can_transition_to_listening_on_interrupt(controller: MiraAnimationController):
    """Verifies that patient speaking halts MIRA speaking and shifts to LISTENING."""
    controller.start_speaking()
    assert controller.current_state == MiraVisualState.SPEAKING

    # Patient interrupts
    controller.interrupt()
    assert controller.current_state == MiraVisualState.LISTENING
    assert controller.lip_sync_controller.is_active is False


def test_listening_transitions_to_thinking_then_speaking(controller: MiraAnimationController):
    """Verifies conversational flow: LISTENING -> THINKING -> SPEAKING."""
    controller.start_listening()
    assert controller.current_state == MiraVisualState.LISTENING

    # AI begins processing
    controller.set_state(MiraVisualState.THINKING, force=True)
    assert controller.current_state == MiraVisualState.THINKING

    # AI begins speaking (SPEAKING 60 > THINKING 45)
    success = controller.set_state(MiraVisualState.SPEAKING)
    assert success is True
    assert controller.current_state == MiraVisualState.SPEAKING


# ------------------------------------------------------------------------------
# 9. Reset and Return to IDLE Tests
# ------------------------------------------------------------------------------

def test_return_to_idle_from_any_state(controller: MiraAnimationController):
    """Verifies safe return to IDLE readiness."""
    controller.show_emergency()
    assert controller.current_state == MiraVisualState.EMERGENCY

    controller.return_to_idle()
    assert controller.current_state == MiraVisualState.IDLE


def test_reset_restores_all_subsystems(controller: MiraAnimationController):
    """Verifies reset resets eyes, head, expression, and mouth."""
    controller.show_emergency()
    controller.eye_controller.look_away()
    controller.attention_controller.set_target(AttentionTarget.SCREEN)
    controller.lip_sync_controller.feed_viseme(VisemeId.AA)

    controller.reset()
    assert controller.current_state == MiraVisualState.IDLE
    assert controller.eye_controller.current_target == GazeTarget.USER
    assert controller.attention_controller.current_target == AttentionTarget.USER
    assert controller.lip_sync_controller.is_active is False


# ------------------------------------------------------------------------------
# 10. Controller Lifecycle Tests
# ------------------------------------------------------------------------------

def test_controller_pause_and_resume(controller: MiraAnimationController):
    """Verifies lifecycle pausing and resumption."""
    assert controller.is_paused is False

    controller.pause()
    assert controller.is_paused is True
    frame_paused = controller.update(0.1)
    assert frame_paused.is_paused is True

    controller.resume()
    assert controller.is_paused is False
    frame_resumed = controller.update(0.1)
    assert frame_resumed.is_paused is False


# ------------------------------------------------------------------------------
# Eye, Attention, and Lip Sync Controller Tests
# ------------------------------------------------------------------------------

def test_eye_controller_blinking():
    """Verifies organic blinking cycle execution."""
    eye = MiraEyeController(blink_duration_ms=160)
    assert eye.is_blinking is False

    eye.blink()
    assert eye.is_blinking is True

    # Advance 80ms (halfway)
    state = eye.update(0.08)
    assert state.blink_weight > 0.0

    # Advance beyond duration
    state_done = eye.update(0.12)
    assert state_done.is_blinking is False
    assert state_done.blink_weight == 0.0


def test_eye_controller_gaze_targets():
    """Verifies gaze target coordinates and lookAt methods."""
    eye = MiraEyeController()
    eye.look_at_screen()
    assert eye.current_target == GazeTarget.SCREEN

    eye.look_away()
    assert eye.current_target == GazeTarget.AWAY

    eye.look_at_user()
    assert eye.current_target == GazeTarget.USER


def test_attention_controller_head_targets():
    """Verifies head orientation targets."""
    att = MiraAttentionController()
    att.orient_to_screen()
    assert att.current_target == AttentionTarget.SCREEN

    att.orient_to_user()
    assert att.current_target == AttentionTarget.USER


def test_attention_controller_listening_nod():
    """Verifies single gentle listening nod progression."""
    att = MiraAttentionController()
    assert att.is_nodding is False

    att.trigger_listening_nod()
    assert att.is_nodding is True

    # Mid-nod pitch offset dip
    state = att.update(0.5)
    assert state.head_pitch_deg < 0.0  # Downward dip

    # Complete nod
    state_done = att.update(0.8)
    assert state_done.is_nodding is False


def test_lip_sync_viseme_mapping():
    """Verifies viseme mouth morph weights."""
    lips = MiraLipSyncController()
    assert lips.is_active is False

    lips.feed_viseme(VisemeId.AA, weight=1.0)
    assert lips.is_active is True
    assert lips.current_viseme == VisemeId.AA

    weights = lips.update(0.05)
    assert weights.jaw_open > 0.2

    lips.stop()
    assert lips.is_active is False


def test_lip_sync_speech_energy_cadence():
    """Verifies fallback acoustic energy cadence."""
    lips = MiraLipSyncController()
    lips.feed_audio_energy(energy_rms=0.7)
    assert lips.is_active is True

    weights = lips.update(0.05)
    assert weights.jaw_open > 0.1

    lips.feed_audio_energy(energy_rms=0.0)
    assert lips.is_active is False


# ------------------------------------------------------------------------------
# Event Bus Integration Tests
# ------------------------------------------------------------------------------

def test_event_bus_pub_sub():
    """Verifies event bus subscription and notification."""
    bus = MiraEventBus()
    received = []

    bus.subscribe(MiraEvent.USER_STARTED_SPEAKING, lambda p: received.append(p))
    payload = bus.publish(MiraEvent.USER_STARTED_SPEAKING, source="mic")

    assert len(received) == 1
    assert received[0].event_type == MiraEvent.USER_STARTED_SPEAKING
    assert received[0].source == "mic"


def test_event_bus_drives_controller_automatically():
    """Verifies that posting events directly drives character animation state."""
    bus = MiraEventBus()
    ctrl = MiraAnimationController(initial_state=MiraVisualState.IDLE, event_bus=bus)

    assert ctrl.current_state == MiraVisualState.IDLE

    # User speaks -> shifts to LISTENING
    bus.publish(MiraEvent.USER_STARTED_SPEAKING)
    assert ctrl.current_state == MiraVisualState.LISTENING

    # AI processing -> shifts to THINKING
    bus.publish(MiraEvent.AI_PROCESSING)
    assert ctrl.current_state == MiraVisualState.THINKING

    # AI speaks -> shifts to SPEAKING
    bus.publish(MiraEvent.AI_STARTED_SPEAKING)
    assert ctrl.current_state == MiraVisualState.SPEAKING

    # User interrupts -> shifts to LISTENING immediately
    bus.publish(MiraEvent.USER_INTERRUPTED)
    assert ctrl.current_state == MiraVisualState.LISTENING

    # Emergency detected -> shifts to EMERGENCY
    bus.publish(MiraEvent.EMERGENCY_DETECTED)
    assert ctrl.current_state == MiraVisualState.EMERGENCY


# ------------------------------------------------------------------------------
# Component Wrapper Tests
# ------------------------------------------------------------------------------

def test_mira_character_component_wrapper():
    """Verifies MiraCharacter component convenience methods."""
    char = MiraCharacter(state=MiraVisualState.IDLE)
    assert char.current_state == MiraVisualState.IDLE

    char.start_listening()
    assert char.current_state == MiraVisualState.LISTENING

    char.start_speaking()
    assert char.current_state == MiraVisualState.SPEAKING

    char.interrupt()
    assert char.current_state == MiraVisualState.LISTENING

    char.show_emergency()
    assert char.current_state == MiraVisualState.EMERGENCY

    char.return_to_idle()
    assert char.current_state == MiraVisualState.IDLE


# ------------------------------------------------------------------------------
# API Endpoints Integration Tests
# ------------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_api_priorities_endpoint(app):
    """Verifies GET /api/v1/character/priorities returns complete priority table."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/v1/character/priorities")
        assert resp.status_code == 200
        data = resp.json()
        assert data["EMERGENCY"] == 100
        assert data["SPEAKING"] == 60
        assert data["LISTENING"] == 50
        assert data["IDLE"] == 10


@pytest.mark.asyncio
async def test_api_telemetry_endpoint(app):
    """Verifies GET /api/v1/character/telemetry returns live frame snapshot."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/v1/character/telemetry")
        assert resp.status_code == 200
        data = resp.json()
        assert "state" in data
        assert "eye_state" in data
        assert "attention_state" in data
        assert "expression_weights" in data
        assert "mouth_weights" in data


@pytest.mark.asyncio
async def test_api_state_transition_endpoint(app):
    """Verifies POST /api/v1/character/state transitions and rejects on lower priority."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # 1. Transition to LISTENING (from IDLE)
        resp = await client.post(
            "/api/v1/character/state",
            json={"state": "LISTENING", "force": False},
        )
        assert resp.status_code == 200
        assert resp.json()["success"] is True
        assert resp.json()["current_state"] == "LISTENING"

        # 2. Escalate to EMERGENCY
        resp = await client.post(
            "/api/v1/character/state",
            json={"state": "EMERGENCY", "force": False},
        )
        assert resp.status_code == 200
        assert resp.json()["success"] is True
        assert resp.json()["current_state"] == "EMERGENCY"

        # 3. Attempt to transition to IDLE without force (Must be rejected)
        resp_reject = await client.post(
            "/api/v1/character/state",
            json={"state": "IDLE", "force": False},
        )
        assert resp_reject.status_code == 200
        assert resp_reject.json()["success"] is False
        assert resp_reject.json()["current_state"] == "EMERGENCY"

        # 4. Force reset to IDLE
        resp_force = await client.post(
            "/api/v1/character/state",
            json={"state": "IDLE", "force": True},
        )
        assert resp_force.status_code == 200
        assert resp_force.json()["success"] is True
        assert resp_force.json()["current_state"] == "IDLE"


@pytest.mark.asyncio
async def test_api_interrupt_endpoint(app):
    """Verifies POST /api/v1/character/interrupt immediately switches to LISTENING."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Start speaking
        await client.post(
            "/api/v1/character/state",
            json={"state": "SPEAKING", "force": True},
        )

        # Trigger interrupt
        resp = await client.post("/api/v1/character/interrupt")
        assert resp.status_code == 200
        assert resp.json()["current_state"] == "LISTENING"
