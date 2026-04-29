# Mumzworld AI Intern - Track A

Track: A

I built a multilingual customer-support triage assistant for Mumzworld that takes incoming EN/AR support text, outputs strict structured JSON (intent, urgency, confidence, missing info), drafts native-sounding replies in English and Arabic, and explicitly flags uncertainty for human escalation when confidence is low.

## Prototype access

This GitHub repository contains a runnable CLI prototype:

GitHub repo link: `<https://github.com/priyanshu30405/ai-native-intern>`

- Install: `pip install -r requirements.txt`
- Run: `python app.py --text "<your message>"`

## 3-minute walkthrough Loom

Loom walkthrough: `<https://www.loom.com/share/b02864cf85ff4fd091ccdc54bcdd2de9>`

## Markdown deliverables

- `EVALS.md`
- `TRADEOFFS.md`

## AI usage note (max 5 lines)

- Models: OpenRouter gateway (optional online path); fallback uses deterministic rule-based triage.
- Builder: Python pipeline + strict Pydantic schema validation for structured output.
- Prompts: structured JSON contract in `src/prompts.py`.
- Tools: Cursor-assisted code scaffolding, prompt iteration, and README drafting.
- No external scraping; test set is synthetic and included in `evals/test_cases.json`.

## Time log (max 5 lines)

- Discovery + problem framing: `__ min`
- Prototype implementation (schema + pipeline): `__ min`
- Evals + test set + runner: `__ min`
- Documentation + Loom prep: `__ min`
- Final polish: `__ min`

## Why this problem

Support triage is high-volume and time-sensitive for e-commerce operations. A reliable triage layer can speed routing, reduce first-response time, and improve consistency while still escalating uncertain cases to human agents.

## Features

- Multilingual input handling (`en`, `ar`, `mixed`)
- Structured output schema validation with Pydantic
- Intent classification (`refund`, `exchange`, `delivery_issue`, `product_question`, `cancel`, `order_change`, `other`)
- Urgency scoring (`low`, `medium`, `high`)
- Confidence + explicit uncertainty note
- Human escalation flag (`needs_human`)
- Suggested replies in English and Arabic
- Eval runner with reproducible test set

## Quickstart (under 5 minutes)

1. Install Python 3.10+.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Optional: connect OpenRouter for LLM inference.
   - Copy `.env.example` to `.env`
   - Set `OPENROUTER_API_KEY`
4. Run one prediction:

```bash
python app.py --text "My order MW-8871 is delayed and not received yet."
```

If no API key is configured, the app uses a local fallback classifier so the project remains runnable.

## Run evals

```bash
python evals/run_evals.py
```

The script reports:
- intent accuracy
- schema validity rate
- uncertainty handling rate
- detailed per-case outputs

## Project structure

- `app.py`: CLI entry point
- `src/schema.py`: strict output schema
- `src/prompts.py`: system/user prompts for model
- `src/clients.py`: OpenRouter integration
- `src/pipeline.py`: inference orchestration + fallback
- `evals/test_cases.json`: test dataset (EN + AR + adversarial)
- `evals/run_evals.py`: evaluation script
- `EVALS.md`: rubric + results + failure analysis
- `TRADEOFFS.md`: architecture decisions and what was cut

## Tooling transparency

- Model gateway: OpenRouter (optional online path)
- Local harness: Python CLI + Pydantic validation
- Fallback path: deterministic rule-based triage
- AI assistant use: code scaffolding, prompt iteration, and documentation drafting

## Commands for the demo

```bash
python app.py --text "Hi, I want a refund for order MW-1032. The stroller arrived damaged."
python app.py --text "مرحبا، أحتاج استبدال مقاس الحذاء في طلبي MW-5521."
python app.py --text "This is not what I expected."
python evals/run_evals.py
```
