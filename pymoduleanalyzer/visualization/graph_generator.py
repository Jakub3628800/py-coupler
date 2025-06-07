"""Generate simple dependency graphs using Graphviz."""

from pathlib import Path
from typing import Dict, List

try:
    import graphviz
except ImportError:  # pragma: no cover - optional dependency
    graphviz = None


def generate_dot(imports: Dict[Path, List[str]]) -> str:
    """Return DOT representation of the import graph."""
    dot_lines = ["digraph dependencies {"]
    for module, deps in imports.items():
        module_label = module.stem
        for dep in deps:
            dot_lines.append(f"    {module_label} -> \"{dep}\"")
    dot_lines.append("}")
    return "\n".join(dot_lines)


def generate_mermaid(imports: Dict[Path, List[str]]) -> str:
    """Return Mermaid flowchart representation of the import graph."""
    lines = ["flowchart TD"]
    for module, deps in imports.items():
        module_label = module.stem
        for dep in deps:
            lines.append(f"    {module_label} --> {dep}")
    return "\n".join(lines)
