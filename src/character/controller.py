"""MIRA Character Central Animation Controller.

The master state engine orchestrating MIRA's interactive character presentation:
- Strict state-driven animation priority engine
- Conversational interruption handling (instant stop speaking -> listening)
- Orchestration across Eye, Attention, Expression, and Lip-Sync subsystems
- Lifecycle awareness (pause/resume/visibility management)
- Clean, decoupled public API strictly prohibiting direct UI manipulation of raw rigs
"""

from typing import Any
from pydantic import BaseModel, ConfigDict, Field
from src.character.attention_controller import (
    AttentionState,
    AttentionTarget,
    MiraAttentionController,
)
from src.character.events import MiraEvent, MiraEventBus, MiraEventPayload
from src.character.expression_controller import (
    ExpressionMorphWeights,
    FacialExpressionId,
    MiraExpressionController,
)
from src.character.eye_controller import EyeState, GazeTarget, MiraEyeController
from src.character.lip_sync_controller import MouthShapeWeights, MiraLipSyncController
from src.character.states import (
    CHARACTER_STATE_REGISTRY,
    MiraStateDefinition,
    MiraVisualState,
    get_state_definition,
)

# Canonical hierarchical priority table (higher number beats lower number)
STATE_PRIORITIES: dict[MiraVisualState, int] = {
    MiraVisualState.EMERGENCY: 100,  # Acute red-flag critical directive
    MiraVisualState.ESCALATING: 90,  # Triage severity escalating
    MiraVisualState.SERIOUS: 80,     # Firm clinical non-negotiable instruction
    MiraVisualState.CONCERNED: 70,   # Heightened scrutiny of alarming symptom
    MiraVisualState.SPEAKING: 60,    # Active clinical guidance delivery
    MiraVisualState.LISTENING: 50,   # Attentive patient symptom intake
    MiraVisualState.THINKING: 45,    # Clinical reasoning & triage evaluation
    MiraVisualState.GREETING: 40,    # Welcoming introduction
    MiraVisualState.REASSURING: 30,  # Empathetic de-escalation
    MiraVisualState.CALMING: 30,     # Paced respiratory soothing
    MiraVisualState.FRIENDLY: 30,    # Warm companionship
    MiraVisualState.COMPLETED: 20,   # Session conclusion
    MiraVisualState.IDLE: 10,        # Baseline bedside readiness
}


# Mapping canonical visual states to corresponding facial expressions and subsystem targets
STATE_SUBSYSTEM_MAPPINGS: dict[MiraVisualState, dict[str, Any]] = {
    MiraVisualState.IDLE: {
        "expression": FacialExpressionId.NEUTRAL,
        "gaze": GazeTarget.USER,
        "attention": AttentionTarget.USER,
        "breathing_cpm": 14.0,
        "blink_interval": 3.8,
        "posture_lean": 0.0,
        "squint": 0.0,
    },
    MiraVisualState.GREETING: {
        "expression": FacialExpressionId.HAPPY,
        "gaze": GazeTarget.USER,
        "attention": AttentionTarget.USER,
        "breathing_cpm": 15.0,
        "blink_interval": 3.2,
        "posture_lean": 0.15,
        "squint": 0.1,
    },
    MiraVisualState.LISTENING: {
        "expression": FacialExpressionId.ATTENTIVE,
        "gaze": GazeTarget.USER,
        "attention": AttentionTarget.USER,
        "breathing_cpm": 13.0,
        "blink_interval": 4.0,
        "posture_lean": 0.35,  # Attentive forward lean towards patient
        "squint": 0.15,
    },
    MiraVisualState.THINKING: {
        "expression": FacialExpressionId.THINKING,
        "gaze": GazeTarget.AWAY,  # Subtle contemplative gaze shift
        "attention": AttentionTarget.UP,
        "breathing_cpm": 12.0,
        "blink_interval": 4.5,
        "posture_lean": 0.0,
        "squint": 0.2,
    },
    MiraVisualState.SPEAKING: {
        "expression": FacialExpressionId.ATTENTIVE,
        "gaze": GazeTarget.USER,
        "attention": AttentionTarget.USER,
        "breathing_cpm": 16.0,
        "blink_interval": 3.0,
        "posture_lean": 0.1,
        "squint": 0.05,
    },
    MiraVisualState.FRIENDLY: {
        "expression": FacialExpressionId.HAPPY,
        "gaze": GazeTarget.USER,
        "attention": AttentionTarget.USER,
        "breathing_cpm": 14.0,
        "blink_interval": 3.5,
        "posture_lean": 0.1,
        "squint": 0.15,
    },
    MiraVisualState.CONCERNED: {
        "expression": FacialExpressionId.CONCERNED,
        "gaze": GazeTarget.USER,
        "attention": AttentionTarget.USER,
        "breathing_cpm": 16.0,
        "blink_interval": 3.0,
        "posture_lean": 0.25,
        "squint": 0.25,
    },
    MiraVisualState.SERIOUS: {
        "expression": FacialExpressionId.SERIOUS,
        "gaze": GazeTarget.USER,
        "attention": AttentionTarget.USER,
        "breathing_cpm": 18.0,
        "blink_interval": 4.8,  # Alert unblinking focus
        "posture_lean": 0.0,    # Authoritative upright posture
        "squint": 0.1,
    },
    MiraVisualState.REASSURING: {
        "expression": FacialExpressionId.REASSURING,
        "gaze": GazeTarget.USER,
        "attention": AttentionTarget.USER,
        "breathing_cpm": 12.0,
        "blink_interval": 3.4,
        "posture_lean": 0.15,
        "squint": 0.1,
    },
    MiraVisualState.EMERGENCY: {
        "expression": FacialExpressionId.EMERGENCY,
        "gaze": GazeTarget.USER,
        "attention": AttentionTarget.USER,
        "breathing_cpm": 20.0,  # Heightened clinical alert
        "blink_interval": 5.0,  # Wide unblinking vigilance
        "posture_lean": 0.0,
        "squint": 0.0,
    },
    MiraVisualState.ESCALATING: {
        "expression": FacialExpressionId.CONCERNED,
        "gaze": GazeTarget.USER,
        "attention": AttentionTarget.USER,
        "breathing_cpm": 17.0,
        "blink_interval": 3.2,
        "posture_lean": 0.2,
        "squint": 0.2,
    },
    MiraVisualState.CALMING: {
        "expression": FacialExpressionId.CALM,
        "gaze": GazeTarget.USER,
        "attention": AttentionTarget.USER,
        "breathing_cpm": 8.0,   # Deliberately slowed breathing for anxiety soothing
        "blink_interval": 4.2,
        "posture_lean": 0.05,
        "squint": 0.05,
    },
    MiraVisualState.COMPLETED: {
        "expression": FacialExpressionId.CALM,
        "gaze": GazeTarget.USER,
        "attention": AttentionTarget.USER,
        "breathing_cpm": 14.0,
        "blink_interval": 3.6,
        "posture_lean": 0.0,
        "squint": 0.05,
    },
}


