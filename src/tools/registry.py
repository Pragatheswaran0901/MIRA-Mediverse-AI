"""MIRA Healthcare Tool Registry.

Manages registration, discovery, and execution of healthcare tools.
Decoupled from specific third-party applications.
"""

from typing import Any
from src.tools.base import BaseHealthcareTool, HealthcareToolDefinition, ToolExecutionResult


class ToolRegistry:
    """Registry managing available clinical and logistical healthcare tools."""

    def __init__(self) -> None:
        self._tools: dict[str, BaseHealthcareTool] = {}

    def register(self, tool: BaseHealthcareTool) -> None:
        """Registers a healthcare tool."""
        self._tools[tool.definition.name] = tool

    def get(self, name: str) -> BaseHealthcareTool | None:
        """Retrieves a tool by name."""
        return self._tools.get(name)

    def list_definitions(self) -> list[HealthcareToolDefinition]:
        """Lists definitions of all registered tools."""
        return [tool.definition for tool in self._tools.values()]

    async def execute(self, tool_name: str, **kwargs: Any) -> ToolExecutionResult:
        """Dispatches execution to a registered tool."""
        tool = self.get(tool_name)
        if not tool:
            return ToolExecutionResult(
                tool_name=tool_name,
                success=False,
                error_message=f"Tool '{tool_name}' is not registered in MIRA Tool Registry.",
            )
        return await tool.execute(**kwargs)


# Global default registry instance
TOOL_REGISTRY = ToolRegistry()
