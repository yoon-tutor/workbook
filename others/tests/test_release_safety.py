from __future__ import annotations

import json
import os
import stat
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from workbook_engine.manifest import ManifestBundle
from workbook_engine.release import (
    PUBLIC_FILENAMES,
    ReleaseError,
    _copy_public_artifact,
    _input_digests,
    _page_records,
    _render_update_index,
    _enforce_version_transitions,
    _sha256_file,
    allocate_output_dir,
    publish_release,
    prepare_release,
    release_status,
)
from workbook_engine.schema_gate import validate_schema


class ReleaseSafetyTests(unittest.TestCase):
    @unittest.skipUnless(
        hasattr(os, "chflags") and bool(getattr(stat, "UF_HIDDEN", 0)),
        "macOS file flags are required",
    )
    def test_public_copy_clears_hidden_file_flag(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "private-build.pdf"
            destination = root / "published.pdf"
            source.write_bytes(b"visible workbook artifact")
            os.chflags(source, source.stat().st_flags | stat.UF_HIDDEN)

            _copy_public_artifact(source, destination)

            self.assertEqual(source.read_bytes(), destination.read_bytes())
            self.assertTrue(source.stat().st_flags & stat.UF_HIDDEN)
            self.assertFalse(destination.stat().st_flags & stat.UF_HIDDEN)

    def test_content_change_requires_version_bump(self) -> None:
        root = Path(__file__).resolve().parents[1]
        canonical = json.loads((root / "workbooks" / "chocolate" / "content.json").read_text(encoding="utf-8"))
        changed = json.loads(json.dumps(canonical))
        changed["metadata"]["topic"] += " 변경"
        previous = ManifestBundle(
            canonical={"contentVersion": canonical["contentVersion"], "canonical": canonical},
            spec={},
            template={},
            build={},
        )
        with self.assertRaisesRegex(ReleaseError, "contentVersion bump"):
            _enforce_version_transitions(
                previous=previous,
                canonical=changed,
                spec=json.loads((root / "config" / "workbook-spec.json").read_text(encoding="utf-8")),
                versions=json.loads((root / "config" / "versions.json").read_text(encoding="utf-8")),
            )

    def test_update_index_preserves_multiple_workbooks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            detail = root / "reports" / "updates" / "U-20260710-999"
            detail.mkdir(parents=True)
            (detail / "book_one.md").write_text("first", encoding="utf-8")
            update = SimpleNamespace(
                update_id="U-20260710-999",
                title="공통 업데이트",
                summary="두 워크북 보고서를 보존합니다.",
                date="2026-07-10",
                apply_to="all",
            )
            with patch("workbook_engine.release.ROOT", root):
                index = _render_update_index(update, current_workbook_id="book-two")
            self.assertIn("book_one.md", index)
            self.assertIn("book_two.md", index)

    def test_prepare_happy_path_stays_private(self) -> None:
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as directory:
            build = Path(directory) / "prepared"
            build.mkdir()
            with patch("workbook_engine.release._build_directory", return_value=build), patch(
                "workbook_engine.release._previous_bundle", return_value=ManifestBundle.empty()
            ):
                result = prepare_release(
                    root / "workbooks" / "chocolate" / "content.json",
                    update_path=root / "updates" / "U-20260710-001.json",
                    output_base="safety_prepare",
                )
            self.assertEqual(22, result.page_count)
            self.assertTrue(all((build / name).is_file() for name in PUBLIC_FILENAMES))
            state = json.loads((build / "release-state.json").read_text(encoding="utf-8"))
            self.assertEqual("awaiting-visual-review", state["status"])
            self.assertTrue(state["inputDigests"])
            self.assertFalse((root / "outputs" / "safety_prepare").exists())

    def test_page_records_digest_each_real_edition(self) -> None:
        student = [{"pageId": "p01", "pageNo": 1, "no": "4", "part": "1-1", "mode": "writing", "items": [{"no": 1, "ko": "학생"}]}]
        answer = [{"pageId": "p01", "pageNo": 1, "no": "4", "part": "1-1", "mode": "writing", "items": [{"no": 1, "ko": "해설", "solutions": {"x": "정답"}}]}]
        records = _page_records(student, answer)
        self.assertEqual(2, len(records))
        self.assertNotEqual(records[0]["digest"], records[1]["digest"])

    def test_output_base_cannot_escape_outputs(self) -> None:
        for value in ("../escape", "/tmp/escape", "nested/name", ".."):
            with self.assertRaises(ReleaseError):
                allocate_output_dir(value)

    def test_update_schema_rejects_non_stage_objects(self) -> None:
        root = Path(__file__).resolve().parents[1]
        schema = json.loads((root / "schemas" / "update.schema.json").read_text(encoding="utf-8"))
        update = json.loads((root / "updates" / "U-20260710-001.json").read_text(encoding="utf-8"))
        update["affectedStages"] = [{"not": "a stage"}]
        self.assertTrue(validate_schema(update, schema))

    def test_publish_rejects_inputs_changed_after_prepare(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            build = root / "build"
            build.mkdir()
            canonical = root / "canonical.json"
            update = root / "update.json"
            canonical.write_text('{"workbookId":"safety-test","value":1}', encoding="utf-8")
            update.write_text('{"id":"U-20260710-999"}', encoding="utf-8")
            artifacts = {}
            for index, name in enumerate(PUBLIC_FILENAMES):
                path = build / name
                path.write_bytes((f"artifact-{index}" * 20).encode("utf-8"))
                artifacts[name] = {"sha256": _sha256_file(path), "size": path.stat().st_size}
            state = {
                "status": "awaiting-visual-review",
                "workbookId": "safety-test",
                "canonicalPath": str(canonical),
                "updatePath": str(update),
                "artifacts": artifacts,
                "inputDigests": _input_digests(canonical, update),
            }
            (build / "release-state.json").write_text(
                json.dumps(state), encoding="utf-8"
            )

            canonical.write_text('{"workbookId":"safety-test","value":2}', encoding="utf-8")
            with self.assertRaisesRegex(ReleaseError, "inputs changed after prepare"):
                publish_release(build, reviewer="test", notes="visual pass")

            status = release_status(canonical, build_dir=build)
            self.assertFalse(status["canPublish"])
            self.assertFalse(status["inputsCurrent"])
            self.assertTrue(status["changedInputs"])


if __name__ == "__main__":
    unittest.main()
