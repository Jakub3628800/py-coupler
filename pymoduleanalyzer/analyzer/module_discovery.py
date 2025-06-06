"""Basic module discovery implementation."""

from pathlib import Path
from typing import List


def discover_modules(root: str) -> List[Path]:
    """Return a list of Python module file paths under the given root directory."""
    root_path = Path(root)
    return [p for p in root_path.rglob("*.py") if p.is_file()]
