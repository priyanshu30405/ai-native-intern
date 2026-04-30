from typing import List, Literal, Optional

from pydantic import BaseModel, Field, field_validator


Intent = Literal[
    "refund",
    "exchange",
    "delivery_issue",
    "product_question",
    "cancel",
    "order_change",
    "other",
]

Urgency = Literal["low", "medium", "high"]


class TriageOutput(BaseModel):
    language_detected: Literal["en", "ar", "mixed", "unknown"]
    intent: Intent
    urgency: Urgency
    confidence: float = Field(ge=0.0, le=1.0)
    needs_human: bool
    reasoning_short: str = Field(min_length=5, max_length=280)
    suggested_reply_en: str = Field(min_length=5)
    suggested_reply_ar: str = Field(min_length=5)
    missing_info: List[str] = Field(default_factory=list)
    uncertainty_note: Optional[str] = None

    @field_validator("uncertainty_note")
    @classmethod
    def require_uncertainty_when_low_confidence(cls, value: Optional[str], info):
        confidence = info.data.get("confidence", 1.0)
        if confidence < 0.6 and (value is None or not value.strip()):
            raise ValueError("uncertainty_note is required when confidence < 0.6")
        return value
