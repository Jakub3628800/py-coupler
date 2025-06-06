"""Placeholder for encapsulation analysis."""

from pathlib import Path
from typing import List

import ast


def private_method_ratio(path: Path) -> float:
    """Return ratio of private to total methods in a file."""
    tree = ast.parse(path.read_text())
    methods = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    if not methods:
        return 0.0
    private = [m for m in methods if m.startswith('_')]
    return len(private) / len(methods)
