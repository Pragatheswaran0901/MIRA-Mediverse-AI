"""MIRA Character Subsystem Package.

Provides character asset foundation, identity anchors, multi-layer rendering stack,
canonical visual states, animation readiness contracts, and interactive character animation foundation:
- MiraAnimationController (State engine, priority hierarchy, interruption handling)
- MiraEyeController (Organic blinking, gaze targets, micro-saccades)
- MiraAttentionController (Head orientation, clinical respiratory rhythm, attentive nods)
- MiraExpressionController (FACS blendshape morph weights, clinical facial expressions)
- MiraLipSyncController (Viseme mapping, phonetic mouth shapes, acoustic cadence)
- MiraEventBus (Decoupled event pub/sub for conversation, safety, and voice integration)
- MiraCharacter (Reusable component)
"""

from src.character.animation_hooks import (
    ANIMATION_CAPABILITY_ARCHITECTURE,
    MiraAnimationCapabilityArchitecture,
)
from src.character.attention_controller import (
    TARGET_HEAD_COORDINATES,
    AttentionState,
    AttentionTarget,
    MiraAttentionController,
)
from src.character.component import (
    CharacterSize,
    MiraCharacter,
    MiraCharacterProps,
)
from src.character.controller import (
    STATE_PRIORITIES,
    STATE_SUBSYSTEM_MAPPINGS,
    CharacterFrameState,
    MiraAnimationController,
)
from src.character.events import (
    MiraEvent,
    MiraEventBus,
    MiraEventPayload,
)
from src.character.expression_controller import (
    CANONICAL_EXPRESSION_PRESETS,
    ExpressionMorphWeights,
    FacialExpressionId,
    MiraExpressionController,
)
from src.character.expressions import (
    CharacterExpression,
    CharacterReaction,
    map_urgency_to_expression,
)
from src.character.eye_controller import (
    TARGET_GAZE_COORDINATES,
    EyeState,
    GazeTarget,
    MiraEyeController,
)
from src.character.identity import (
    CANONICAL_MODEL_NAME,
    CANONICAL_MODEL_SHA256,
    CANONICAL_MODEL_VERSION,
    CANONICAL_RELATIVE_PATH,
    MIRA_CHARACTER_IDENTITY,
    BrandingConfig,
    ColorPalette,
    EyeProfile,
    FaceProfile,
    HairProfile,
    MiraCharacterIdentity,
    SkinProfile,
    UniformProfile,
    VisualReference,
)
from src.character.layers import (
    CANONICAL_LAYER_STACK,
    MiraCharacterLayer,
    MiraCharacterLayerStack,
    MiraLayerConfig,
)
from src.character.lip_sync import (
    LipSyncTrack,
    VisemeFrame,
    VisemeId,
)
from src.character.lip_sync_controller import (
    VISEME_MORPH_TARGETS,
    MouthShapeWeights,
    MiraLipSyncController,
)
from src.character.states import (
    CHARACTER_STATE_REGISTRY,
    MiraStateDefinition,
    MiraVisualState,
    get_all_states,
    get_state_definition,
)

__all__ = [
    # Canonical Identity
    "CANONICAL_MODEL_NAME",
    "CANONICAL_MODEL_VERSION",
    "CANONICAL_MODEL_SHA256",
    "CANONICAL_RELATIVE_PATH",
    "MIRA_CHARACTER_IDENTITY",
    "MiraCharacterIdentity",
    "VisualReference",
    "HairProfile",
    "FaceProfile",
    "SkinProfile",
    "EyeProfile",
    "UniformProfile",
    "ColorPalette",
    "BrandingConfig",
    # Visual States
    "MiraVisualState",
    "MiraStateDefinition",
    "CHARACTER_STATE_REGISTRY",
    "get_state_definition",
    "get_all_states",
    # Layer Architecture
    "MiraCharacterLayer",
    "MiraLayerConfig",
    "MiraCharacterLayerStack",
    "CANONICAL_LAYER_STACK",
    # Reusable Component
    "CharacterSize",
    "MiraCharacterProps",
    "MiraCharacter",
    # Animation Controller Engine (Block 3)
    "MiraAnimationController",
    "CharacterFrameState",
    "STATE_PRIORITIES",
    "STATE_SUBSYSTEM_MAPPINGS",
    # Eye Subsystem
    "MiraEyeController",
    "EyeState",
    "GazeTarget",
    "TARGET_GAZE_COORDINATES",
    # Attention Subsystem
    "MiraAttentionController",
    "AttentionState",
    "AttentionTarget",
    "TARGET_HEAD_COORDINATES",
    # Facial Expression Subsystem
    "MiraExpressionController",
    "FacialExpressionId",
    "ExpressionMorphWeights",
    "CANONICAL_EXPRESSION_PRESETS",
    # Lip Sync Subsystem
    "MiraLipSyncController",
    "MouthShapeWeights",
    "VISEME_MORPH_TARGETS",
    # Event Bus
    "MiraEvent",
    "MiraEventPayload",
    "MiraEventBus",
    # Future Animation Hooks & Compatibility
    "MiraAnimationCapabilityArchitecture",
    "ANIMATION_CAPABILITY_ARCHITECTURE",
    # Foundational Schemas
    "CharacterExpression",
    "CharacterReaction",
    "map_urgency_to_expression",
    "VisemeId",
    "VisemeFrame",
    "LipSyncTrack",
]
