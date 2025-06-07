"""Stub for method and function analysis."""

from pathlib import Path
from typing import Dict, List

import ast


def list_defined_functions(path: Path) -> List[str]:
    """Return a list of defined function names within the file."""
    tree = ast.parse(path.read_text())
    return [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
