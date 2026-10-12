"""MIRA Character Identity Contract.

Defines the centralized, immutable visual identity specification for MIRA.
Anchored strictly to MIRA_FACE_MODEL as the canonical visual reference.
Prohibits runtime mutations or arbitrary redesigns.
"""

import hashlib
import os
from pathlib import Path
from typing import Any
from pydantic import BaseModel, ConfigDict, Field


CANONICAL_MODEL_NAME = "MIRA_FACE_MODEL"
CANONICAL_MODEL_VERSION = "MIRA_FACE_MODEL_v1"
CANONICAL_MODEL_SHA256 = "bf3b7cdc290d28ca7500b3d55679cbd98a397b4ec873dd86e8c910c46d1b44dc"
CANONICAL_RELATIVE_PATH = "assets/mira/identity/MIRA_FACE_MODEL.png"
CANONICAL_ROOT_PATH = "MIRA_FACE_MODEL.png"


class VisualReference(BaseModel):
    """Specification of the canonical visual reference model."""
    model_config = ConfigDict(frozen=True, populate_by_name=True)

    model_name: str = Field(default=CANONICAL_MODEL_NAME, alias="modelName")
    version: str = Field(default=CANONICAL_MODEL_VERSION)
    file_path: str = Field(default=CANONICAL_RELATIVE_PATH, alias="filePath")
    canonical_sha256: str = Field(default=CANONICAL_MODEL_SHA256, alias="canonicalSha256")
    width: int = Field(default=1536)
    height: int = Field(default=1024)
    aspect_ratio: str = Field(default="3:2", alias="aspectRatio")
    format: str = Field(default="PNG")
    is_source_of_truth: bool = Field(default=True, alias="isSourceOfTruth")


class HairProfile(BaseModel):
    """Immutable specification of MIRA's hair aesthetics."""
    model_config = ConfigDict(frozen=True, populate_by_name=True)

    style: str = "Neat professional parted hair gathered in a graceful low bun"
    color: str = "Natural deep dark brown / black"
    texture: str = "Natural healthy sheen, clinical grooming standard"
    parting: str = "Clean side part"
    highlights: str = "None (natural uniform tone)"
    accessory: str = "Discreet clinical hairpins if required, no decorative clips"


class FaceProfile(BaseModel):
    """Immutable specification of MIRA's facial geometry and features."""
    model_config = ConfigDict(frozen=True, populate_by_name=True)

    ethnicity: str = "South Asian / South Indian woman"
    structure: str = "Natural balanced oval contours, gentle jawline"
    cheekbones: str = "Subtle soft natural definition"
    expression_baseline: str = "Calm, welcoming, attentive clinical bedside warmth"
    proportions: str = "Natural human facial proportions (strictly non-stylized, non-anime)"
    aesthetic_style: str = "Professional healthcare provider (not futuristic sci-fi robot)"


class SkinProfile(BaseModel):
    """Immutable specification of MIRA's skin tone and texture."""
    model_config = ConfigDict(frozen=True, populate_by_name=True)

    tone: str = "Natural warm South Indian olive/tan complexion"
    undertone: str = "Warm golden undertone"
    texture: str = "Natural realistic skin texture, non-plastic, non-synthetic"
    finish: str = "Soft matte clinical realism"


class EyeProfile(BaseModel):
    """Immutable specification of MIRA's eye appearance and gaze."""
    model_config = ConfigDict(frozen=True, populate_by_name=True)

    color: str = "Deep warm espresso / dark brown"
    shape: str = "Almond-shaped eyes with natural gentle epicanthic contour"
    eyebrows: str = "Naturally arched, well-groomed dark brown brows"
    gaze_quality: str = "Compassionate, attentive, calm, direct bedside contact"
    eyelash_style: str = "Natural subtle lashes, professional appearance"


