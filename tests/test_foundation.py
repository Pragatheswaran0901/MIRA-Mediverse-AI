"""Foundation tests for MIRA project configuration and identity contracts."""

import pytest
from pydantic import ValidationError
from config.settings import get_settings
from src.core.contracts import PRODUCT_IDENTITY, ProductIdentity, UrgencyLevel


def test_settings_load_defaults():
    """Verifies that settings load properly with foundational defaults."""
    settings = get_settings()
    assert settings.app_name == "MIRA"
    assert settings.app_full_name == "Medical Intelligent Response Assistant"
    assert "Block 1" in settings.current_block
    assert settings.strict_safety_mode is True
    assert settings.emergency_escalation_enabled is True


def test_product_identity_is_strictly_non_human():
    """Verifies that MIRA is explicitly defined as non-human and non-replacement."""
    identity = PRODUCT_IDENTITY
    assert identity.name == "MIRA"
    assert identity.is_human is False
    assert identity.replaces_professionals is False
    assert identity.get_canonical_introduction() == "I'm MIRA, an AI healthcare assistant."


def test_product_identity_is_immutable():
    """Verifies that ProductIdentity attributes cannot be mutated at runtime."""
    with pytest.raises(ValidationError):
        PRODUCT_IDENTITY.is_human = True  # type: ignore

    with pytest.raises(ValidationError):
        PRODUCT_IDENTITY.replaces_professionals = True  # type: ignore


def test_urgency_levels():
    """Verifies all four clinical triage urgency tiers exist."""
    assert UrgencyLevel.EMERGENCY == "emergency"
    assert UrgencyLevel.URGENT == "urgent"
    assert UrgencyLevel.ROUTINE == "routine"
    assert UrgencyLevel.INFORMATIONAL == "informational"
