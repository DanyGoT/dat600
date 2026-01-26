import unittest
from main import insertion_sort, merge_sort, heap_sort, quick_sort

__unittest = True

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
        test(self, insertion_sort)

    def test_merge_sort(self):
        test(self, merge_sort)

    def test_heap_sort(self):
        test(self, heap_sort)

    def test_quick_sort(self):
        test(self, quick_sort)


def test(tester: TestSorting, sort_fn):
    fail = False
    try:
        sort_fn([])
    except NotImplementedError:
        fail = True
    if fail:
        tester.fail("NotImplemented")

    for case in (c.copy() for c in TEST_CASES):
        with tester.subTest(sort=sort_fn.__name__, input=case):
            got, _ = sort_fn(case)
            tester.assertEqual(got, sorted(case))
