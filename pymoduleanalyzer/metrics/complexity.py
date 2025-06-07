"""Simple code complexity metric stubs."""

from pathlib import Path


def line_count(path: Path) -> int:
    """Return the number of lines in the file."""
    return len(path.read_text().splitlines())
