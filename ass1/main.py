from typing import List


def insertion_sort(arr: List[int]) -> List[int]:
    for j in range(1, len(arr)):
        key = arr[j]
        i = j - 1
        while i >= 0 and arr[i] > key:
            arr[i + 1] = arr[i]
            i = i - 1
        arr[i + 1] = key
    return arr


def merge_sort(arr: List[int], p=1, r=None) -> List[int]:
    if r is None:
        r = len(arr)

    if p < r:
        q = (p + r) // 2
        arr = merge_sort(arr, p, q)
        arr = merge_sort(arr, q + 1, r)
        merge(arr, p, q, r)
    return arr


def merge(arr: List[int], p, q, r) -> List[int]:
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
    return arr


def heap_sort(arr: List[int]):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        arr = max_heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        arr = max_heapify(arr, i, 0)
    return arr


def max_heapify(arr: List[int], n: int, i: int):
    max = i

    left_node = 2 * i + 1
    right_node = 2 * i + 2

    if left_node < n and arr[left_node] > arr[max]:
        max = left_node
    if right_node < n and arr[right_node] > arr[max]:
        max = right_node

    if max != i:
        arr[i], arr[max] = arr[max], arr[i]
        arr = max_heapify(arr, n, max)
    return arr


def quick_sort(arr: List[int]):
    raise NotImplementedError
