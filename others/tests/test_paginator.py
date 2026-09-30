from __future__ import annotations

import unittest

from workbook_engine.paginator import balanced_chunks, paginate_stage


class PaginatorTests(unittest.TestCase):
    def test_balances_21_items_across_two_pages_with_a_maximum_of_11(self) -> None:
        items = list(range(1, 22))
        pages = list(balanced_chunks(items, 11))
        self.assertEqual([11, 10], [len(page_items) for _, page_items in pages])
        self.assertEqual([(0, items[:11]), (11, items[11:])], pages)

    def test_avoids_a_singleton_tail(self) -> None:
        items = list(range(1, 14))
        pages = list(balanced_chunks(items, 11))
        self.assertEqual([7, 6], [len(page_items) for _, page_items in pages])

    def test_paginated_parts_are_continuous_and_balanced(self) -> None:
        stage = {"no": "4", "items": [{"no": value} for value in range(1, 22)]}
        spec = {
            "logicalStages": [
                {
                    "number": 4,
                    "pagination": {"targetPerPage": 10, "hardMaximum": 11},
                }
            ]
        }
        pages = paginate_stage(stage, spec)
        self.assertEqual(["1-11", "12-21"], [page["part"] for page in pages])
        self.assertEqual([11, 10], [len(page["items"]) for page in pages])
        self.assertTrue(all(page["pageItemMaximum"] == 11 for page in pages))


if __name__ == "__main__":
    unittest.main()
