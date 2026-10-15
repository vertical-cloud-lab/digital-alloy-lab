"""Directed acyclic graph (DAG) for function network models.

Ported from frazier-lab/partial_kgfn (MIT license).
Original: https://github.com/frazier-lab/partial_kgfn/blob/main/partial_kgfn/models/dag.py
"""

from __future__ import annotations


class DAG:
    """Directed acyclic graph representing a function network topology."""

    def __init__(self, parent_nodes: list[list[int]]) -> None:
        self.parent_nodes = parent_nodes
        self.n_nodes = len(parent_nodes)
        self.root_nodes = [
            k for k in range(self.n_nodes) if len(parent_nodes[k]) == 0
        ]

    def get_n_nodes(self) -> int:
        return self.n_nodes

    def get_parent_nodes(self, k: int) -> list[int]:
        return self.parent_nodes[k]

    def get_root_nodes(self) -> list[int]:
        return self.root_nodes
