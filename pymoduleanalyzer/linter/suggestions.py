"""Linting suggestions generator."""

from pathlib import Path

from .rules import check_private_methods


def suggest_private(path: Path) -> str | None:
    """Suggest making functions private if ratio is below threshold."""
    if not check_private_methods(path, threshold=0.3):
        return f"Consider making some functions in {path} private"
    return None
