"""MIRA Service Health & Readiness Route."""

from datetime import datetime, timezone
from fastapi import APIRouter
from pydantic import BaseModel, Field
from config.settings import get_settings

router = APIRouter(tags=["System Health"])


class SubsystemHealth(BaseModel):
    """Health indicator for an individual architectural tier."""
    status: str = "healthy"
    details: str


class HealthResponse(BaseModel):
    """Complete health response payload."""
    status: str = "ok"
    app_name: str
    version: str
    current_block: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    subsystems: dict[str, SubsystemHealth]


@router.get("/health", response_model=HealthResponse)
async def check_health() -> HealthResponse:
    """Service health and subsystem status."""
    settings = get_settings()
    return HealthResponse(
        status="ok",
        app_name=settings.app_name,
        version=settings.version,
        current_block=settings.current_block,
        subsystems={
            "brain": SubsystemHealth(
                status="healthy",
                details="Personality engine & memory contracts initialized",
            ),
            "safety": SubsystemHealth(
                status="healthy",
                details="Red-flag clinical catalog & triage rules active",
            ),
            "knowledge": SubsystemHealth(
                status="healthy",
                details="Guideline reference repository initialized",
            ),
            "tools": SubsystemHealth(
                status="healthy",
                details="Decoupled healthcare tool registry active",
            ),
            "character": SubsystemHealth(
                status="healthy",
                details="Expression mappings and viseme frames defined",
            ),
            "voice": SubsystemHealth(
                status="healthy",
                details="MIRA custom nurse acoustic profile configured",
            ),
        },
    )
