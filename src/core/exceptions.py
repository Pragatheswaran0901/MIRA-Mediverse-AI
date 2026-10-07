"""MIRA Core Domain Exceptions."""


class MiraBaseException(Exception):
    """Base exception for all MIRA runtime errors."""
    def __init__(self, message: str, details: dict | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}


class SafetyViolationException(MiraBaseException):
    """Raised when an action or generated text violates safety policy."""
    pass


class HumanClaimForbiddenException(SafetyViolationException):
    """Raised when an output falsely claims MIRA is a human."""
    pass


class ProfessionalReplacementException(SafetyViolationException):
    """Raised when an output falsely claims to replace licensed doctors or nurses."""
    pass


class TriageEscalationRequired(MiraBaseException):
    """Raised when clinical red flags demand immediate emergency intervention."""
    def __init__(self, red_flags: list[str], guidance: str) -> None:
        super().__init__(
            f"Emergency escalation triggered due to critical red flags: {', '.join(red_flags)}",
            {"red_flags": red_flags, "guidance": guidance},
        )
        self.red_flags = red_flags
        self.guidance = guidance
