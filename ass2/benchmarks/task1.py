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
from adt import Element, Set


def benchmark_build(sizes: list[int], trials: int) -> list[float]:
    times = []
    for n in sizes:
        total = 0.0
        for _ in range(trials):
            elements = [Element(i, f"data{i}") for i in random.sample(range(n * 10), n)]
            s = Set()
            start = time.perf_counter()
            s.build(elements)
            total += time.perf_counter() - start
        times.append(total / trials)
    return times


def benchmark_find(sizes: list[int], trials: int, ops_per_trial: int) -> list[float]:
    """Measure time per single find operation at different tree sizes."""
    times = []
    for n in sizes:
        s = Set()
        keys = random.sample(range(n * 10), n)
        s.build([Element(k, f"data{k}") for k in keys])

        total = 0.0
        for _ in range(trials):
            targets = [random.choice(keys) for _ in range(ops_per_trial)]
            start = time.perf_counter()
            for k in targets:
                s.find(k)
            total += time.perf_counter() - start

        times.append(total / (trials * ops_per_trial))
    return times


def benchmark_insert(sizes: list[int], trials: int, ops_per_trial: int) -> list[float]:
    """Measure time per single insert operation at different tree sizes."""
    times = []
    for n in sizes:
        total = 0.0
        for _ in range(trials):
            s = Set()
            keys = random.sample(range(n * 10), n)
            s.build([Element(k, f"data{k}") for k in keys])

            # Insert new keys not in the tree
            new_keys = random.sample(range(n * 10, n * 20), ops_per_trial)
            start = time.perf_counter()
            for k in new_keys:
                s.insert(Element(k, f"data{k}"))
            total += time.perf_counter() - start

        times.append(total / (trials * ops_per_trial))
    return times


def main():
    sizes = list(range(100, 5001, 100))  # 100 to 5000, step 100 (50 points)
    trials = 15
    ops = 500

    print("Benchmarking build...")
    build_times = benchmark_build(sizes, trials)

    print("Benchmarking find...")
    find_times = benchmark_find(sizes, trials, ops)

    print("Benchmarking insert...")
    insert_times = benchmark_insert(sizes, trials, ops)

    # Least squares fit for scaling reference curves
    def fit_scale(measured, reference):
        num = sum(m * r for m, r in zip(measured, reference))
        den = sum(r * r for r in reference)
        return num / den

    # Plot
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))

    # Build: O(n log n)
    ax = axes[0]
    ax.plot(sizes, build_times, 'o-', label='Measured', markersize=4)
    nlogn = [n * math.log2(n) for n in sizes]
    scale = fit_scale(build_times, nlogn)
    ax.plot(sizes, [t * scale for t in nlogn], '--', label='O(n log n) reference')
    ax.set_xlabel('n')
    ax.set_ylabel('Time (s)')
    ax.set_title('build()')
    ax.legend()

    # Find: O(log n) per operation
    ax = axes[1]
    ax.plot(sizes, find_times, 'o-', label='Measured', markersize=4)
    logn = [math.log2(n) for n in sizes]
    scale = fit_scale(find_times, logn)
    ax.plot(sizes, [t * scale for t in logn], '--', label='O(log n) reference')
    ax.set_xlabel('n')
    ax.set_ylabel('Time per find (s)')
    ax.set_title('find()')
    ax.legend()

    # Insert: O(log n) per operation
    ax = axes[2]
    ax.plot(sizes, insert_times, 'o-', label='Measured', markersize=4)
    scale = fit_scale(insert_times, logn)
    ax.plot(sizes, [t * scale for t in logn], '--', label='O(log n) reference')
    ax.set_xlabel('n')
    ax.set_ylabel('Time per insert (s)')
    ax.set_title('insert()')
    ax.legend()

    plt.tight_layout()
    out = Path(__file__).parent / "task1.pdf"
    plt.savefig(out)
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
