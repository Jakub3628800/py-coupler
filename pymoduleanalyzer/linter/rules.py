"""Basic linting rules."""

from pathlib import Path

from ..metrics.encapsulation import private_method_ratio


def check_private_methods(path: Path, threshold: float = 0.5) -> bool:
    """Return True if private method ratio meets threshold."""
    return private_method_ratio(path) >= threshold
