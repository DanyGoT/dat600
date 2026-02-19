#!/usr/bin/env python3
# pyright: basic

from __future__ import annotations


class Element:
    def __init__(self, key: int, data):
        self.key = key
        self.data = data

    def __repr__(self):
        return f"Element(key={self.key}, data={self.data})"