class UniformProfile(BaseModel):
    """Immutable specification of MIRA's healthcare attire."""
    model_config = ConfigDict(frozen=True, populate_by_name=True)

    attire_type: str = "Crisp white clinical medical coat / tailored healthcare scrubs"
    primary_color: str = "#FFFFFF (Crisp Medical White)"
    collar_style: str = "Tailored clinical collar with neat lapels"
    accents: str = "Subtle soft pink and warm sandal piping on inner trim"
    badge_label: str = "MIRA — AI Nurse Assistant"
    badge_location: str = "Left chest pocket"
    stethoscope: str = "Optional clinical accessory or digital diagnostic pendant"


class ColorPalette(BaseModel):
    """MIRA visual color system tokens."""
    model_config = ConfigDict(frozen=True, populate_by_name=True)

    medical_white: str = "#FFFFFF"
    clean_surface: str = "#F8FAFC"
    clinical_teal: str = "#0D9488"
    clinical_teal_dark: str = "#0F766E"
    accent_pink: str = "#F472B6"
    accent_pink_soft: str = "#FBCFE8"
    accent_sandal: str = "#E2C799"
    accent_sandal_light: str = "#F5EBE0"
    clinical_slate: str = "#0F172A"
    text_primary: str = "#1E293B"
    text_muted: str = "#64748B"
    emergency_crimson: str = "#DC2626"
    warning_amber: str = "#F59E0B"


class BrandingConfig(BaseModel):
    """MIRA product and visual branding attributes."""
    model_config = ConfigDict(frozen=True, populate_by_name=True)

    name: str = "MIRA"
    full_name: str = "Medical Intelligent Response Assistant"
    role: str = "Autonomous AI Healthcare Companion & AI Nurse Assistant"
    badge: str = "RN / AI NURSE ASSISTANT"
    brand_identity_anchor: str = "MIRA_FACE_MODEL"
    canonical_tagline: str = "Compassionate Clinical Intelligence"


class MiraCharacterIdentity(BaseModel):
    """Centralized MIRA Character Configuration Contract.
    
    Serves as the definitive identity anchor for all visual assets and renderers.
    Strictly frozen to prevent runtime mutation or unauthorized visual changes.
    """
    model_config = ConfigDict(frozen=True, populate_by_name=True)

    name: str = Field(default="MIRA")
    character_version: str = Field(default=CANONICAL_MODEL_VERSION, alias="characterVersion")
    visual_reference: VisualReference = Field(
        default_factory=VisualReference, alias="visualReference"
    )
    hair_style: HairProfile = Field(default_factory=HairProfile, alias="hairStyle")
    face_profile: FaceProfile = Field(default_factory=FaceProfile, alias="faceProfile")
    skin_profile: SkinProfile = Field(default_factory=SkinProfile, alias="skinProfile")
    eye_profile: EyeProfile = Field(default_factory=EyeProfile, alias="eyeProfile")
    uniform_profile: UniformProfile = Field(
        default_factory=UniformProfile, alias="uniformProfile"
    )
    color_palette: ColorPalette = Field(default_factory=ColorPalette, alias="colorPalette")
    branding: BrandingConfig = Field(default_factory=BrandingConfig)

    def verify_asset_integrity(self, base_dir: str | Path | None = None) -> bool:
        """Verifies that the canonical asset exists on disk and its SHA256 checksum matches."""
        target_path = Path(self.visual_reference.file_path)
        if base_dir:
            target_path = Path(base_dir) / target_path

        if not target_path.exists():
            # Check fallback root location
            root_fallback = Path(CANONICAL_ROOT_PATH)
            if base_dir:
                root_fallback = Path(base_dir) / root_fallback
            if not root_fallback.exists():
                return False
            target_path = root_fallback

        try:
            with open(target_path, "rb") as f:
                content = f.read()
            computed_sha256 = hashlib.sha256(content).hexdigest()
            return computed_sha256 == self.visual_reference.canonical_sha256
        except Exception:
            return False


# Singleton instance of the canonical character identity contract
MIRA_CHARACTER_IDENTITY = MiraCharacterIdentity()
