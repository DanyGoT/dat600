#!/usr/bin/env python3
# pyright: basic

from __future__ import annotations
from typing import Optional
from .element import Element
from .node import Node


class Set:
    def __init__(self):
        self.root: Optional[Node] = None

    def build(self, elements: list[Element]):
        for e in elements:
            self.insert(e)

    # AVL tree helpers

    def _height(self, node: Optional[Node]) -> int:
        return node.height if node else 0

    def _balance_factor(self, node: Node) -> int:
        return self._height(node.left) - self._height(node.right)

    def _update_height(self, node: Node):
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _rotate_right(self, y: Node) -> Node:
        x = y.left
        assert x is not None
        t2 = x.right

        x.right = y
        y.left = t2

        self._update_height(y)
        self._update_height(x)
        return x

    def _rotate_left(self, x: Node) -> Node:
        y = x.right
        assert y is not None
        t2 = y.left

        y.left = x
        x.right = t2

        self._update_height(x)
        self._update_height(y)
        return y

    def _rebalance(self, node: Node) -> Node:
        self._update_height(node)
        balance = self._balance_factor(node)

        # Left heavy
        if balance > 1:
            assert node.left is not None
            if self._balance_factor(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Right heavy
        if balance < -1:
            assert node.right is not None
            if self._balance_factor(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    # Insert

    def insert(self, element: Element):
        self.root = self._insert(self.root, element)

    def _insert(self, node: Optional[Node], element: Element) -> Node:
        if node is None:
            return Node(element)

        if element.key < node.element.key:
            node.left = self._insert(node.left, element)
        elif element.key > node.element.key:
            node.right = self._insert(node.right, element)
        else:
            return node  # duplicate key

        return self._rebalance(node)

    # Find

    def find(self, k: int) -> tuple[int | None, object | None, bool]:
        node = self._find(self.root, k)
        if node is None:
            return None, None, False
        return node.element.key, node.element.data, True

    def _find(self, node: Optional[Node], k: int) -> Optional[Node]:
        if node is None:
            return None
        if k == node.element.key:
            return node
        elif k < node.element.key:
            return self._find(node.left, k)
        else:
            return self._find(node.right, k)

    # Delete

    def delete(self, k: int):
        self.root = self._delete(self.root, k)

    def _delete(self, node: Optional[Node], k: int) -> Optional[Node]:
        if node is None:
            return None

        if k < node.element.key:
            node.left = self._delete(node.left, k)
        elif k > node.element.key:
            node.right = self._delete(node.right, k)
        else:
            # Found node to delete
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left

            # Two children: replace with in-order successor
            successor = self._min_node(node.right)
            node.element = successor.element
            node.right = self._delete(node.right, successor.element.key)

        return self._rebalance(node)

    # Min / Max

    def find_min(self) -> tuple[int | None, object | None, bool]:
        if self.root is None:
            return None, None, False
        node = self._min_node(self.root)
        return node.element.key, node.element.data, True

    def _min_node(self, node: Node) -> Node:
        while node.left is not None:
            node = node.left
        return node

    def find_max(self) -> tuple[int | None, object | None, bool]:
        if self.root is None:
            return None, None, False
        node = self._max_node(self.root)
        return node.element.key, node.element.data, True

    def _max_node(self, node: Node) -> Node:
        while node.right is not None:
            node = node.right
        return node

    # Prev / Next

    def find_prev(self, k: int) -> tuple[int | None, object | None, bool]:
        """Find element with largest key less than k."""
        result: Optional[Node] = None
        node = self.root

        while node is not None:
            if node.element.key < k:
                result = node
                node = node.right
            else:
                node = node.left

        if result is None:
            return None, None, False
        return result.element.key, result.element.data, True

    def find_next(self, k: int) -> tuple[int | None, object | None, bool]:
        """Find element with smallest key greater than k."""
        result: Optional[Node] = None
        node = self.root

        while node is not None:
            if node.element.key > k:
                result = node
                node = node.left
            else:
                node = node.right

        if result is None:
            return None, None, False
        return result.element.key, result.element.data, True
