"""Command line entry point for the canonical workbook engine."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .compiler import compile_file
from .migrate_legacy import migrate
from .release import prepare_release, publish_release, release_status
from .schema_gate import validate_schema
from .validator import load_json, load_spec, require_valid, validate_canonical


ROOT = Path(__file__).resolve().parents[1]


def _print_json(value: object) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def _validate(path: Path) -> None:
    data = load_json(path)
    schema = load_json(ROOT / "schemas" / "canonical-workbook.schema.json")
    schema_issues = validate_schema(data, schema)
    if schema_issues:
        raise SystemExit("\n".join(issue.format() for issue in schema_issues))
    issues = validate_canonical(data, load_spec())
    require_valid(issues)
    warnings = [issue.format() for issue in issues if issue.severity != "error"]
    _print_json(
        {
            "status": "passed",
            "workbookId": data.get("workbookId"),
            "sentences": len(data.get("sentences", [])),
            "schemaIssues": 0,
            "warnings": warnings,
        }
    )


def _inspect(path: Path, sentence_no: int) -> None:
    data = load_json(path)
    sentence = next(
        (item for item in data.get("sentences", []) if int(item.get("no", -1)) == sentence_no),
        None,
    )
    if sentence is None:
        raise SystemExit(f"sentence {sentence_no} was not found")
    _print_json(sentence)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    validate = commands.add_parser("validate", help="validate canonical content")
    validate.add_argument("canonical", type=Path)

    inspect = commands.add_parser("inspect", help="print one canonical sentence record")
    inspect.add_argument("canonical", type=Path)
    inspect.add_argument("--sentence", type=int, required=True)

    compile_command = commands.add_parser("compile", help="compile one edition to page IR")
    compile_command.add_argument("canonical", type=Path)
    compile_command.add_argument("--edition", choices=("student", "answer"), required=True)
    compile_command.add_argument("--output", type=Path, required=True)

    migrate_command = commands.add_parser("migrate-legacy", help="convert the approved legacy builder")
    migrate_command.add_argument("legacy", type=Path)
    migrate_command.add_argument("--output", type=Path, required=True)

    prepare = commands.add_parser("prepare", help="build and QA privately without publishing")
    prepare.add_argument("canonical", type=Path)
    prepare.add_argument("--update", type=Path, required=True)
    prepare.add_argument("--output-base")
    prepare.add_argument("--allow-manual-review", action="store_true")

    status = commands.add_parser("status", help="inspect the latest prepared or published release")
    status.add_argument("canonical", type=Path)
    status.add_argument("--build-dir", type=Path)

    publish = commands.add_parser("publish", help="publish a visually approved prepared build")
    publish.add_argument("build_dir", type=Path)
    publish.add_argument("--reviewer", required=True)
    publish.add_argument("--notes", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "validate":
        _validate(args.canonical)
    elif args.command == "inspect":
        _inspect(args.canonical, args.sentence)
    elif args.command == "compile":
        compile_file(args.canonical, args.edition, args.output)
        print(args.output)
    elif args.command == "migrate-legacy":
        canonical = migrate(args.legacy.resolve())
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(canonical, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(args.output)
    elif args.command == "prepare":
        result = prepare_release(
            args.canonical,
            update_path=args.update,
            output_base=args.output_base,
            allow_manual_review=args.allow_manual_review,
        )
        _print_json(
            {
                "status": "awaiting-visual-review",
                "buildDir": str(result.build_dir),
                "pageCount": result.page_count,
                "contactSheets": [str(path) for path in result.contact_sheets],
            }
        )
    elif args.command == "status":
        _print_json(release_status(args.canonical, build_dir=args.build_dir))
    elif args.command == "publish":
        result = publish_release(args.build_dir, reviewer=args.reviewer, notes=args.notes)
        _print_json(
            {
                "status": "published",
                "outputDir": str(result.output_dir),
                "report": str(result.report_path),
                "updateIndex": str(result.aggregate_report_path),
                "manifest": str(result.build_manifest_path),
            }
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
