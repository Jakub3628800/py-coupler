"""File system utilities."""

from pathlib import Path


def iter_python_files(root: Path):
    """Yield all Python files under the given root."""
    yield from root.rglob("*.py")
