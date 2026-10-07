"""Tests for MIRA personality traits, tone adaptation, and prompt engineering."""

from src.core.contracts import UrgencyLevel
from src.brain.personality import (
    PERSONALITY_TRAITS,
    generate_system_prompt,
    MIRA_BASE_SYSTEM_PROMPT,
)


def test_personality_traits_attributes():
    """Verifies that all required personality traits are codified."""
    assert "companion" in PERSONALITY_TRAITS.companion_style.lower()
    assert "nurse" in PERSONALITY_TRAITS.clinical_care.lower()
    assert "ai" in PERSONALITY_TRAITS.intellect.lower()
    assert "calm" in PERSONALITY_TRAITS.temperament.lower()
    assert "warm" in PERSONALITY_TRAITS.communication_normal.lower()
    assert "concise" in PERSONALITY_TRAITS.communication_urgent.lower()
    assert "serious" in PERSONALITY_TRAITS.communication_emergency.lower()
    assert "judgmental" in PERSONALITY_TRAITS.non_judgmental.lower()


def test_base_system_prompt_identity_mandate():
    """Verifies that the base system prompt contains strict identity mandates."""
    assert "NEVER claim to be a human" in MIRA_BASE_SYSTEM_PROMPT
    assert "NEVER claim to replace doctors" in MIRA_BASE_SYSTEM_PROMPT
    assert "I'm MIRA, an AI healthcare assistant." in MIRA_BASE_SYSTEM_PROMPT


def test_generate_system_prompt_emergency_adaptation():
    """Verifies prompt tone dynamically switches to serious and concise during emergencies."""
    prompt = generate_system_prompt(UrgencyLevel.EMERGENCY)
    assert "[EMERGENCY PROTOCOL ACTIVE]" in prompt
    assert "SERIOUS and CONCISE" in prompt
    assert "Drop conversational chit-chat" in prompt


def test_generate_system_prompt_standard_adaptation():
    """Verifies prompt tone is warm and caring during standard interactions."""
    prompt = generate_system_prompt(UrgencyLevel.INFORMATIONAL)
    assert "[STANDARD HEALTHCARE CONVERSATION]" in prompt
    assert "WARM, CARING, and FRIENDLY" in prompt
