# Evals

## Rubric

We evaluate on three dimensions:

1. **Intent accuracy**: predicted `intent` equals expected intent.
2. **Schema validity**: output always conforms to the Pydantic schema.
3. **Uncertainty handling**: if `confidence < 0.6`, output must include `uncertainty_note`.

## Test set

- 12 cases total
- Mix of English, Arabic, mixed-language, and ambiguous/adversarial examples
- Includes cases requiring escalation/uncertainty

## How to run

```bash
python evals/run_evals.py
```

## Current results

Latest local run (`python evals/run_evals.py`):
- Intent accuracy: `12/12 = 100.0%`
- Schema validity rate: `12/12 = 100.0%`
- Uncertainty handling rate: `12/12 = 100.0%`

Notes:
- These scores are on a synthetic test set designed for this prototype.
- High scores here prove pipeline correctness and schema reliability, not production readiness.
- The report also prints per-case outputs to support manual reviewer inspection.

## Known failure modes

- Nuanced policy questions can be misrouted to `product_question` or `other`.
- Mixed-intent messages (e.g., refund + complaint + order change) may collapse to one label.
- Arabic dialect variations may reduce confidence for the fallback path.

## Next eval upgrades

- Add confusion matrix and per-intent precision/recall
- Add bilingual fluency scoring for draft replies
- Add robustness tests for typo-heavy and code-mixed Arabic inputs
