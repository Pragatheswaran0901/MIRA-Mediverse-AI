"""MIRA Healthcare Tool Base Contracts.

Provides abstract tool interfaces for hospital discovery, doctor discovery,
appointment scheduling, and ambulance workflow dispatch.
Completely decoupled from any external proprietary platform.
"""

from abc import ABC, abstractmethod
from typing import Any
from pydantic import BaseModel, Field


class ToolParameterSchema(BaseModel):
    """Schema descriptor for a healthcare tool parameter."""
    name: str
    type: str
    description: str
    required: bool = True


class HealthcareToolDefinition(BaseModel):
    """Metadata describing a healthcare tool available to MIRA."""
    name: str
    description: str
    category: str
    parameters: list[ToolParameterSchema] = Field(default_factory=list)


class ToolExecutionResult(BaseModel):
    """Result payload returned by a healthcare tool."""
    tool_name: str
    success: bool
    data: dict[str, Any] = Field(default_factory=dict)
    error_message: str | None = None


class BaseHealthcareTool(ABC):
    """Abstract base class for all MIRA healthcare tools."""

    @property
    @abstractmethod
    def definition(self) -> HealthcareToolDefinition:
        """Returns metadata definition of the tool."""
        pass

    @abstractmethod
    async def execute(self, **kwargs: Any) -> ToolExecutionResult:
        """Executes the tool with supplied keyword arguments."""
        pass
