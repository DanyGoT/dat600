import unittest
from main import insertion_sort, merge_sort, heap_sort, quick_sort

SORT_FUNCTIONS = [insertion_sort, merge_sort, heap_sort, quick_sort]
TEST_CASES = [
    [],
    [1],
    [1, 2, 3],
    [3, 2, 1],
    [3, 1, 2, 1],
    [0, -1, 5, -3, 2],
]


class TestSorting(unittest.TestCase):
    def test_insertion_sort(self):
        sort_fn = insertion_sort
        try:
            sort_fn([])
        except NotImplementedError:
            self.fail("Not implemented")
        for case in (c.copy() for c in TEST_CASES):
            with self.subTest(sort=sort_fn.__name__, input=case):
                self.assertEqual(sort_fn(case), sorted(case))

    def test_merge_sort(self):
        sort_fn = merge_sort
        try:
            sort_fn([])
        except NotImplementedError:
            self.fail("Not implemented")
        for case in (c.copy() for c in TEST_CASES):
            if len(case) == 4:
                with self.subTest(sort=sort_fn.__name__, input=case):
                    self.assertEqual(sort_fn(case), sorted(case))

    def test_heap_sort(self):
        sort_fn = heap_sort
        try:
            sort_fn([])
        except NotImplementedError:
            self.fail("Not implemented")
        for case in (c.copy() for c in TEST_CASES):
            with self.subTest(sort=sort_fn.__name__, input=case):
                self.assertEqual(sort_fn(case), sorted(case))

    def test_quick_sort(self):
        sort_fn = quick_sort
        try:
            sort_fn([])
        except NotImplementedError:
            self.fail("Not implemented")
        for case in (c.copy() for c in TEST_CASES):
            with self.subTest(sort=sort_fn.__name__, input=case):
                self.assertEqual(sort_fn(case), sorted(case))
