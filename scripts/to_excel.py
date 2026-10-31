"""Convert generated prompt JSON into an Excel workbook."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from openpyxl import Workbook


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="JSON response from call_service.py")
    parser.add_argument(
        "output",
        type=Path,
        nargs="?",
        default=Path("output/prompts.xlsx"),
        help="Destination workbook.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        payload: Any = json.loads(args.input.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Could not read input JSON: {exc}", file=sys.stderr)
        return 1

    prompts = payload.get("prompts") if isinstance(payload, dict) else None
    if not isinstance(prompts, list):
        print("Input JSON must contain a 'prompts' list.", file=sys.stderr)
        return 1

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Prompts"
    sheet.append(["Category", "Prompt"])
    for item in prompts:
        if not isinstance(item, dict):
            print("Each prompt must be an object.", file=sys.stderr)
            return 1
        sheet.append([item.get("category", ""), item.get("prompt", "")])
    sheet.freeze_panes = "A2"
    sheet.column_dimensions["A"].width = 24
    sheet.column_dimensions["B"].width = 100

    try:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        workbook.save(args.output)
    except OSError as exc:
        print(f"Could not write workbook: {exc}", file=sys.stderr)
        return 1
    print(f"Saved workbook to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
