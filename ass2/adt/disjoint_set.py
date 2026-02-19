#!/usr/bin/env python3
# pyright: basic

from __future__ import annotations


class DisjointSet:
    def __init__(self):
        self.parent: dict[int, int] = {}
        self.rank: dict[int, int] = {}

    def make_set(self, x: int):
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0

    def find_set(self, x: int) -> int:
        # Path compression
        if self.parent[x] != x:
            self.parent[x] = self.find_set(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int):
        rx, ry = self.find_set(x), self.find_set(y)
        if rx == ry:
            return

        # Union by rank
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[rx] > self.rank[ry]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1
