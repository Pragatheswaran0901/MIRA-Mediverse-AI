"""MIRA Character Layer Architecture.

Defines the multi-layered visual structure separating:
BACKGROUND, BODY, UNIFORM, HEAD, HAIR, FACE, EYES, EYEBROWS, MOUTH, ACCESSORIES.

Prepares the system for future multi-sprite/2.5D rigged asset separation while
safely referencing canonical MIRA_FACE_MODEL as the current unified baseline.
Strictly prohibits fake facial animation via full-image distortion.
"""

from enum import Enum
from typing import Any
from pydantic import BaseModel, ConfigDict, Field
from src.character.identity import CANONICAL_RELATIVE_PATH


class MiraCharacterLayer(str, Enum):
    """Canonical visual layers of MIRA avatar."""
    BACKGROUND = "BACKGROUND"      # Clinical or ambient backdrop (z: 0)
    BODY = "BODY"                  # Torso, shoulders, physical posture (z: 10)
    UNIFORM = "UNIFORM"            # White medical coat, lapels, scrub piping (z: 20)
    HEAD = "HEAD"                  # Cranial base, jaw contour, neck structure (z: 30)
    HAIR = "HAIR"                  # Dark parted hairstyle and low bun (z: 40)
    FACE = "FACE"                  # Skin tone, facial base, nose, cheek contours (z: 50)
    EYES = "EYES"                  # Almond dark eyes, iris, sclera, blink lids (z: 60)
    EYEBROWS = "EYEBROWS"          # Expressive brow arches (z: 70)
    MOUTH = "MOUTH"                # Lips, viseme targets, smile line (z: 80)
    ACCESSORIES = "ACCESSORIES"    # Clinical badge, ID lanyard, pendant (z: 90)


class MiraLayerConfig(BaseModel):
    """Individual layer configuration and future rigging specification."""
    model_config = ConfigDict(frozen=True)

    layer_id: MiraCharacterLayer
    name: str
    z_index: int
    asset_source: str = CANONICAL_RELATIVE_PATH
    is_canonical_fallback: bool = True
    opacity: float = Field(default=1.0, ge=0.0, le=1.0)
    blend_mode: str = "normal"
    transform_origin: str = "50% 50%"
    anchor_x: float = 0.5
    anchor_y: float = 0.5
    future_rig_type: str = "static_canonical"
    description: str = ""
    visible: bool = True
    metadata: dict[str, Any] = Field(default_factory=dict)


class MiraCharacterLayerStack(BaseModel):
    """Stack container managing the complete 10-layer visual pipeline."""
    model_config = ConfigDict(frozen=True)

    version: str = "MIRA_LAYER_STACK_v1"
    layers: list[MiraLayerConfig]

    def get_layer(self, layer_id: MiraCharacterLayer) -> MiraLayerConfig | None:
        """Finds a layer config by its enum identifier."""
        for layer in self.layers:
            if layer.layer_id == layer_id:
                return layer
        return None

    def get_ordered_layers(self) -> list[MiraLayerConfig]:
        """Returns layers sorted from back (lowest z-index) to front (highest z-index)."""
        return sorted(self.layers, key=lambda l: l.z_index)

    def to_css_layer_map(self) -> dict[str, dict[str, Any]]:
        """Exports layer stack for consumption by web components and CSS renderers."""
        return {
            layer.layer_id.value: {
                "name": layer.name,
                "zIndex": layer.z_index,
                "assetSource": layer.asset_source,
                "isCanonicalFallback": layer.is_canonical_fallback,
                "opacity": layer.opacity,
                "blendMode": layer.blend_mode,
                "transformOrigin": layer.transform_origin,
                "visible": layer.visible,
                "futureRigType": layer.future_rig_type,
            }
            for layer in self.get_ordered_layers()
        }


# Canonical default layer stack mapping all 10 layers
CANONICAL_LAYER_STACK = MiraCharacterLayerStack(
    layers=[
        MiraLayerConfig(
            layer_id=MiraCharacterLayer.BACKGROUND,
            name="Clinical Ambient Background",
            z_index=0,
            future_rig_type="backdrop_plane",
            description="Subtle clinical ambient gradient / soft hospital ward background.",
        ),
        MiraLayerConfig(
            layer_id=MiraCharacterLayer.BODY,
            name="Torso & Posture Base",
            z_index=10,
            future_rig_type="skeletal_torso",
            description="Upper torso posture anchoring subtle respiratory pacing.",
        ),
        MiraLayerConfig(
            layer_id=MiraCharacterLayer.UNIFORM,
            name="White Medical Coat & Trim",
            z_index=20,
            future_rig_type="apparel_overlay",
            description="Crisp white clinical coat with subtle pink/sandal piping.",
        ),
        MiraLayerConfig(
            layer_id=MiraCharacterLayer.HEAD,
            name="Cranial & Neck Anchor",
            z_index=30,
            future_rig_type="cranial_root",
            description="Head tilt, yaw, and nodding motion anchor node.",
        ),
        MiraLayerConfig(
            layer_id=MiraCharacterLayer.HAIR,
            name="Dark Parted Hair & Low Bun",
            z_index=40,
            future_rig_type="hair_physics_mesh",
            description="Dark parted hair framing the face with natural texture.",
        ),
        MiraLayerConfig(
            layer_id=MiraCharacterLayer.FACE,
            name="Facial Canvas & Skin Tone",
            z_index=50,
            future_rig_type="facial_base_mesh",
            description="Natural South Indian facial contours and skin tone.",
        ),
        MiraLayerConfig(
            layer_id=MiraCharacterLayer.EYES,
            name="Eyes, Iris & Blink Lids",
            z_index=60,
            future_rig_type="gaze_blink_rig",
            description="Warm dark brown almond eyes, saccade, and eyelid blink rig.",
        ),
        MiraLayerConfig(
            layer_id=MiraCharacterLayer.EYEBROWS,
            name="Expressive Eyebrows",
            z_index=70,
            future_rig_type="brow_morph_rig",
            description="Naturally arched eyebrows expressing concern, reassurance, warmth.",
        ),
        MiraLayerConfig(
            layer_id=MiraCharacterLayer.MOUTH,
            name="Mouth & Lip Visemes",
            z_index=80,
            future_rig_type="viseme_blendshape",
            description="Mouth aperture and phonetic viseme lip-sync receiver.",
        ),
        MiraLayerConfig(
            layer_id=MiraCharacterLayer.ACCESSORIES,
            name="MIRA ID Badge & Credential",
            z_index=90,
            future_rig_type="credential_badge",
            description="MIRA AI Nurse Assistant professional credential badge.",
        ),
    ]
)
