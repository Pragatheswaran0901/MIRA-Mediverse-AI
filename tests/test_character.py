"""Comprehensive tests for MIRA Character Asset Foundation (Block 2).

Verifies:
1. Canonical identity contract immutability and visual reference anchor.
2. Asset pipeline checksum verification for MIRA_FACE_MODEL.png.
3. Complete 13-state data-driven visual system.
4. Multi-layer architecture (10 layers) with proper z-indices.
5. Reusable MiraCharacter component props contract and strict rejection of AI logic.
6. Dormant future animation capability hooks.
7. Character API endpoints and static asset serving.
"""

from pathlib import Path
import pytest
from httpx import ASGITransport, AsyncClient
from pydantic import ValidationError
from src.api.app import create_app
from src.character import (
    ANIMATION_CAPABILITY_ARCHITECTURE,
    CANONICAL_LAYER_STACK,
    CANONICAL_MODEL_NAME,
    CANONICAL_MODEL_SHA256,
    CANONICAL_MODEL_VERSION,
    CHARACTER_STATE_REGISTRY,
    MIRA_CHARACTER_IDENTITY,
    CharacterSize,
    MiraCharacter,
    MiraCharacterIdentity,
    MiraCharacterLayer,
    MiraCharacterProps,
    MiraVisualState,
    get_all_states,
    get_state_definition,
)


@pytest.fixture
def app():
    """FastAPI test app fixture."""
    return create_app()


def test_character_identity_canonical_anchor():
    """Verifies that MIRA_CHARACTER_IDENTITY is anchored strictly to MIRA_FACE_MODEL."""
    identity = MIRA_CHARACTER_IDENTITY
    assert identity.name == "MIRA"
    assert identity.character_version == CANONICAL_MODEL_VERSION
    assert identity.visual_reference.model_name == CANONICAL_MODEL_NAME
    assert identity.visual_reference.canonical_sha256 == CANONICAL_MODEL_SHA256
    assert identity.visual_reference.width == 1536
    assert identity.visual_reference.height == 1024
    assert identity.visual_reference.aspect_ratio == "3:2"

    # Verify visual identity traits
    assert "South Indian" in identity.face_profile.ethnicity
    assert "low bun" in identity.hair_style.style
    assert "olive" in identity.skin_profile.tone or "tan" in identity.skin_profile.tone
    assert "espresso" in identity.eye_profile.color or "dark brown" in identity.eye_profile.color
    assert "white" in identity.uniform_profile.attire_type.lower()
    assert "#FFFFFF" in identity.color_palette.medical_white


def test_character_identity_is_strictly_immutable():
    """Verifies that identity contract cannot be mutated at runtime."""
    with pytest.raises(ValidationError):
        MIRA_CHARACTER_IDENTITY.name = "DifferentName"  # type: ignore

    with pytest.raises(ValidationError):
        MIRA_CHARACTER_IDENTITY.character_version = "MODIFIED_v2"  # type: ignore


def test_canonical_asset_integrity_on_disk():
    """Verifies that MIRA_FACE_MODEL exists on disk and its SHA256 checksum matches."""
    assert MIRA_CHARACTER_IDENTITY.verify_asset_integrity() is True

    # Test file directly in assets/mira/identity/
    canonical_file = Path("assets/mira/identity/MIRA_FACE_MODEL.png")
    assert canonical_file.exists()
    assert canonical_file.stat().st_size > 1000000  # ~2.6MB


def test_all_thirteen_visual_states_exist():
    """Verifies that all 13 canonical states are registered with complete metadata."""
    expected_states = {
        MiraVisualState.IDLE,
        MiraVisualState.GREETING,
        MiraVisualState.LISTENING,
        MiraVisualState.THINKING,
        MiraVisualState.SPEAKING,
        MiraVisualState.FRIENDLY,
        MiraVisualState.CONCERNED,
        MiraVisualState.SERIOUS,
        MiraVisualState.REASSURING,
        MiraVisualState.EMERGENCY,
        MiraVisualState.ESCALATING,
        MiraVisualState.CALMING,
        MiraVisualState.COMPLETED,
    }
    registered_keys = set(CHARACTER_STATE_REGISTRY.keys())
    assert registered_keys == expected_states
    assert len(get_all_states()) == 13

    # Check key state properties
    idle = get_state_definition(MiraVisualState.IDLE)
    assert idle.display_name == "Bedside Idle"
    assert idle.accent_color.startswith("#")

    emergency = get_state_definition(MiraVisualState.EMERGENCY)
    assert emergency.display_name == "Emergency Escalation"
    assert emergency.accent_color == "#DC2626"


def test_state_transitions_preserve_character():
    """Verifies that transitioning character states does not break or clear character identity."""
    char = MiraCharacter(state=MiraVisualState.IDLE)
    assert char.current_state == MiraVisualState.IDLE

    # Transition through multiple states
    char.set_state(MiraVisualState.LISTENING)
    assert char.current_state == MiraVisualState.LISTENING
    assert char.props.canonical_reference == CANONICAL_MODEL_SHA256

    char.set_state("EMERGENCY")
    assert char.current_state == MiraVisualState.EMERGENCY
    assert char.props.canonical_reference == CANONICAL_MODEL_SHA256

    # Verify HTML snippet renders without disappearing
    snippet = char.render_html_snippet()
    assert "state=\"EMERGENCY\"" in snippet
    assert "mira-character" in snippet


