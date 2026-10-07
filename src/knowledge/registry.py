"""MIRA Medical Knowledge Registry.

Coordinates clinical document repositories and evidence-based guideline retrievers.
"""

from src.knowledge.base import MedicalKnowledgeRetriever, MedicalDocument


class InMemoryKnowledgeRetriever:
    """Baseline reference knowledge retriever populated with foundational guidelines."""

    def __init__(self) -> None:
        self._documents: list[MedicalDocument] = [
            MedicalDocument(
                document_id="GUIDE-CARDIO-001",
                title="AHA Guidelines for Acute Coronary Syndromes",
                source="American Heart Association",
                content=(
                    "Patients with acute crushing chest pain, dyspnea, or pain radiating to the left arm "
                    "or jaw must immediately be referred to emergency medical care for rapid ECG and evaluation."
                ),
                confidence_score=0.99,
                topics=["cardiology", "chest pain", "emergency"],
            ),
            MedicalDocument(
                document_id="GUIDE-NEURO-001",
                title="AHA/ASA Guidelines for Acute Ischemic Stroke (FAST protocol)",
                source="American Stroke Association",
                content=(
                    "Sudden face drooping, arm weakness, or speech difficulty indicates suspected acute stroke. "
                    "Time is critical; immediate EMS activation is mandated."
                ),
                confidence_score=0.99,
                topics=["neurology", "stroke", "emergency"],
            ),
            MedicalDocument(
                document_id="GUIDE-GEN-001",
                title="CDC Guidance for Common Cold and Upper Respiratory Infections",
                source="Centers for Disease Control and Prevention",
                content=(
                    "Most viral upper respiratory tract infections resolve with rest, hydration, and symptomatic "
                    "support. Seek care if symptoms persist beyond 10 days or high persistent fever develops."
                ),
                confidence_score=0.95,
                topics=["respiratory", "cold", "routine"],
            ),
        ]

    async def retrieve(self, query: str, top_k: int = 3) -> list[MedicalDocument]:
        """Simple keyword-matching baseline retriever."""
        normalized = query.lower()
        matched = []
        for doc in self._documents:
            if any(term in normalized for term in doc.topics) or any(
                w in doc.content.lower() for w in normalized.split() if len(w) > 3
            ):
                matched.append(doc)
        return (matched or self._documents)[:top_k]
