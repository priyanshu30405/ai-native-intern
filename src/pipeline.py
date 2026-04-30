import json
import re
from typing import Any, Dict

from src.clients import OpenRouterClient
from src.prompts import SYSTEM_PROMPT, user_prompt
from src.schema import TriageOutput


ARABIC_RE = re.compile(r"[\u0600-\u06FF]")


def _detect_language(text: str) -> str:
    has_ar = bool(ARABIC_RE.search(text))
    has_en = bool(re.search(r"[A-Za-z]", text))
    if has_ar and has_en:
        return "mixed"
    if has_ar:
        return "ar"
    if has_en:
        return "en"
    return "unknown"


def _fallback_triage(message_text: str) -> Dict[str, Any]:
    text = message_text.lower()
    language = _detect_language(message_text)
    intent = "other"
    urgency = "low"
    missing_info = []

    if any(k in text for k in ["refund", "money back", "استرجاع", "refund me"]):
        intent = "refund"
    elif any(k in text for k in ["exchange", "replace", "استبدال"]):
        intent = "exchange"
    elif any(
        k in text
        for k in ["late", "delayed", "not received", "delivery", "تأخر", "لم يصل", "شحنة"]
    ):
        intent = "delivery_issue"
    elif any(k in text for k in ["cancel", "إلغاء"]):
        intent = "cancel"
    elif any(k in text for k in ["change address", "change size", "update order"]):
        intent = "order_change"
    elif any(k in text for k in ["is this", "ingredients", "suitable", "هل"]):
        intent = "product_question"

    if any(k in text for k in ["urgent", "asap", "today", "baby sick", "ضروري", "حالاً"]):
        urgency = "high"
    elif any(k in text for k in ["soon", "tomorrow", "بكرة"]):
        urgency = "medium"

    if "order" not in text and "طلب" not in text:
        missing_info.append("order_id")

    confidence = 0.72 if intent != "other" else 0.45
    uncertainty_note = None
    needs_human = False
    if confidence < 0.6:
        uncertainty_note = "Message is too ambiguous; route to human for accurate handling."
        needs_human = True

    return {
        "language_detected": language,
        "intent": intent,
        "urgency": urgency,
        "confidence": confidence,
        "needs_human": needs_human,
        "reasoning_short": "Classified using fallback rules due to missing API key or model failure.",
        "suggested_reply_en": "Thanks for contacting Mumzworld. We are reviewing your request and will help shortly.",
        "suggested_reply_ar": "شكراً لتواصلك مع مومزوورلد. نقوم بمراجعة طلبك وسنساعدك قريباً.",
        "missing_info": missing_info,
        "uncertainty_note": uncertainty_note,
    }


def run_triage(message_text: str, order_context: str = "") -> TriageOutput:
    client = OpenRouterClient()
    try:
        if client.enabled:
            raw = client.complete_json(
                system_prompt=SYSTEM_PROMPT,
                user_prompt=user_prompt(message_text=message_text, order_context=order_context),
            )
        else:
            raw = _fallback_triage(message_text)
    except Exception:
        raw = _fallback_triage(message_text)

    return TriageOutput.model_validate(raw)


def to_json(result: TriageOutput) -> str:
    return json.dumps(result.model_dump(), ensure_ascii=False, indent=2)
