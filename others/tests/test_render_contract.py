from __future__ import annotations

import json
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from workbook_engine.compiler import (
    compile_workbook,
    lock_response_layout,
    lock_solution_slot_layouts,
    project_student_workbook,
)
from workbook_engine.qa import (
    find_chrome,
    measure_answer_layouts,
    require_shared_structure,
    snapshot_dom,
)
from workbook_engine.render import build_html


ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "workbooks" / "chocolate" / "content.json"


class RenderContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.canonical = json.loads(CANONICAL.read_text(encoding="utf-8"))

    def test_release_html_is_self_contained_and_not_duplicated(self) -> None:
        compiled = compile_workbook(self.canonical, "student")
        html = build_html(compiled)
        self.assertIn("data-workbook-payload", html)
        self.assertIn("data-workbook-renderer", html)
        self.assertNotIn('src="./renderer.js"', html)
        self.assertNotIn('href="./workbook.css"', html)
        self.assertNotIn('"steps":', html)
        for marker in ("__DOCUMENT_TITLE__", "__SCREEN_TITLE__", "__WORKSHEETS__"):
            self.assertNotIn(marker, html)

    def test_real_browser_student_answer_contract(self) -> None:
        try:
            find_chrome()
        except Exception as error:  # pragma: no cover - platform skip
            self.skipTest(str(error))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            answer_compiled = compile_workbook(self.canonical, "answer")
            draft_answer = root / "answer-draft.html"
            draft_answer.write_text(build_html(answer_compiled), encoding="utf-8")
            measured_layouts = measure_answer_layouts(
                draft_answer,
                expected_pages=22,
                profile_root=root / "layout-profiles",
            )
            answer_compiled = lock_response_layout(
                answer_compiled,
                measured_layouts["responses"],
            )
            answer_compiled = lock_solution_slot_layouts(
                answer_compiled,
                measured_layouts["solutionSlots"],
            )
            student_compiled = project_student_workbook(
                answer_compiled,
                expected_sentences=len(self.canonical["sentences"]),
            )
            for edition, compiled in (
                ("student", student_compiled),
                ("answer", answer_compiled),
            ):
                (root / f"{edition}.html").write_text(build_html(compiled), encoding="utf-8")
            _, student = snapshot_dom(
                root / "student.html",
                edition="student",
                expected_pages=22,
                profile_root=root / "profiles",
            )
            _, answer = snapshot_dom(
                root / "answer.html",
                edition="answer",
                expected_pages=22,
                profile_root=root / "profiles",
            )
            require_shared_structure(student, answer)
            with self.assertRaisesRegex(Exception, "normalized problem DOM differs"):
                require_shared_structure(student, replace(answer, structure_digest="different"))
            self.assertEqual(0, student.solution_count)
            self.assertGreater(answer.solution_count, 200)
            self.assertEqual(student.response_box_heights, answer.response_box_heights)
            self.assertEqual(student.solution_slot_layouts, answer.solution_slot_layouts)
            self.assertEqual(
                [target_id for target_id, _lines in student.response_line_layouts],
                [target_id for target_id, _lines in answer.response_line_layouts],
            )


if __name__ == "__main__":
    unittest.main()
