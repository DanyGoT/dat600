#!/usr/bin/env python3
# pyright: basic

from __future__ import annotations
from typing import Optional
from .element import Element


class Node:
    def __init__(self, element: Element):
        self.element = element
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None
        self.height: int = 1
