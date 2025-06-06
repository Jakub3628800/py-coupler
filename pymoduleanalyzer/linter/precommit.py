"""Pre-commit hook integration."""

import sys
from pathlib import Path

from .suggestions import suggest_private


def run(paths: list[str]) -> int:
    """Run linter on the provided file paths."""
    failed = False
    for path_str in paths:
        path = Path(path_str)
        suggestion = suggest_private(path)
        if suggestion:
            print(suggestion)
            failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(run(sys.argv[1:]))
