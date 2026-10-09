from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from support import CONTENT, SERVER

from workbook_authoring import AuthoringPacketError, compact_canonical, expand_packet, verify_new_packet_policy
from workbook_engine.compiler import compile_workbook
from workbook_engine.validator import load_spec


ROOT = CONTENT
REFERENCE = ROOT / "workbooks" / "2026-june-grade2-q23" / "content.json"
BASELINE = SERVER / "config" / "canonical-content-baseline.json"


class AuthoringPacketTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.canonical = json.loads(REFERENCE.read_text(encoding="utf-8"))
        cls.spec = load_spec()

    def test_existing_reviewed_content_is_byte_locked(self) -> None:
        baseline = json.loads(BASELINE.read_text(encoding="utf-8"))["sha256"]
        current = {path.relative_to(ROOT).as_posix() for path in ROOT.glob("workbooks/*/content.json")}
        self.assertTrue(set(baseline).issubset(current))
        for relative, expected in baseline.items():
            digest = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
            self.assertEqual(expected, digest, relative)

    def test_current_reference_round_trips_without_any_change(self) -> None:
        packet = compact_canonical(self.canonical)
        self.assertEqual(self.canonical, expand_packet(packet))

    def test_compiled_student_and_answer_views_are_unchanged(self) -> None:
        roundtrip = expand_packet(compact_canonical(self.canonical))
        for edition in ("student", "answer"):
            self.assertEqual(
                compile_workbook(self.canonical, edition, self.spec),
                compile_workbook(roundtrip, edition, self.spec),
            )

    def test_packet_removes_mechanical_sentence_and_target_ids(self) -> None:
        packet = compact_canonical(self.canonical)
        first = packet["sentences"][0]
        self.assertNotIn("id", first)
        self.assertNotIn("no", first)
        self.assertNotIn("id", first["meaningSegments"][0])
        self.assertIsInstance(first["exercises"]["enBlank"]["targets"][0], str)
        self.assertEqual([3, 1, 4, 2], first["exercises"]["arrange"]["displayOrder"])

    def test_repeated_shorthand_target_is_rejected_instead_of_guessed(self) -> None:
        packet = compact_canonical(self.canonical)
        packet["sentences"][0]["exercises"]["enBlank"]["targets"][0] = "a"
        with self.assertRaisesRegex(AuthoringPacketError, "must occur exactly once"):
            expand_packet(packet)

    def test_new_stage9_choices_are_alphabetical_and_answers_are_shuffled(self) -> None:
        def activity(answer):
            return {"blocks": [[1], [2], [3]], "displayOrder": [1, 2, 3],
                    "answerOrder": answer, "fixedIntroSentenceIds": [], "fixedOutroSentenceIds": []}

        packet = {"passageActivities": {"paragraphOrder": [
            activity([3, 1, 2]), activity([2, 1, 3]), activity([2, 3, 1]),
            activity([3, 2, 1]), activity([1, 3, 2]),
        ]}}
        verify_new_packet_policy(packet)

        packet["passageActivities"]["paragraphOrder"][0]["displayOrder"] = [3, 2, 1]
        with self.assertRaisesRegex(AuthoringPacketError, "print labels in A, B, C order"):
            verify_new_packet_policy(packet)
        packet["passageActivities"]["paragraphOrder"][0]["displayOrder"] = [1, 2, 3]

        packet["passageActivities"]["paragraphOrder"][0]["answerOrder"] = [1, 2, 3]
        with self.assertRaisesRegex(AuthoringPacketError, "not a meaningful arrangement"):
            verify_new_packet_policy(packet)
        packet["passageActivities"]["paragraphOrder"][0]["answerOrder"] = [3, 1, 2]

        packet["passageActivities"]["paragraphOrder"][1]["answerOrder"] = [3, 1, 2]
        with self.assertRaisesRegex(AuthoringPacketError, "vary answerOrder"):
            verify_new_packet_policy(packet)

        packet["passageActivities"]["paragraphOrder"][1]["answerOrder"] = [2, 1, 3]
        packet["passageActivities"]["paragraphOrder"].append(activity([3, 1, 2]))
        verify_new_packet_policy(packet)  # Six questions can use all five non-ABC orders.
        packet["passageActivities"]["paragraphOrder"][4]["answerOrder"] = [3, 1, 2]
        with self.assertRaisesRegex(AuthoringPacketError, "vary answerOrder"):
            verify_new_packet_policy(packet)

    def test_new_stage9_requires_all_text_in_movable_blocks(self) -> None:
        packet = {"passageActivities": {"paragraphOrder": [{
            "blocks": [[2], [3], [4]], "displayOrder": [1, 2, 3],
            "answerOrder": [3, 1, 2], "fixedIntroSentenceIds": ["s001"],
        }]}}
        with self.assertRaisesRegex(AuthoringPacketError, "entire passage in blocks"):
            verify_new_packet_policy(packet)


if __name__ == "__main__":
    unittest.main()
