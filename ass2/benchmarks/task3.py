#!/usr/bin/env python3
# pyright: basic

import time
import random
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 16})
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from adt.knapsack import (
    knapsack_naive,
    knapsack_memoization,
    knapsack_tabulation,
    knapsack_greedy,
)


def generate_instance(n: int, max_weight: int = 20, max_value: int = 100):
    weights = [random.randint(1, max_weight) for _ in range(n)]
    values = [random.randint(1, max_value) for _ in range(n)]
    capacity = min(50 + n * 2, 500)
    return weights, values, capacity


def benchmark(fn, weights, values, capacity, trials: int = 3) -> float:
    total = 0.0
    for _ in range(trials):
        start = time.perf_counter()
        fn(weights, values, capacity)
        total += time.perf_counter() - start
    return total / trials


def main():
    random.seed(42)

    # Naive is O(2^n), so keep n small
    naive_sizes = list(range(5, 23))
    # DP and greedy can handle larger n
    dp_sizes = list(range(10, 201, 5))

    print("Benchmarking naive recursion (small n only)...")
    naive_times = []
    for n in naive_sizes:
        w, v, c = generate_instance(n)
        t = benchmark(knapsack_naive, w, v, c, trials=3)
        naive_times.append(t)
        print(f"  n={n}: {t:.4f}s")

    print("Benchmarking memoization...")
    memo_times = []
    for n in dp_sizes:
        w, v, c = generate_instance(n)
        t = benchmark(knapsack_memoization, w, v, c, trials=5)
        memo_times.append(t)

    print("Benchmarking tabulation...")
    tab_times = []
    for n in dp_sizes:
        w, v, c = generate_instance(n)
        t = benchmark(knapsack_tabulation, w, v, c, trials=5)
        tab_times.append(t)

    print("Benchmarking greedy...")
    greedy_times = []
    for n in dp_sizes:
        w, v, c = generate_instance(n)
        t = benchmark(knapsack_greedy, w, v, c, trials=5)
        greedy_times.append(t)

    # Show that greedy gives wrong answer
    print("\nGreedy vs Optimal comparison:")
    w, v, c = [10, 20, 30], [60, 100, 120], 50
    optimal = knapsack_tabulation(w, v, c)
    greedy = knapsack_greedy(w, v, c)
    print(f"  weights={w}, values={v}, capacity={c}")
    print(f"  Optimal (DP): {optimal}")
    print(f"  Greedy:       {greedy} {'(wrong!)' if greedy != optimal else ''}")

    # Plot
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    # Naive: O(2^n)
    ax = axes[0]
    ax.plot(naive_sizes, naive_times, 'o-', label='Naive O(2^n)', markersize=4)
    ax.set_xlabel('n')
    ax.set_ylabel('Time (s)')
    ax.set_title('Naive Recursion (exponential)')
    ax.legend()

    # DP vs Greedy
    ax = axes[1]
    ax.plot(dp_sizes, memo_times, 'o-', label='Memoization', markersize=3)
    ax.plot(dp_sizes, tab_times, 's-', label='Tabulation', markersize=3)
    ax.plot(dp_sizes, greedy_times, '^-', label='Greedy', markersize=3)
    ax.set_xlabel('n')
    ax.set_ylabel('Time (s)')
    ax.set_title('DP vs Greedy (polynomial)')
    ax.legend()

    plt.tight_layout()
    out = Path(__file__).parent / "task3.pdf"
    plt.savefig(out)
    print(f"\nSaved {out}")


if __name__ == "__main__":
    main()
