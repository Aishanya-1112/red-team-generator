"""Call the prompt-generation service and save its JSON response."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import requests


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://localhost:8000/generate")
    parser.add_argument("--input-one", required=True)
    parser.add_argument("--input-two", required=True)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("output/prompts.json"),
        help="Path for the JSON response.",
    )
    parser.add_argument("--timeout", type=float, default=30)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = {"input_one": args.input_one, "input_two": args.input_two}

    try:
        response = requests.post(args.url, json=payload, timeout=args.timeout)
        response.raise_for_status()
        result = response.json()
    except requests.RequestException as exc:
        print(f"Service request failed: {exc}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"Service returned invalid JSON: {exc}", file=sys.stderr)
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Saved response to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
