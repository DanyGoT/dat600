#!/usr/bin/env python3
# pyright: basic

"""
0/1 Knapsack Problem

Recursive relation:
    knapsack(i, w) = max(
        knapsack(i-1, w),                           # don't take item i
        values[i] + knapsack(i-1, w - weights[i])   # take item i (if weights[i] <= w)
    )

Base case: knapsack(i, w) = 0 if i < 0 or w <= 0
"""

from __future__ import annotations


def knapsack_naive(weights: list[int], values: list[int], capacity: int) -> int:
    """Naive recursive solution - O(2^n)"""
    def recurse(i: int, w: int) -> int:
        if i < 0 or w <= 0:
            return 0
        if weights[i] > w:
            return recurse(i - 1, w)
        return max(
            recurse(i - 1, w),
            values[i] + recurse(i - 1, w - weights[i])
        )
    return recurse(len(weights) - 1, capacity)


def knapsack_memoization(weights: list[int], values: list[int], capacity: int) -> int:
    """Top-down DP with memoization - O(n * capacity)"""
    memo: dict[tuple[int, int], int] = {}

    def recurse(i: int, w: int) -> int:
        if i < 0 or w <= 0:
            return 0
        if (i, w) in memo:
            return memo[(i, w)]

        if weights[i] > w:
            result = recurse(i - 1, w)
        else:
            result = max(
                recurse(i - 1, w),
                values[i] + recurse(i - 1, w - weights[i])
            )
        memo[(i, w)] = result
        return result

    return recurse(len(weights) - 1, capacity)


def knapsack_tabulation(weights: list[int], values: list[int], capacity: int) -> int:
    """Bottom-up DP with tabulation - O(n * capacity)"""
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]  # don't take
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i][w], values[i - 1] + dp[i - 1][w - weights[i - 1]])

    return dp[n][capacity]


def knapsack_greedy(weights: list[int], values: list[int], capacity: int) -> int:
    """
    Greedy by value/weight ratio - O(n log n)

    NOTE: This does NOT give optimal solution for 0/1 knapsack!
    Greedy works for fractional knapsack, but not when items must be taken whole.
    """
    n = len(weights)
    # Sort by value-to-weight ratio (descending)
    items = sorted(range(n), key=lambda i: values[i] / weights[i], reverse=True)

    total = 0
    remaining = capacity
    for i in items:
        if weights[i] <= remaining:
            total += values[i]
            remaining -= weights[i]
    return total
