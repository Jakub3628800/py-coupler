"""Configuration management."""

from dataclasses import dataclass
from pathlib import Path


def load_config(path: Path) -> dict:
    """Load a YAML configuration file."""
    import yaml

    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text())