def test_character_layers_stack_architecture():
    """Verifies the 10-layer visual architecture and strictly ordered z-indices."""
    layers = CANONICAL_LAYER_STACK.get_ordered_layers()
    assert len(layers) == 10

    layer_ids = [l.layer_id for l in layers]
    expected_order = [
        MiraCharacterLayer.BACKGROUND,
        MiraCharacterLayer.BODY,
        MiraCharacterLayer.UNIFORM,
        MiraCharacterLayer.HEAD,
        MiraCharacterLayer.HAIR,
        MiraCharacterLayer.FACE,
        MiraCharacterLayer.EYES,
        MiraCharacterLayer.EYEBROWS,
        MiraCharacterLayer.MOUTH,
        MiraCharacterLayer.ACCESSORIES,
    ]
    assert layer_ids == expected_order

    # Verify z-index monotonic increase
    z_indices = [l.z_index for l in layers]
    assert z_indices == sorted(z_indices)
    assert len(set(z_indices)) == 10  # All unique


def test_character_component_rejects_ai_logic():
    """ARCHITECTURAL INVARIANT: Rejects injection of AI logic or LLM payloads into character component."""
    # Valid props succeed
    props = MiraCharacterProps(state=MiraVisualState.IDLE, size=CharacterSize.RESPONSIVE)
    assert props.state == MiraVisualState.IDLE

    # Passing forbidden AI logic parameters raises ValidationError
    with pytest.raises(ValidationError):
        MiraCharacterProps.model_validate({"llm_prompt": "Diagnose the patient"})

    with pytest.raises(ValidationError):
        MiraCharacterProps.model_validate({"rag_context": "Medical guidelines for flu"})

    with pytest.raises(ValidationError):
        MiraCharacterProps.model_validate({"triage_reasoning": "Severe chest pain"})


def test_future_animation_hooks_dormant_in_block_2():
    """Verifies that all 13 future animation hooks are structured and dormant (disabled)."""
    arch = ANIMATION_CAPABILITY_ARCHITECTURE
    assert arch.is_dormant_in_block_2 is True
    assert arch.blinking.enabled is False
    assert arch.eye_movement.enabled is False
    assert arch.eye_direction.enabled is False
    assert arch.subtle_breathing.enabled is False
    assert arch.head_movement.enabled is False
    assert arch.facial_expressions.enabled is False
    assert arch.mouth_movement.enabled is False
    assert arch.lip_sync.enabled is False
    assert arch.speaking_animation.enabled is False
    assert arch.listening_animation.enabled is False
    assert arch.emotional_reactions.enabled is False
    assert arch.interruption.enabled is False
    assert arch.attention_direction.enabled is False


@pytest.mark.asyncio
async def test_character_api_identity_endpoint(app):
    """Verifies GET /api/v1/character/identity."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/api/v1/character/identity")
        assert res.status_code == 200
        data = res.json()
        assert data["name"] == "MIRA"
        assert data["characterVersion"] == CANONICAL_MODEL_VERSION
        assert data["visualReference"]["canonicalSha256"] == CANONICAL_MODEL_SHA256


@pytest.mark.asyncio
async def test_character_api_states_endpoint(app):
    """Verifies GET /api/v1/character/states returns all 13 states."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/api/v1/character/states")
        assert res.status_code == 200
        states = res.json()
        assert len(states) == 13
        state_names = {s["state"] for s in states}
        assert "IDLE" in state_names
        assert "EMERGENCY" in state_names
        assert "GREETING" in state_names


@pytest.mark.asyncio
async def test_character_api_layers_endpoint(app):
    """Verifies GET /api/v1/character/layers returns all 10 layers."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/api/v1/character/layers")
        assert res.status_code == 200
        data = res.json()
        assert len(data["layers"]) == 10


@pytest.mark.asyncio
async def test_character_api_verify_reference_endpoint(app):
    """Verifies GET /api/v1/character/verify-reference returns valid status."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/api/v1/character/verify-reference")
        assert res.status_code == 200
        data = res.json()
        assert data["is_valid"] is True
        assert data["status"] == "CANONICAL_ANCHOR_VERIFIED"


@pytest.mark.asyncio
async def test_character_static_assets_served(app):
    """Verifies static files and character viewer are served properly."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Check canonical asset served
        img_res = await client.get("/assets/mira/identity/MIRA_FACE_MODEL.png")
        assert img_res.status_code == 200
        assert img_res.headers["content-type"] == "image/png"

        # Check web component JS
        js_res = await client.get("/character-ui/mira-character.js")
        assert js_res.status_code == 200
        assert "mira-character" in js_res.text

        # Check web component CSS
        css_res = await client.get("/character-ui/mira-character.css")
        assert css_res.status_code == 200
        assert "mira-portrait-canvas" in css_res.text

        # Check viewer HTML console
        viewer_res = await client.get("/character")
        assert viewer_res.status_code == 200
        assert "MIRA_FACE_MODEL" in viewer_res.text
