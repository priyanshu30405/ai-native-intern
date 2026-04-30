import json
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.pipeline import run_triage


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    load_dotenv()
    here = Path(__file__).resolve().parent
    cases = json.loads((here / "test_cases.json").read_text(encoding="utf-8"))

    total = len(cases)
    correct_intent = 0
    valid_schema = 0
    uncertainty_ok = 0
    rows = []

    for case in cases:
        result = run_triage(case["input"])
        row = result.model_dump()
        row["id"] = case["id"]
        row["expected_intent"] = case["expected_intent"]
        row["intent_match"] = row["intent"] == case["expected_intent"]

        if row["intent_match"]:
            correct_intent += 1
        valid_schema += 1

        uncertainty_valid = not (row["confidence"] < 0.6 and not row["uncertainty_note"])
        if uncertainty_valid:
            uncertainty_ok += 1
        row["uncertainty_valid"] = uncertainty_valid
        rows.append(row)

    print("=== Mumzworld Track A Eval Results ===")
    print(f"Total cases: {total}")
    print(f"Intent accuracy: {correct_intent}/{total} = {correct_intent/total:.1%}")
    print(f"Schema valid rate: {valid_schema}/{total} = {valid_schema/total:.1%}")
    print(f"Uncertainty handling rate: {uncertainty_ok}/{total} = {uncertainty_ok/total:.1%}")
    print()
    print("Per-case outputs:")
    print(json.dumps(rows, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
