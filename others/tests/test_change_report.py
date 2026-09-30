from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from workbook_engine.change_report import (
    UpdateDefinition,
    compare_bundles,
    main,
    render_markdown,
    update_changelog,
    write_report,
)
from workbook_engine.manifest import (
    ManifestBundle,
    canonical_json,
    json_digest,
    load_bundle,
    write_bundle,
)


def update_data(apply_to: str = "all") -> dict:
    value = {
        "id": "U-20260710-001",
        "title": "배열 문장부호 보존",
        "date": "2026-07-10",
        "summary": "8단계 배열 결과를 원문과 일치시킵니다.",
        "category": "compiler",
        "applyTo": apply_to,
        "affectedStages": [8],
        "request": ["콘텐츠의 단어와 순서는 유지합니다."],
        "directChanges": {
            "files": ["workbook_engine/compiler.py"],
            "jsonPaths": [
                {
                    "manifest": "spec",
                    "path": "$.stages[0].preservePunctuation",
                }
            ],
        },
        "verification": [
            {
                "name": "source-restore",
                "status": "pass",
                "details": "원문 복원 통과",
            }
        ],
    }
    if apply_to == "selected":
        value["selectedWorkbooks"] = ["chocolate", "productive-people"]
    return value


def before_bundle() -> ManifestBundle:
    return ManifestBundle(
        canonical={
            "version": "1.0.0",
            "files": [
                {"path": "workbooks/chocolate/content.json", "sha256": "aaa", "size": 10}
            ],
            "stages": [
                {
                    "id": 8,
                    "items": [
                        {"id": "s05", "answer": "It is thought."},
                        {"id": "s06", "answer": "They used cacao."},
                    ],
                }
            ],
        },
        spec={
            "version": "1.2.0",
            "stages": [{"id": 8, "preservePunctuation": False}],
        },
        template={
            "version": "2.0.0",
            "files": [{"path": "templates/renderer.js", "sha256": "111", "size": 20}],
        },
        build={
            "version": "3.0.0",
            "files": [{"path": "outputs/chocolate/문제.pdf", "sha256": "old", "size": 100}],
            "pages": [
                {
                    "id": "student-p08",
                    "edition": "student",
                    "page": 8,
                    "stageId": 8,
                    "itemIds": ["s05", "s06"],
                    "sha256": "page-old",
                }
            ],
            "outputs": [
                {"path": "문제.pdf", "sha256": "old", "pages": 20, "size": 100}
            ],
        },
    )


def after_bundle() -> ManifestBundle:
    return ManifestBundle(
        canonical={
            "version": "1.0.1",
            "files": [
                {"path": "workbooks/chocolate/content.json", "sha256": "bbb", "size": 11}
            ],
            "stages": [
                {
                    "id": 8,
                    "items": [
                        {"id": "s05", "answer": "It is thought!"},
                        {"id": "s06", "answer": "They used cacao."},
                    ],
                }
            ],
        },
        spec={
            "version": "1.2.1",
            "stages": [{"id": 8, "preservePunctuation": True}],
        },
        template={
            "version": "2.0.0",
            "files": [{"path": "templates/renderer.js", "sha256": "111", "size": 20}],
        },
        build={
            "version": "3.0.1",
            "files": [{"path": "outputs/chocolate/문제.pdf", "sha256": "new", "size": 101}],
            "pages": [
                {
                    "id": "student-p08",
                    "edition": "student",
                    "page": 8,
                    "stageId": 8,
                    "itemIds": ["s05", "s06"],
                    "sha256": "page-new",
                }
            ],
            "outputs": [
                {"path": "문제.pdf", "sha256": "new", "pages": 20, "size": 101}
            ],
        },
    )


class ManifestTests(unittest.TestCase):
    def test_digest_and_json_are_mapping_order_independent(self) -> None:
        left = {"b": 2, "a": {"y": 2, "x": 1}}
        right = {"a": {"x": 1, "y": 2}, "b": 2}
        self.assertEqual(canonical_json(left), canonical_json(right))
        self.assertEqual(json_digest(left), json_digest(right))

    def test_bundle_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bundle.json"
            write_bundle(path, before_bundle())
            loaded = load_bundle(path)
            self.assertEqual(loaded, before_bundle())
            self.assertEqual(list(json.loads(path.read_text(encoding="utf-8"))), [
                "build",
                "bundleVersion",
                "canonical",
                "spec",
                "template",
            ])


