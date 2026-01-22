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

def merge_sort(arr: List[int]) -> List[int]:
    raise NotImplementedError


def heap_sort(arr: List[int]):
    raise NotImplementedError


def quick_sort(arr: List[int]):
    raise NotImplementedError
