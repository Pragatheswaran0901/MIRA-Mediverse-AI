"""MIRA Reusable Character Component Contract.

Defines the configuration, validation rules, and structural contracts for the
reusable MiraCharacter component.

ARCHITECTURAL MANDATE:
The character component handles rendering, visual state, and layer presentation only.
AI reasoning, LLM orchestration, RAG retrieval, and clinical triage logic are STRICTLY
prohibited inside this component.
"""

from enum import Enum
from typing import Any, Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator
from src.character.identity import CANONICAL_RELATIVE_PATH, MIRA_CHARACTER_IDENTITY
from src.character.layers import CANONICAL_LAYER_STACK, MiraCharacterLayerStack
from src.character.states import MiraVisualState, get_state_definition


class CharacterSize(str, Enum):
    """Preset sizes for MIRA character component."""
    SM = "sm"                  # Compact widget (240px wide)
    MD = "md"                  # Standard card/bedside panel (400px wide)
    LG = "lg"                  # Prominent companion display (560px wide)
    XL = "xl"                  # Immersive workstation (720px wide)
    RESPONSIVE = "responsive"  # Fluidly adapts to parent container width


# Forbidden AI keywords to enforce strict separation of AI logic from character rendering
FORBIDDEN_AI_KEYS = {
    "llm",
    "prompt",
    "system_prompt",
    "rag",
    "retrieval",
    "triage_reasoning",
    "clinical_knowledge",
    "medical_knowledge",
    "vector_store",
    "ai_brain",
    "memory_context",
    "token_usage",
}


class MiraCharacterProps(BaseModel):
    """Props contract for the reusable MiraCharacter component."""
    model_config = ConfigDict(populate_by_name=True)

    state: MiraVisualState = Field(default=MiraVisualState.IDLE)
    size: CharacterSize = Field(default=CharacterSize.RESPONSIVE)
    visibility: bool = Field(default=True)
    interaction_enabled: bool = Field(default=True, alias="interactionEnabled")
    animation_enabled: bool = Field(default=False, alias="animationEnabled")
    expression_state: str = Field(default="calm", alias="expressionState")
    canonical_reference: str = Field(
        default=MIRA_CHARACTER_IDENTITY.visual_reference.canonical_sha256,
        alias="canonicalReference",
    )
    asset_path: str = Field(default=CANONICAL_RELATIVE_PATH, alias="assetPath")
    custom_class: str = Field(default="", alias="customClass")

    @model_validator(mode="before")
    @classmethod
    def reject_ai_logic(cls, data: Any) -> Any:
        """Enforces that no AI reasoning or LLM payloads are injected into character component."""
        if isinstance(data, dict):
            for k in data.keys():
                lowered = k.lower()
                for forbidden in FORBIDDEN_AI_KEYS:
                    if forbidden in lowered:
                        raise ValueError(
                            f"Architectural Violation: Character component cannot contain AI logic "
                            f"or reasoning payloads. Detected forbidden key: '{k}'."
                        )
        return data

    def to_client_props(self) -> dict[str, Any]:
        """Returns JSON-serializable dictionary for Web Component consumption."""
        state_def = get_state_definition(self.state)
        return {
            "state": self.state.value,
            "stateName": state_def.display_name,
            "clinicalIntent": state_def.clinical_intent,
            "accentColor": state_def.accent_color,
            "size": self.size.value,
            "visibility": self.visibility,
            "interactionEnabled": self.interaction_enabled,
            "animationEnabled": self.animation_enabled,
            "expressionState": self.expression_state,
            "assetPath": f"/{self.asset_path}".replace("\\", "/"),
            "characterVersion": MIRA_CHARACTER_IDENTITY.character_version,
            "layers": CANONICAL_LAYER_STACK.to_css_layer_map(),
        }


class MiraCharacter:
    """Python wrapper and renderer descriptor for the reusable MIRA character."""

    def __init__(
        self,
        state: MiraVisualState = MiraVisualState.IDLE,
        size: CharacterSize = CharacterSize.RESPONSIVE,
        visibility: bool = True,
        interaction_enabled: bool = True,
        animation_enabled: bool = False,
        expression_state: str = "calm",
        layer_stack: MiraCharacterLayerStack = CANONICAL_LAYER_STACK,
    ) -> None:
        self.props = MiraCharacterProps(
            state=state,
            size=size,
            visibility=visibility,
            interactionEnabled=interaction_enabled,
            animationEnabled=animation_enabled,
            expressionState=expression_state,
        )
        self.layer_stack = layer_stack
        from src.character.controller import MiraAnimationController
        self.controller = MiraAnimationController(initial_state=state)

    @property
    def current_state(self) -> MiraVisualState:
        return self.controller.current_state

    def set_state(self, new_state: MiraVisualState | str, force: bool = True) -> bool:
        """Updates character visual state via animation controller."""
        if isinstance(new_state, str):
            new_state = MiraVisualState(new_state.upper())
        success = self.controller.set_state(new_state, force=force)
        self.props.state = self.controller.current_state
        return success

    def start_listening(self) -> None:
        """Transitions into active listening posture."""
        self.controller.start_listening()
        self.props.state = self.controller.current_state

    def start_thinking(self) -> None:
        """Transitions into clinical reasoning posture."""
        self.controller.start_thinking()
        self.props.state = self.controller.current_state

    def start_speaking(self) -> None:
        """Transitions into clinical delivery posture."""
        self.controller.start_speaking()
        self.props.state = self.controller.current_state

    def stop_speaking(self) -> None:
        """Halts speaking and returns to idle/attentive."""
        self.controller.stop_speaking()
        self.props.state = self.controller.current_state

    def show_concern(self) -> None:
        """Escalates visual posture to clinical concern."""
        self.controller.show_concern()
        self.props.state = self.controller.current_state

    def show_emergency(self) -> None:
        """Escalates to acute emergency crisis posture."""
        self.controller.show_emergency()
        self.props.state = self.controller.current_state

    def return_to_idle(self) -> None:
        """Safely returns MIRA to bedside idle readiness."""
        self.controller.return_to_idle()
        self.props.state = self.controller.current_state

    def interrupt(self) -> None:
        """Executes instant patient barge-in interruption."""
        self.controller.interrupt()
        self.props.state = self.controller.current_state

    def reset(self) -> None:
        """Resets all subsystems to neutral baseline."""
        self.controller.reset()
        self.props.state = self.controller.current_state

    def render_html_snippet(self, element_id: str = "mira-character-main") -> str:
        """Produces declarative HTML tag consuming the Web Component."""
        p = self.props.to_client_props()
        return (
            f'<mira-character '
            f'id="{element_id}" '
            f'state="{self.current_state.value}" '
            f'size="{p["size"]}" '
            f'visibility="{"true" if p["visibility"] else "false"}" '
            f'interaction-enabled="{"true" if p["interactionEnabled"] else "false"}" '
            f'animation-enabled="{"true" if p["animationEnabled"] else "false"}" '
            f'expression-state="{p["expressionState"]}">'
            f'</mira-character>'
        )

