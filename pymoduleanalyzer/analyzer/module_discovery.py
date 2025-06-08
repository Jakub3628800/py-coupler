"""Basic module discovery implementation."""

from pathlib import Path
from typing import List


def discover_modules(root: str) -> List[Path]:
    """Return a list of Python module file paths under the given root directory.
    
    Excludes virtual environments, installed packages, and common non-project directories.
    """
    root_path = Path(root)
    
    # Directories to exclude
    exclude_dirs = {
        '.venv', 'venv', 'env', '.env',  # Virtual environments
        '__pycache__', '.git', '.pytest_cache',  # Cache directories
        'node_modules', '.tox', 'htmlcov',  # Build/test artifacts
        'site-packages', 'dist-packages',  # Installed packages
        '.mypy_cache', '.coverage',  # Tool caches
        'build', 'dist', 'egg-info',  # Build outputs
    }
    
    modules = []
    for py_file in root_path.rglob("*.py"):
        # Check if any parent directory is in exclude list
        if any(part in exclude_dirs for part in py_file.parts):
            continue
        
        # Skip if in hidden directory (starts with .)
        if any(part.startswith('.') and part not in {'.', '..'} for part in py_file.parts):
            continue
            
        # Only include if it's a regular file
        if py_file.is_file():
            modules.append(py_file)
    
    return modules
