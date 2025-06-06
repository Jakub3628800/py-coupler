"""Calculate basic coupling metrics."""

from pathlib import Path
from typing import Dict, Iterable, List


def efferent_coupling(imports: Dict[Path, List[str]]) -> Dict[Path, int]:
    """Return efferent coupling (outgoing dependencies) per module."""
    return {module: len(deps) for module, deps in imports.items()}


def afferent_coupling(imports: Dict[Path, List[str]]) -> Dict[Path, int]:
    """Return afferent coupling (incoming dependencies) per module."""
    name_map = {module.stem: module for module in imports}
    counts: Dict[Path, int] = {module: 0 for module in imports}
    for module, deps in imports.items():
        for dep in deps:
            dep_name = dep.split(".")[0]
            target = name_map.get(dep_name)
            if target is not None:
                counts[target] += 1
    return counts


def instability(afferent: Dict[Path, int], efferent: Dict[Path, int]) -> Dict[Path, float]:
    """Return instability metric per module."""
    result: Dict[Path, float] = {}
    for module in efferent:
        ca = afferent.get(module, 0)
        ce = efferent.get(module, 0)
        total = ca + ce
        result[module] = ce / total if total else 0.0
    return result
