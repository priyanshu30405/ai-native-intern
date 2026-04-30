# Tradeoffs

## Why this architecture

- **Chosen:** single-pass triage with strict schema output  
  **Reason:** fastest way to ship a reliable prototype in ~5 hours.

- **Chosen:** optional OpenRouter model + local fallback  
  **Reason:** keeps submission runnable without paid keys and avoids blocking demo.

- **Chosen:** CLI interface (not full web app)  
  **Reason:** prioritizes correctness, evals, and reproducibility over UI polish.

## Rejected options

- Full agentic workflow with retrieval and tool calls: too much moving surface for 5-hour scope.
- Fine-tuning: unnecessary for a prototype and difficult to validate quickly.
- External scraped dataset: disallowed by assignment constraints.

## Uncertainty strategy

- Confidence is explicit.
- Low confidence requires `uncertainty_note`.
- Ambiguous cases set `needs_human=true`.
- Output avoids inventing policy/order details not in input.

## What was cut

- No persistent datastore/dashboard for triage history.
- No SLA-aware queue prioritization logic.
- No bilingual quality scorer for reply fluency.

## If given more time

- Add model-graded and human-graded Arabic response quality evals.
- Add confidence calibration and threshold tuning on larger labeled set.
- Add lightweight web UI + CSV batch upload for support operations.