class UpdateDefinitionTests(unittest.TestCase):
    def test_all_apply_modes_are_supported(self) -> None:
        for apply_to in ("new-only", "all", "selected", "manual-review"):
            with self.subTest(apply_to=apply_to):
                update = UpdateDefinition.from_dict(update_data(apply_to))
                self.assertEqual(update.apply_to, apply_to)

    def test_selected_requires_workbook_ids(self) -> None:
        value = update_data("selected")
        value.pop("selectedWorkbooks")
        with self.assertRaisesRegex(ValueError, "selectedWorkbooks"):
            UpdateDefinition.from_dict(value)


class ChangeReportTests(unittest.TestCase):
    def setUp(self) -> None:
        self.update = UpdateDefinition.from_dict(update_data())
        self.report = compare_bundles(before_bundle(), after_bundle(), self.update)

    def test_compare_tracks_direct_and_derived_impacts(self) -> None:
        self.assertTrue(self.report.direct_changes)
        self.assertTrue(self.report.derived_changes)
        self.assertIn("8", self.report.stage_ids)
        self.assertIn("s05", self.report.item_ids)
        self.assertEqual([page.page for page in self.report.page_changes], ["student-p08"])
        self.assertEqual([output.output for output in self.report.output_changes], ["문제.pdf"])

        file_classes = {(item.path, item.classification) for item in self.report.file_changes}
        self.assertIn(("workbooks/chocolate/content.json", "direct"), file_classes)
        self.assertIn(("outputs/chocolate/문제.pdf", "derived"), file_classes)
        self.assertIn(("workbook_engine/compiler.py", "direct"), file_classes)

    def test_component_comparison_includes_all_four_manifests(self) -> None:
        self.assertEqual(
            [row["component"] for row in self.report.component_rows],
            ["canonical", "spec", "template", "build"],
        )
        statuses = {row["component"]: row["status"] for row in self.report.component_rows}
        self.assertEqual(statuses["template"], "unchanged")
        self.assertEqual(statuses["canonical"], "changed")

    def test_markdown_is_deterministic_and_complete(self) -> None:
        first = render_markdown(self.report)
        second = render_markdown(self.report)
        self.assertEqual(first, second)
        for expected in (
            "## manifest 비교",
            "## 직접 변경",
            "## 파생 영향",
            "## 영향 없음",
            "## 출력 변화",
            "## 검증 결과",
            "## 호환성",
            "## 버전",
            "student-p08",
            "문제.pdf",
            "s05",
            "`all`",
        ):
            self.assertIn(expected, first)

    def test_changelog_is_only_written_when_explicitly_requested(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            report_path = root / "reports" / "updates" / "U-20260710-001.md"
            changelog = root / "CHANGELOG.md"
            write_report(report_path, self.report)
            self.assertFalse(changelog.exists())

            update_changelog(changelog, self.report, report_path=report_path)
            update_changelog(changelog, self.report, report_path=report_path)
            content = changelog.read_text(encoding="utf-8")
            entries = [line for line in content.splitlines() if line.startswith("- 2026-")]
            self.assertEqual(len(entries), 1)
            self.assertIn("reports/updates/U-20260710-001.md", content)

    def test_cli_writes_report_and_optional_changelog(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            update_path = root / "update.json"
            before_path = root / "before.json"
            after_path = root / "after.json"
            report_path = root / "report.md"
            changelog_path = root / "CHANGELOG.md"
            update_path.write_text(
                json.dumps(update_data(), ensure_ascii=False), encoding="utf-8"
            )
            write_bundle(before_path, before_bundle())
            write_bundle(after_path, after_bundle())
            result = main(
                [
                    "--update",
                    str(update_path),
                    "--before",
                    str(before_path),
                    "--after",
                    str(after_path),
                    "--report",
                    str(report_path),
                    "--changelog",
                    str(changelog_path),
                ]
            )
            self.assertEqual(result, 0)
            self.assertTrue(report_path.exists())
            self.assertTrue(changelog_path.exists())


if __name__ == "__main__":
    unittest.main()
