"""Tests for MIRA safety guardrails, red-flag detection, and clinical triage."""

import pytest
from src.core.contracts import UrgencyLevel
from src.core.exceptions import HumanClaimForbiddenException, ProfessionalReplacementException
from src.safety.rules import (
    verify_ai_identity_compliance,
    verify_non_replacement_compliance,
    validate_safety_constraints,
)
from src.safety.red_flags import detect_red_flags
from src.safety.triage import evaluate_triage_level


def test_ai_identity_compliance_allows_truthful_statement():
    """Validates that legitimate AI statements pass safety inspection."""
    safe_text = "I'm MIRA, an AI healthcare assistant. How can I help you today?"
    assert validate_safety_constraints(safe_text) is True


@pytest.mark.parametrize(
    "forbidden_text",
    [
        "I'm your human nurse today.",
        "I am a real living person and doctor.",
        "I am not an AI, you can trust me.",
        "As a human nurse, I will check your chart.",
    ],
)
def test_ai_identity_compliance_rejects_human_claims(forbidden_text: str):
    """Verifies that claiming to be human triggers HumanClaimForbiddenException."""
    with pytest.raises(HumanClaimForbiddenException):
        verify_ai_identity_compliance(forbidden_text)


@pytest.mark.parametrize(
    "forbidden_text",
    [
        "I can replace your doctor completely.",
        "You don't need to see a doctor ever again.",
        "No need to consult a real doctor, I am all the medical care you need.",
        "Don't call 911, let me treat you instead.",
    ],
)
def test_non_replacement_compliance_rejects_doctor_replacement(forbidden_text: str):
    """Verifies that claiming to replace physicians triggers ProfessionalReplacementException."""
    with pytest.raises(ProfessionalReplacementException):
        verify_non_replacement_compliance(forbidden_text)


def test_red_flag_detection_identifies_cardiac_emergency():
    """Verifies that crushing chest pain is immediately flagged."""
    symptoms = "The patient has crushing chest pain radiating to left arm and neck."
    detected = detect_red_flags(symptoms)
    assert len(detected) > 0
    assert any("Chest Pain" in rf.label for rf in detected)


def test_red_flag_detection_identifies_stroke():
    """Verifies FAST acute stroke symptoms are flagged."""
    symptoms = "My mother has sudden face drooping and slurred speech."
    detected = detect_red_flags(symptoms)
    assert len(detected) > 0
    assert any("Stroke" in rf.label for rf in detected)


def test_triage_evaluation_escalates_emergency():
    """Verifies triage system assigns EMERGENCY urgency to red flags."""
    assessment = evaluate_triage_level("I have crushing chest pain and cannot breathe")
    assert assessment.urgency == UrgencyLevel.EMERGENCY
    assert assessment.requires_emergency_dispatch is True
    assert "emergency" in assessment.action_recommendation.lower()


def test_triage_evaluation_assigns_urgent():
    """Verifies high fever and suspected fractures trigger URGENT urgency."""
    assessment = evaluate_triage_level("My child has a high fever and persistent vomiting")
    assert assessment.urgency == UrgencyLevel.URGENT
    assert assessment.requires_emergency_dispatch is False


def test_triage_evaluation_assigns_routine():
    """Verifies mild cold symptoms are assigned ROUTINE urgency."""
    assessment = evaluate_triage_level("I have a mild cough and a running nose")
    assert assessment.urgency == UrgencyLevel.ROUTINE
    assert assessment.requires_emergency_dispatch is False


def test_triage_evaluation_assigns_informational():
    """Verifies general inquiries are marked INFORMATIONAL."""
    assessment = evaluate_triage_level("How many glasses of water should I drink daily?")
    assert assessment.urgency == UrgencyLevel.INFORMATIONAL
    assert assessment.requires_emergency_dispatch is False
