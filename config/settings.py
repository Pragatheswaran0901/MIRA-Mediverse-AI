"""MIRA Configuration & Environment Settings.

Provides strongly-typed application settings loaded from environment variables
or .env files with defensive defaults.
"""

from functools import lru_cache
from typing import Literal
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration for MIRA healthcare assistant."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Core Application Metadata
    app_name: str = Field(default="MIRA", description="Product acronym name")
    app_full_name: str = Field(
        default="Medical Intelligent Response Assistant",
        description="Full formal name of the product",
    )
    version: str = Field(default="0.1.0", description="Semantic version")
    current_block: str = Field(
        default="Block 1: Project Foundation",
        description="Current engineering milestone block",
    )
    environment: Literal["development", "staging", "production", "testing"] = Field(
        default="development",
        alias="MIRA_ENV",
        description="Runtime deployment environment",
    )
    debug: bool = Field(default=True, alias="MIRA_DEBUG")

    # Networking & Server
    host: str = Field(default="0.0.0.0", alias="MIRA_HOST")
    port: int = Field(default=8000, alias="MIRA_PORT")
    secret_key: str = Field(
        default="dev-secret-key-mira-standalone-do-not-use-in-production-32c",
        alias="MIRA_SECRET_KEY",
    )

    # Safety Guardrails Flags
    strict_safety_mode: bool = Field(
        default=True,
        alias="MIRA_STRICT_SAFETY_MODE",
        description="Enforces strict pre- and post-processing safety audits",
    )
    emergency_escalation_enabled: bool = Field(
        default=True,
        alias="MIRA_EMERGENCY_ESCALATION_ENABLED",
        description="Whether red-flag emergency detection interrupts standard flow",
    )
    disclaimer_enforcement: bool = Field(
        default=True,
        alias="MIRA_DISCLAIMER_ENFORCEMENT",
        description="Mandatory medical disclaimer appended to clinical guidance",
    )

    # Future AI / LLM Engine Settings (Foundational hooks)
    llm_provider: str = Field(default="mock", alias="MIRA_LLM_PROVIDER")
    llm_model: str = Field(default="gemini-2.5-flash", alias="MIRA_LLM_MODEL")
    llm_api_key: str | None = Field(default=None, alias="MIRA_LLM_API_KEY")

    # Future Voice & Character Hooks
    voice_id: str = Field(default="mira-caring-nurse-v1", alias="MIRA_VOICE_ID")
    voice_sample_rate: int = Field(default=24000, alias="MIRA_VOICE_SAMPLE_RATE")


@lru_cache
def get_settings() -> Settings:
    """Singleton getter for application settings."""
    return Settings()
