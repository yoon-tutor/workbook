#!/usr/bin/env python3
"""Compact or expand a semantic authoring packet for a canonical workbook."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from workbook_authoring import compact_canonical, expand_packet, verify_new_packet_policy


def _load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit("input JSON must contain one object")
    return value


def _write(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("compact", "expand"):
        command = commands.add_parser(name)
        command.add_argument("input", type=Path)
        command.add_argument("--output", type=Path, required=True)
    verify = commands.add_parser("verify")
    verify.add_argument("input", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    value = _load(args.input)
    if args.command == "compact":
        _write(args.output, compact_canonical(value))
        print(args.output)
    elif args.command == "expand":
        verify_new_packet_policy(value)
        _write(args.output, expand_packet(value))
        print(args.output)
    else:
        verify_new_packet_policy(value)
        canonical = expand_packet(value)
        print(
            json.dumps(
                {
                    "status": "passed",
                    "workbookId": canonical["workbookId"],
                    "sentences": len(canonical["sentences"]),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
