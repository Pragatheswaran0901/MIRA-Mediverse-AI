"""MIRA Clinical Knowledge Base & RAG Contracts.

Defines schemas and protocols for retrieving verified clinical guidelines,
medical literature, and triage references.
"""

from typing import Protocol, runtime_checkable
from pydantic import BaseModel, Field


class MedicalDocument(BaseModel):
    """Clinical guideline or reference document snippet."""
    document_id: str
    title: str
    source: str  # e.g., "CDC Guidelines", "WHO", "AHA", "Mayo Clinic"
    content: str
    confidence_score: float = Field(default=1.0, ge=0.0, le=1.0)
    topics: list[str] = Field(default_factory=list)


@runtime_checkable
class MedicalKnowledgeRetriever(Protocol):
    """Protocol for RAG-based clinical knowledge retrieval."""
    async def retrieve(self, query: str, top_k: int = 3) -> list[MedicalDocument]:
        """Retrieves top_k relevant medical documents matching query."""
        ...
