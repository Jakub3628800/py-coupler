"""Build simple HTML reports."""

from pathlib import Path
from typing import Dict, List

from jinja2 import Template


def build_report(imports: Dict[Path, List[str]]) -> str:
    """Return a minimal HTML report of module dependencies."""
    template = Template(
        """<html><body><h1>Dependencies</h1><ul>{% for module, deps in imports.items() %}<li>{{ module }}: {{ deps|join(', ') }}</li>{% endfor %}</ul></body></html>"""
    )
    return template.render(imports=imports)