class CharacterFrameState(BaseModel):
    """Unified telemetry snapshot of MIRA character animation state at current frame."""
    model_config = ConfigDict(frozen=True)

    state: MiraVisualState
    priority: int
    is_paused: bool
    eye_state: EyeState
    attention_state: AttentionState
    expression_weights: ExpressionMorphWeights
    mouth_weights: MouthShapeWeights
    state_definition: MiraStateDefinition


class MiraAnimationController:
    """Master character animation controller driving MIRA's living presentation."""

    def __init__(
        self,
        initial_state: MiraVisualState = MiraVisualState.IDLE,
        event_bus: MiraEventBus | None = None,
    ) -> None:
        self._current_state: MiraVisualState = initial_state
        self._previous_state: MiraVisualState = initial_state
        self._is_paused: bool = False

        # Subsystem Controllers
        self.eye_controller = MiraEyeController()
        self.attention_controller = MiraAttentionController()
        self.expression_controller = MiraExpressionController()
        self.lip_sync_controller = MiraLipSyncController()

        # Decoupled Event Bus
        self.event_bus = event_bus or MiraEventBus()
        self._setup_event_listeners()

        # Initialize subsystem states
        self._apply_state_configuration(self._current_state)

    def _setup_event_listeners(self) -> None:
        """Wires up event bus handlers for conversational and safety triggers."""
        self.event_bus.subscribe(MiraEvent.USER_STARTED_SPEAKING, self._on_user_started_speaking)
        self.event_bus.subscribe(MiraEvent.USER_STOPPED_SPEAKING, self._on_user_stopped_speaking)
        self.event_bus.subscribe(MiraEvent.USER_INTERRUPTED, self._on_user_interrupted)
        self.event_bus.subscribe(MiraEvent.AI_PROCESSING, self._on_ai_processing)
        self.event_bus.subscribe(MiraEvent.AI_STARTED_SPEAKING, self._on_ai_started_speaking)
        self.event_bus.subscribe(MiraEvent.AI_STOPPED_SPEAKING, self._on_ai_stopped_speaking)
        self.event_bus.subscribe(MiraEvent.EMERGENCY_DETECTED, self._on_emergency_detected)
        self.event_bus.subscribe(MiraEvent.TRIAGE_ESCALATING, self._on_triage_escalating)
        self.event_bus.subscribe(MiraEvent.CLINICAL_CONCERN_RAISED, self._on_clinical_concern)
        self.event_bus.subscribe(MiraEvent.RESET_REQUESTED, lambda _: self.reset())

    # --------------------------------------------------------------------------
    # Event Handlers
    # --------------------------------------------------------------------------

    def _on_user_started_speaking(self, payload: MiraEventPayload) -> None:
        """Handles patient voice onset. If MIRA is speaking, trigger immediate interruption."""
        if self._current_state == MiraVisualState.SPEAKING:
            self.interrupt()
        else:
            self.start_listening()

    def _on_user_stopped_speaking(self, payload: MiraEventPayload) -> None:
        """Patient stopped speaking; prepare for reasoning or response."""
        # Remain in listening/attentive mode until AI processing or response begins
        pass

    def _on_user_interrupted(self, payload: MiraEventPayload) -> None:
        """Immediate barge-in handling."""
        self.interrupt()

    def _on_ai_processing(self, payload: MiraEventPayload) -> None:
        """Clinical knowledge reasoning in progress."""
        self.start_thinking()

    def _on_ai_started_speaking(self, payload: MiraEventPayload) -> None:
        """Active medical delivery onset."""
        self.start_speaking()

    def _on_ai_stopped_speaking(self, payload: MiraEventPayload) -> None:
        """Speech conclusion."""
        self.stop_speaking()

    def _on_emergency_detected(self, payload: MiraEventPayload) -> None:
        """Acute clinical red-flag trigger."""
        self.show_emergency()

    def _on_triage_escalating(self, payload: MiraEventPayload) -> None:
        """Triage severity elevation."""
        self.set_state(MiraVisualState.ESCALATING)

    def _on_clinical_concern(self, payload: MiraEventPayload) -> None:
        """Concerning symptom reported."""
        self.show_concern()

    # --------------------------------------------------------------------------
    # Priority & State Engine
    # --------------------------------------------------------------------------

    @property
    def current_state(self) -> MiraVisualState:
        """Active visual state."""
        return self._current_state

    @property
    def current_priority(self) -> int:
        """Numeric priority of current visual state."""
        return STATE_PRIORITIES.get(self._current_state, 0)

    @property
    def is_paused(self) -> bool:
        """True if animation updates are suspended."""
        return self._is_paused

    def get_priority_for_state(self, state: MiraVisualState) -> int:
        """Returns the priority value for a given state."""
        return STATE_PRIORITIES.get(state, 0)

    def can_transition_to(self, target_state: MiraVisualState) -> bool:
        """Determines if a transition to target_state is permitted under priority rules.
        
        Rules:
        - Target priority must be >= current priority, OR
        - Permitted conversational progression:
          * LISTENING -> THINKING (patient finished speaking -> AI reasoning)
          * SPEAKING -> LISTENING (patient barge-in interruption)
        - EMERGENCY cannot be overridden by non-emergency states without explicit force.
        """
        if self._current_state == MiraVisualState.EMERGENCY and target_state != MiraVisualState.EMERGENCY:
            return False
        if target_state == MiraVisualState.EMERGENCY:
            return True
        if self._current_state == MiraVisualState.LISTENING and target_state == MiraVisualState.THINKING:
            return True
        if self._current_state == MiraVisualState.SPEAKING and target_state == MiraVisualState.LISTENING:
            return True

        curr_prio = self.current_priority
        target_prio = STATE_PRIORITIES.get(target_state, 0)
        return target_prio >= curr_prio

    def set_state(self, state: MiraVisualState | str, force: bool = False) -> bool:
        """Transitions MIRA to a new visual state adhering to the priority hierarchy.
        
        Returns:
            bool: True if transition succeeded, False if rejected due to higher priority.
        """
        if isinstance(state, str):
            try:
                state = MiraVisualState(state.upper())
            except ValueError:
                return False

        if state == self._current_state:
            return True

        # Enforce priority and conversational progression rules
        if not force and not self.can_transition_to(state):
            return False

        self._previous_state = self._current_state
        self._current_state = state
        self._apply_state_configuration(state)
        return True

    def _apply_state_configuration(self, state: MiraVisualState) -> None:
        """Dispatches state parameters to all 4 subsystem controllers."""
        config = STATE_SUBSYSTEM_MAPPINGS.get(state, STATE_SUBSYSTEM_MAPPINGS[MiraVisualState.IDLE])

        # 1. Expression
        self.expression_controller.set_expression(config["expression"])

        # 2. Eye Subsystem
        self.eye_controller.look_at(config["gaze"])
        self.eye_controller.set_base_blink_interval(config["blink_interval"])
        self.eye_controller.set_squint(config["squint"])

        # 3. Attention Subsystem
        self.attention_controller.set_target(config["attention"])
        self.attention_controller.set_breathing_rate(config["breathing_cpm"])
        self.attention_controller.set_posture_lean(config["posture_lean"])

        # Special state actions
        if state == MiraVisualState.LISTENING:
            self.attention_controller.trigger_listening_nod()
        elif state == MiraVisualState.SPEAKING:
            pass
        elif state != MiraVisualState.SPEAKING:
            self.lip_sync_controller.stop()

    # --------------------------------------------------------------------------
    # High-Level Clean API Methods
    # --------------------------------------------------------------------------

    def play_greeting(self) -> None:
        """Plays welcoming clinical greeting animation."""
        self.set_state(MiraVisualState.GREETING, force=True)

    def start_listening(self) -> None:
        """Transitions into attentive active listening posture."""
        self.set_state(MiraVisualState.LISTENING)

    def start_thinking(self) -> None:
        """Transitions into clinical reasoning posture."""
        self.set_state(MiraVisualState.THINKING)

    def start_speaking(self, audio_duration_ms: int = 0) -> None:
        """Transitions into articulate medical delivery posture."""
        success = self.set_state(MiraVisualState.SPEAKING)
        if success:
            # Active speech start
            self.eye_controller.look_at_user()

    def stop_speaking(self) -> None:
        """Stops clinical speech delivery and returns to attentive listening or idle."""
        self.lip_sync_controller.stop()
        if self._current_state == MiraVisualState.SPEAKING:
            # Return to idle or attentive posture
            self.set_state(MiraVisualState.IDLE, force=True)

    def show_concern(self) -> None:
        """Escalates visual posture to clinical concern."""
        self.set_state(MiraVisualState.CONCERNED)

    def show_emergency(self) -> None:
        """Activates acute emergency crisis posture (maximum priority)."""
        self.set_state(MiraVisualState.EMERGENCY, force=True)

    def return_to_idle(self) -> None:
        """Safely returns MIRA to bedside idle readiness."""
        self.set_state(MiraVisualState.IDLE, force=True)

    def look_at_user(self) -> None:
        """Orients eye gaze directly toward user."""
        self.eye_controller.look_at_user()
        self.attention_controller.orient_to_user()

    def look_at_screen(self) -> None:
        """Orients gaze toward vitals monitor / screen."""
        self.eye_controller.look_at_screen()
        self.attention_controller.orient_to_screen()

    def look_away(self) -> None:
        """Subtly diverts gaze during reflection."""
        self.eye_controller.look_away()

    def blink(self) -> None:
        """Forces an immediate natural eyelid blink."""
        self.eye_controller.blink()

    def interrupt(self) -> None:
        """Patient barge-in: instantly stops speech and switches to active listening."""
        self.lip_sync_controller.stop()
        self.set_state(MiraVisualState.LISTENING, force=True)
        self.attention_controller.trigger_listening_nod()

    def reset(self) -> None:
        """Resets all subsystems and returns to default bedside idle."""
        self._current_state = MiraVisualState.IDLE
        self._previous_state = MiraVisualState.IDLE
        self._is_paused = False
        self.eye_controller.reset()
        self.attention_controller.reset()
        self.expression_controller.reset()
        self.lip_sync_controller.stop()
        self._apply_state_configuration(MiraVisualState.IDLE)

    def pause(self) -> None:
        """Suspends animation loop (lifecycle-aware backgrounding)."""
        self._is_paused = True

    def resume(self) -> None:
        """Resumes active animation loop."""
        self._is_paused = False

    # --------------------------------------------------------------------------
    # Frame Update Loop
    # --------------------------------------------------------------------------

    def update(self, delta_time_sec: float) -> CharacterFrameState:
        """Advances the complete character animation model by delta time."""
        if self._is_paused:
            # Return cached state without advancing timers
            return CharacterFrameState(
                state=self._current_state,
                priority=self.current_priority,
                is_paused=True,
                eye_state=self.eye_controller.update(0.0),
                attention_state=self.attention_controller.update(0.0),
                expression_weights=self.expression_controller.update(0.0),
                mouth_weights=self.lip_sync_controller.update(0.0),
                state_definition=get_state_definition(self._current_state),
            )

        # Advance all subsystem controllers
        eye_st = self.eye_controller.update(delta_time_sec)
        att_st = self.attention_controller.update(delta_time_sec)
        exp_wt = self.expression_controller.update(delta_time_sec)
        mth_wt = self.lip_sync_controller.update(delta_time_sec)

        return CharacterFrameState(
            state=self._current_state,
            priority=self.current_priority,
            is_paused=False,
            eye_state=eye_st,
            attention_state=att_st,
            expression_weights=exp_wt,
            mouth_weights=mth_wt,
            state_definition=get_state_definition(self._current_state),
        )
