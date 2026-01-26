from typing import List, Tuple


def insertion_sort(arr: List[int]) -> Tuple[List[int], int]:
    steps = 0
    for j in range(1, len(arr)):
        key = arr[j]
        i = j - 1
        while i >= 0 and arr[i] > key:
            arr[i + 1] = arr[i]
            i = i - 1
            steps += 1
        arr[i + 1] = key
        steps += 1
    return (arr, steps)


def merge_sort(arr: List[int], p=1, r=None) -> Tuple[List[int], int]:
    steps = 0
    if r is None:
        r = len(arr)

    if p < r:
        q = (p + r) // 2
        arr, s = merge_sort(arr, p, q)
        steps += s
        arr, s = merge_sort(arr, q + 1, r)
        steps += s
        arr, s = merge(arr, p, q, r)
        steps += s

    return (arr, steps)


def merge(arr: List[int], p, q, r) -> Tuple[List[int], int]:
    steps = 0
    n1 = q - p + 1
    n2 = r - q
    left = arr[p - 1 : q]
    right = arr[q:r]

    i = 0
    j = 0
    for k in range(p - 1, r):
        if i < n1 and (j > n2 - 1 or left[i] <= right[j]):
            arr[k] = left[i]
            i = i + 1
        else:
            arr[k] = right[j]
            j = j + 1
        steps += 1

    return (arr, steps)


def heap_sort(arr: List[int]) -> Tuple[List[int], int]:
    steps = 1
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        arr, s = max_heapify(arr, n, i)
        steps += s

    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        arr, s = max_heapify(arr, i, 0)
        steps += s

    return (arr, steps)


def max_heapify(arr: List[int], n: int, i: int) -> Tuple[List[int], int]:
    steps = 1
    max = i

    left_node = 2 * i + 1
    right_node = 2 * i + 2

    if left_node < n and arr[left_node] > arr[max]:
        max = left_node
    if right_node < n and arr[right_node] > arr[max]:
        max = right_node

    if max != i:
        arr[i], arr[max] = arr[max], arr[i]
        arr, s = max_heapify(arr, n, max)
        steps += s

    return (arr, steps)


def quick_sort(
    arr: List[int], start: int = 0, pivot_point: int = -1
) -> Tuple[List[int], int]:
    steps = 1
    if arr == []:
        return (arr, steps)

    i = start
    j = i

    if pivot_point == -1:
        pivot_point = len(arr) - 1
    pivot = arr[pivot_point]

    while j < pivot_point:
        if arr[j] < pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
        j += 1
        steps += 1

    arr[i], arr[pivot_point] = arr[pivot_point], arr[i]

    if start < i - 1:
        _, s = quick_sort(arr, start, i - 1)
        steps += s
    if i + 1 < pivot_point:
        _, s = quick_sort(arr, i + 1, pivot_point)
        steps += s

    return (arr, steps)
