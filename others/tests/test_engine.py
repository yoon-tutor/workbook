from __future__ import annotations

import json
import copy
import unittest
from pathlib import Path

from workbook_engine.compiler import (
    compile_workbook,
    lock_response_layout,
    lock_solution_slot_layouts,
    project_student_workbook,
)
from workbook_engine.migrate_legacy import migrate
from workbook_engine.schema_gate import validate_schema
from workbook_engine.validator import load_spec, validate_canonical, validate_compiled


ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "workbooks" / "chocolate" / "content.json"
LEGACY = ROOT / "tmp" / "build_chocolate_reading_json.py"


class EngineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.spec = load_spec()
        cls.canonical = json.loads(CANONICAL.read_text(encoding="utf-8"))

    def test_migration_is_deterministic(self) -> None:
        first = migrate(LEGACY)
        second = migrate(LEGACY)
        self.assertEqual(first, second)
        self.assertEqual(
            [item["source"] for item in first["sentences"]],
            [item["source"] for item in self.canonical["sentences"]],
        )

    def test_canonical_has_no_structural_errors(self) -> None:
        schema = json.loads(
            (ROOT / "schemas" / "canonical-workbook.schema.json").read_text(encoding="utf-8")
        )
        self.assertEqual([], [issue.format() for issue in validate_schema(self.canonical, schema)])
        issues = validate_canonical(self.canonical, self.spec)
        self.assertEqual([], [issue.format() for issue in issues if issue.severity == "error"])

    def test_meaning_and_arrange_reconstruct_source(self) -> None:
        for sentence in self.canonical["sentences"]:
            meaning = " ".join(segment["en"] for segment in sentence["meaningSegments"])
            arrange = " ".join(chunk["text"] for chunk in sentence["exercises"]["arrange"]["chunks"])
            self.assertEqual(sentence["source"], meaning, sentence["id"])
            self.assertEqual(sentence["source"], arrange, sentence["id"])

    def test_compile_has_exact_stage_coverage(self) -> None:
        for edition in ("student", "answer"):
            compiled = compile_workbook(self.canonical, edition, self.spec)
            self.assertEqual(22, len(compiled["pages"]))
            self.assertNotIn("steps", compiled)
            self.assertNotIn("sourceSentences", compiled)
            self.assertEqual(
                22, len({page["pageId"] for page in compiled["pages"]})
            )
            self.assertEqual([], validate_compiled(compiled, 24))

    def test_student_projection_contains_no_answers(self) -> None:
        compiled = compile_workbook(self.canonical, "student", self.spec)
        for page in compiled["pages"]:
            self.assertNotIn("corrections", page)
            self.assertNotIn("sequenceAnswer", page)
            for key in ("items", "units"):
                for item in page.get(key, []):
                    self.assertEqual({}, item.get("solutions", {}))
                    self.assertNotIn("solutionText", item)

    def test_answer_projection_retains_answer_data(self) -> None:
        compiled = compile_workbook(self.canonical, "answer", self.spec)
        solution_count = sum(
            len(item.get("solutions", {}))
            for page in compiled["pages"]
            for key in ("items", "units")
            for item in page.get(key, [])
        )
        self.assertGreater(solution_count, 200)
        self.assertTrue(any(page.get("corrections") for page in compiled["pages"]))
        self.assertTrue(any(page.get("sequenceAnswer") for page in compiled["pages"]))

    def test_student_is_projected_from_answer_layout(self) -> None:
        answer = compile_workbook(self.canonical, "answer", self.spec)
        writing_targets = {
            item["responseTargetId"]: {
                "boxHeightPx": 48.25 + index,
                "lines": [
                    {
                        "leftPx": 3.75,
                        "topPx": 12.5,
                        "widthPx": 180.5 + index,
                        "heightPx": 17.6,
                    }
                ],
            }
            for index, item in enumerate(
                item
                for page in answer["pages"]
                if page.get("mode") == "writing"
                for item in page.get("items", [])
            )
        }
        locked_answer = lock_response_layout(answer, writing_targets)
        locked_answer = lock_solution_slot_layouts(
            locked_answer,
            {
                "inline-answer-1": {"widthPx": 81.25, "heightPx": 17.5},
                "inline-answer-2": {"widthPx": 124.75, "heightPx": 18.25},
            },
        )
        student = project_student_workbook(
            locked_answer,
            expected_sentences=len(self.canonical["sentences"]),
        )
        answer_items = [
            item
            for page in locked_answer["pages"]
            if page.get("mode") == "writing"
            for item in page.get("items", [])
        ]
        student_items = [
            item
            for page in student["pages"]
            if page.get("mode") == "writing"
            for item in page.get("items", [])
        ]
        self.assertEqual("answer", locked_answer["edition"])
        self.assertEqual("student", student["edition"])
        self.assertEqual(len(answer_items), len(student_items))
        self.assertEqual(
            locked_answer["solutionSlotLayouts"],
            student["solutionSlotLayouts"],
        )
        for answer_item, student_item in zip(answer_items, student_items):
            self.assertEqual(answer_item["answerHeight"], student_item["answerHeight"])
            self.assertEqual(answer_item["responseLayout"], student_item["responseLayout"])
            self.assertTrue(student_item["keepAnswerHeight"])
            self.assertEqual({}, student_item["solutions"])
            self.assertNotIn("solutionText", student_item)

    def test_stage8_uses_only_the_full_sentence_response_area(self) -> None:
        for edition in ("student", "answer"):
            compiled = compile_workbook(self.canonical, edition, self.spec)
            stage8_items = [
                item
                for page in compiled["pages"]
                if str(page["no"]) == "8"
                for item in page["items"]
            ]
            self.assertEqual(len(self.canonical["sentences"]), len(stage8_items))
            for sentence, item in zip(self.canonical["sentences"], stage8_items):
                self.assertNotIn("en", item)
                self.assertNotIn("arrange-slot", json.dumps(item, ensure_ascii=False))
                self.assertEqual(
                    f"{sentence['id']}-arrange-response",
                    item["responseTargetId"],
                )
                if edition == "student":
                    self.assertEqual({}, item["solutions"])
                else:
                    self.assertEqual(
                        {item["responseTargetId"]: sentence.get("display") or sentence["source"]},
                        item["solutions"],
                    )

    def test_separate_passages_are_arranged_without_other_passage_text(self) -> None:
        canonical = copy.deepcopy(self.canonical)
        sentences = canonical["sentences"]
        activities = []
        for index, (start, end) in enumerate(((0, 12), (12, 24)), start=1):
            passage_ids = [sentence["id"] for sentence in sentences[start:end]]
            activities.append({
                "id": f"paragraph-order-{index:02d}",
                "blocks": [
                    {"id": label, "sentenceIds": passage_ids[offset:offset + 4]}
                    for label, offset in (("A", 0), ("B", 4), ("C", 8))
                ],
                "displayOrder": ["C", "B", "A"],
                "answerOrder": ["A", "B", "C"],
            })
        canonical["passageActivities"]["paragraphOrder"] = activities
        self.assertEqual([], validate_canonical(canonical, self.spec))
        compiled = compile_workbook(canonical, "answer", self.spec)
        stage_nine = [page for page in compiled["pages"] if str(page["no"]) == "9"]
        self.assertEqual(2, len(stage_nine))
        first_text = " ".join(block["text"] for block in stage_nine[0]["blocks"])
        self.assertIn(sentences[0]["source"], first_text)
        self.assertNotIn(sentences[12]["source"], first_text)

        activities[1]["blocks"][0]["sentenceIds"][0] = sentences[0]["id"]
        codes = {issue.code for issue in validate_canonical(canonical, self.spec)}
        self.assertIn("paragraph.coverage", codes)

    def test_all_declared_passage_activities_are_compiled(self) -> None:
        canonical = copy.deepcopy(self.canonical)
        correction = copy.deepcopy(canonical["passageActivities"]["correction"][0])
        correction["id"] = "correction-02"
        for target in correction["targets"]:
            target["id"] = target["id"].replace("correction-01", "correction-02")
        canonical["passageActivities"]["correction"].append(correction)
        paragraph = copy.deepcopy(canonical["passageActivities"]["paragraphOrder"][0])
        paragraph["id"] = "paragraph-order-02"
        canonical["passageActivities"]["paragraphOrder"].append(paragraph)
        self.assertEqual([], validate_canonical(canonical, self.spec))
        compiled = compile_workbook(canonical, "answer", self.spec)
        self.assertEqual(24, len(compiled["pages"]))
        self.assertEqual(2, sum(str(page["no"]) == "7" for page in compiled["pages"]))
        self.assertEqual(2, sum(str(page["no"]) == "9" for page in compiled["pages"]))

    def test_passage_activities_cannot_be_empty(self) -> None:
        canonical = copy.deepcopy(self.canonical)
        canonical["passageActivities"]["correction"] = []
        canonical["passageActivities"]["paragraphOrder"] = []
        codes = {issue.code for issue in validate_canonical(canonical, self.spec)}
        self.assertIn("correction.empty", codes)
        self.assertIn("paragraph.empty", codes)

    def test_default_exercises_do_not_duplicate_canonical_text(self) -> None:
        overrides = []
        for sentence in self.canonical["sentences"]:
            for name in ("koBlank", "enBlank", "verb", "choice"):
                exercise = sentence["exercises"][name]
                if "baseText" in exercise:
                    overrides.append((sentence["no"], name, exercise.get("overrideReason")))
        self.assertEqual([(1, "verb", "원문이 동사 없는 헤드라인 조각이므로 승인된 완전문장으로 동사형 연습을 구성함")], overrides)


if __name__ == "__main__":
    unittest.main()
