"""Analyze import relationships between modules."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Dict, List

from .ast_parser import parse_imports


def analyze_imports(modules: List[Path]) -> Dict[Path, List[str]]:
    """Return mapping of modules to list of full import names including what's imported."""
    result: Dict[Path, List[str]] = {}
    for module in modules:
        found: List[str] = []
        for node in parse_imports(module):
            if isinstance(node, ast.ImportFrom):
                base = node.module or ""
                if node.level:
                    # Relative imports
                    base = "." * node.level + base
                
                # Add specific imports from the module
                if node.names:
                    for alias in node.names:
                        if alias.name == "*":
                            # Handle wildcard imports
                            found.append(f"{base}.*")
                        else:
                            # Full qualified name
                            if base:
                                found.append(f"{base}.{alias.name}")
                            else:
                                found.append(alias.name)
                else:
                    # Just the module itself
                    found.append(base)
                    
            elif isinstance(node, ast.Import):
                # Direct imports like "import os" or "import os.path"
                found.extend(alias.name for alias in node.names)
        result[module] = found
    return result


def detect_circular_dependencies(imports: Dict[Path, List[str]]) -> List[tuple[str, str]]:
    """Return a list of simple circular import pairs."""
    name_map = {m.stem: m for m in imports}
    cycles: List[tuple[str, str]] = []
    for module, deps in imports.items():
        module_name = module.stem
        for dep in deps:
            dep_name = dep.split(".")[0]
            target = name_map.get(dep_name)
            if target is None:
                continue
            target_deps = [d.split(".")[0] for d in imports.get(target, [])]
            if module_name in target_deps:
                pair = tuple(sorted((module_name, dep_name)))
                if pair not in cycles:
                    cycles.append(pair)
    return cycles
