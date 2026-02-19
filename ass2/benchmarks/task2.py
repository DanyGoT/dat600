#!/usr/bin/env python3
# pyright: basic

import time
import random
import math
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 16})
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from adt import DisjointSet


def benchmark_make_set(sizes: list[int], trials: int) -> list[float]:
    times = []
    for n in sizes:
        total = 0.0
        for _ in range(trials):
            ds = DisjointSet()
            elements = list(range(n))
            start = time.perf_counter()
            for x in elements:
                ds.make_set(x)
            total += time.perf_counter() - start
        times.append(total / (trials * n))
    return times


def benchmark_find_set(sizes: list[int], trials: int, ops: int) -> list[float]:
    times = []
    for n in sizes:
        ds = DisjointSet()
        for x in range(n):
            ds.make_set(x)
        # Create deeper trees with chain of unions
        elements = list(range(n))
        random.shuffle(elements)
        for i in range(n - 1):
            ds.union(elements[i], elements[i + 1])

        total = 0.0
        for _ in range(trials):
            targets = [random.randint(0, n - 1) for _ in range(ops)]
            start = time.perf_counter()
            for x in targets:
                ds.find_set(x)
            total += time.perf_counter() - start
        times.append(total / (trials * ops))
    return times


def benchmark_union(sizes: list[int], trials: int) -> list[float]:
    times = []
    for n in sizes:
        total = 0.0
        for _ in range(trials):
            ds = DisjointSet()
            for x in range(n):
                ds.make_set(x)
            elements = list(range(n))
            random.shuffle(elements)

            start = time.perf_counter()
            for i in range(n - 1):
                ds.union(elements[i], elements[i + 1])
            total += time.perf_counter() - start
        times.append(total / (trials * (n - 1)))
    return times


def main():
    sizes = list(range(100, 5001, 100))  # 100 to 5000, step 100 (50 points)
    trials = 15
    ops = 500

    print("Benchmarking make_set...")
    make_times = benchmark_make_set(sizes, trials)

    print("Benchmarking find_set...")
    find_times = benchmark_find_set(sizes, trials, ops)

    print("Benchmarking union...")
    union_times = benchmark_union(sizes, trials)

    # Scale reference to start at same point as measured (fair comparison)
    def scale_to_start(measured, reference):
        return measured[0] / reference[0]

    logn = [math.log2(n) for n in sizes]

    fig, axes = plt.subplots(1, 3, figsize=(14, 4))

    # make_set: Θ(1)
    ax = axes[0]
    ax.plot(sizes, make_times, 'o-', label='Measured', markersize=4)
    avg = sum(make_times) / len(make_times)
    ax.axhline(y=avg, linestyle='--', label='Θ(1) reference')
    ax.set_xlabel('n')
    ax.set_ylabel('Time per op (s)')
    ax.set_title('make_set()')
    ax.legend()

    # find_set: O(α(n)) << O(log n)
    ax = axes[1]
    ax.plot(sizes, find_times, 'o-', label='Measured (α(n))', markersize=4)
    scale = scale_to_start(find_times, logn)
    ax.plot(sizes, [l * scale for l in logn], '--', label='O(log n) reference')
    ax.set_xlabel('n')
    ax.set_ylabel('Time per op (s)')
    ax.set_title('find_set() — α(n) << log n')
    ax.legend()

    # union: O(α(n)) << O(log n)
    ax = axes[2]
    ax.plot(sizes, union_times, 'o-', label='Measured (α(n))', markersize=4)
    scale = scale_to_start(union_times, logn)
    ax.plot(sizes, [l * scale for l in logn], '--', label='O(log n) reference')
    ax.set_xlabel('n')
    ax.set_ylabel('Time per op (s)')
    ax.set_title('union() — α(n) << log n')
    ax.legend()

    plt.tight_layout()
    out = Path(__file__).parent / "task2.pdf"
    plt.savefig(out)
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
