import argparse
import sys

from dotenv import load_dotenv

from src.pipeline import run_triage, to_json


def main():
    # Ensure Arabic output prints correctly on Windows terminals.
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    load_dotenv()
    parser = argparse.ArgumentParser(description="Mumzworld EN/AR support triage prototype")
    parser.add_argument("--text", required=True, help="Customer support message text")
    parser.add_argument(
        "--order-context", default="", help="Optional order metadata/context for grounding"
    )
    args = parser.parse_args()

    result = run_triage(message_text=args.text, order_context=args.order_context)
    print(to_json(result))


if __name__ == "__main__":
    main()
