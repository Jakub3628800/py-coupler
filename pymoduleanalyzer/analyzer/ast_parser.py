"""Lightweight AST parser utilities."""

import ast
from pathlib import Path
from typing import List


def parse_imports(path: Path) -> List[ast.AST]:
    """Return import nodes from the given Python file."""
    tree = ast.parse(path.read_text())
    return [node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]
