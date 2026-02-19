#!/usr/bin/env python3
# pyright: basic

from adt import Element, Set, DisjointSet


def demo_set():
    print("=== Set ADT ===")
    s = Set()
    elements = [Element(5, "five"), Element(3, "three"), Element(7, "seven"), Element(1, "one"), Element(9, "nine")]
    s.build(elements)

    print("find(3):", s.find(3))
    print("find_min():", s.find_min())
    print("find_max():", s.find_max())
    print("find_prev(5):", s.find_prev(5))
    print("find_next(5):", s.find_next(5))

    s.insert(Element(6, "six"))
    print("After insert(6), find(6):", s.find(6))

    s.delete(3)
    print("After delete(3), find(3):", s.find(3))


def demo_disjoint_set():
    print("\n=== Disjoint Set ADT ===")
    ds = DisjointSet()

    for i in range(6):
        ds.make_set(i)

    ds.union(0, 1)
    ds.union(2, 3)
    ds.union(0, 2)

    print("find_set(0):", ds.find_set(0))
    print("find_set(3):", ds.find_set(3))
    print("0 and 3 same set:", ds.find_set(0) == ds.find_set(3))
    print("0 and 5 same set:", ds.find_set(0) == ds.find_set(5))


if __name__ == "__main__":
    demo_set()
    demo_disjoint_set()
