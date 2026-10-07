"""MIRA Safety & Triage Verification Route.

Allows clients and test suites to verify candidate text compliance
and evaluate patient symptom severity.
"""

from fastapi import APIRouter
from pydantic import BaseModel, Field
from src.safety.rules import (
    verify_ai_identity_compliance,
    verify_non_replacement_compliance,
)
from src.safety.triage import evaluate_triage_level, TriageAssessment
from src.core.exceptions import (
    HumanClaimForbiddenException,
    ProfessionalReplacementException,
)

router = APIRouter(prefix="/api/v1", tags=["Safety Verification"])


class TextSafetyCheckRequest(BaseModel):
    """Payload to audit for safety invariant breaches."""
    text: str = Field(..., description="Candidate generated text to verify")


class TextSafetyCheckResponse(BaseModel):
    """Audit result for candidate generated text."""
    is_safe: bool
    violations: list[str] = Field(default_factory=list)


class TriageEvaluationRequest(BaseModel):
    """Payload to evaluate patient symptoms."""
    symptoms_text: str = Field(..., description="Patient reported symptoms")


@router.post("/verify-safety", response_model=TextSafetyCheckResponse)
async def verify_text_safety(payload: TextSafetyCheckRequest) -> TextSafetyCheckResponse:
    """Verifies candidate response text against MIRA safety policies."""
    violations: list[str] = []
    
    try:
        verify_ai_identity_compliance(payload.text)
    except HumanClaimForbiddenException as e:
        violations.append(str(e))

    try:
        verify_non_replacement_compliance(payload.text)
    except ProfessionalReplacementException as e:
        violations.append(str(e))

    return TextSafetyCheckResponse(
        is_safe=len(violations) == 0,
        violations=violations,
    )


@router.post("/triage-evaluate", response_model=TriageAssessment)
async def evaluate_triage(payload: TriageEvaluationRequest) -> TriageAssessment:
    """Classifies symptom input into clinical triage urgency category."""
    return evaluate_triage_level(payload.symptoms_text)
