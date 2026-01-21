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
    def test_sort_correct(self):
        for sort_fn in SORT_FUNCTIONS:
            for case in TEST_CASES:
                with self.subTest(sort=sort_fn.__name__, input=case):
                    self.assertEqual(sort_fn(case), sorted(case))
