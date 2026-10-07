"""MIRA Clinical Red Flags & Emergency Detection.

Catalogs life-threatening symptoms and acute clinical indicators requiring
immediate emergency intervention and 911 / EMS escalation.
"""

from dataclasses import dataclass
from enum import Enum
import re


class RedFlagCategory(str, Enum):
    """Clinical category of critical red-flag presentation."""
    CARDIOVASCULAR = "cardiovascular"
    NEUROLOGICAL = "neurological"
    RESPIRATORY = "respiratory"
    TRAUMA_HEMORRHAGE = "trauma_hemorrhage"
    ANAPHYLAXIS = "anaphylaxis"
    PSYCHIATRIC_CRISIS = "psychiatric_crisis"
    OBSTETRIC = "obstetric"


@dataclass(frozen=True)
class RedFlagItem:
    """Individual clinical red flag indicator."""
    code: str
    category: RedFlagCategory
    label: str
    patterns: list[str]
    suggested_action: str


RED_FLAG_CATALOG: list[RedFlagItem] = [
    RedFlagItem(
        code="RF_CARDIO_01",
        category=RedFlagCategory.CARDIOVASCULAR,
        label="Acute Chest Pain / Myocardial Infarction Indicator",
        patterns=[
            r"\b(crushing|severe|radiating|tight) chest pain\b",
            r"\bpain (in|radiating to) (left arm|jaw|neck|back)\b",
            r"\bchest (pressure|heaviness|squeezing)\b",
            r"\bheart attack\b",
        ],
        suggested_action="Immediate emergency response: Dial local emergency number (e.g., 911) immediately.",
    ),
    RedFlagItem(
        code="RF_NEURO_01",
        category=RedFlagCategory.NEUROLOGICAL,
        label="Acute Stroke / Neurological Deficit (FAST signs)",
        patterns=[
            r"\bface (droop|drooping|numbness)\b",
            r"\b(arm|leg) weakness (on one side|sudden)\b",
            r"\bsudden (numbness|paralysis) on one side\b",
            r"\bslurred speech\b",
            r"\bunable to speak\b",
            r"\bsudden severe headache\b",
            r"\bthunderclap headache\b",
        ],
        suggested_action="Suspected acute stroke: Activate emergency medical services immediately without delay.",
    ),
    RedFlagItem(
        code="RF_RESP_01",
        category=RedFlagCategory.RESPIRATORY,
        label="Severe Respiratory Distress / Airway Obstruction",
        patterns=[
            r"\bcan'?t breathe\b",
            r"\bcannot breathe\b",
            r"\bsevere shortness of breath\b",
            r"\bchoking\b",
            r"\bturning blue\b",
            r"\bgasping for air\b",
            r"\bstridor\b",
        ],
        suggested_action="Severe airway compromise: Immediate 911/EMS dispatch required.",
    ),
    RedFlagItem(
        code="RF_ANAPH_01",
        category=RedFlagCategory.ANAPHYLAXIS,
        label="Anaphylaxis / Severe Systemic Allergic Reaction",
        patterns=[
            r"\bthroat closing\b",
            r"\bswelling of (lips|tongue|throat)\b",
            r"\banaphylaxis\b",
            r"\bsevere allergic reaction\b",
        ],
        suggested_action="Immediate administration of epinephrine if available, and call 911 immediately.",
    ),
    RedFlagItem(
        code="RF_TRAUMA_01",
        category=RedFlagCategory.TRAUMA_HEMORRHAGE,
        label="Severe Hemorrhage / Uncontrolled Bleeding",
        patterns=[
            r"\buncontrolled bleeding\b",
            r"\bspurting blood\b",
            r"\bcoughing up blood\b",
            r"\bvomi?ting (large amounts of )?blood\b",
            r"\bmassive blood loss\b",
        ],
        suggested_action="Apply direct pressure and seek immediate emergency trauma care.",
    ),
    RedFlagItem(
        code="RF_PSYCH_01",
        category=RedFlagCategory.PSYCHIATRIC_CRISIS,
        label="Acute Self-Harm / Suicide Crisis",
        patterns=[
            r"\bwant to (kill myself|end my life|die)\b",
            r"\bcommit suicide\b",
            r"\bthoughts of suicide\b",
            r"\bself-harm\b",
        ],
        suggested_action="Immediate crisis hotline connection: Call or text 988 (Suicide & Crisis Lifeline) or local emergency services.",
    ),
]


def detect_red_flags(text: str) -> list[RedFlagItem]:
    """Scans text for clinical red flag matches.
    
    Returns:
        list[RedFlagItem]: Detected red flag indicators.
    """
    normalized = text.lower()
    detected: list[RedFlagItem] = []
    
    for item in RED_FLAG_CATALOG:
        for pattern in item.patterns:
            if re.search(pattern, normalized):
                detected.append(item)
                break  # Don't add duplicate item if multiple patterns match
                
    return detected
