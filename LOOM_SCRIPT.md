# 3-Minute Loom Script

Use this exact flow while screen recording.

Recording style:
- Keep this script visible as a cue card (this is fine).
- Spend most of the time on terminal output and project files.
- Target ratio: ~25% script on screen, ~75% live demo.

## 0:00 - 0:20 Intro

"Hi, I am Priyanshu. This is my Mumzworld Track A submission: an English/Arabic customer support triage assistant.  
It takes incoming support text, returns strict structured JSON, drafts replies in English and Arabic, and explicitly escalates uncertain cases."

## 0:20 - 0:45 Project overview

Show repository root and briefly point to:
- `app.py`
- `src/schema.py`
- `src/pipeline.py`
- `evals/test_cases.json`
- `evals/run_evals.py`

Say:
"The core reliability layer is strict schema validation with uncertainty rules. If confidence is low, the output must include an uncertainty note."

## 0:45 - 1:20 English happy path demo

Run:

```bash
python app.py --text "Hi, I want a refund for order MW-1032. The stroller arrived damaged."
```

Say:
"This case is correctly classified as refund, with bilingual drafted replies and confidence score."

## 1:20 - 1:50 Arabic happy path demo

Run:

```bash
python app.py --text "مرحبا، أحتاج استبدال مقاس الحذاء في طلبي MW-5521."
```

Say:
"This Arabic request is routed to exchange intent, preserving multilingual behavior in output."

## 1:50 - 2:20 Uncertainty / refusal behavior

Run:

```bash
python app.py --text "This is not what I expected."
```

Say:
"This message is ambiguous. The system lowers confidence, sets `needs_human=true`, and adds an explicit uncertainty note instead of inventing facts."

## 2:20 - 2:50 Eval proof

Run:

```bash
python evals/run_evals.py
```

Say:
"Here are eval metrics across 12 synthetic EN/AR cases: intent accuracy, schema validity, and uncertainty handling. I also print per-case outputs for transparent inspection."

## 2:50 - 3:00 Close

Say:
"Tradeoffs, failure modes, and tooling transparency are documented in `TRADEOFFS.md`, `EVALS.md`, and `README.md`. Thank you."

