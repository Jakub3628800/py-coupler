#!/usr/bin/env python3
"""Generate HTML report of repository analysis."""

from pathlib import Path
from pymoduleanalyzer.analyzer.module_discovery import discover_modules
from pymoduleanalyzer.analyzer.import_analyzer import analyze_imports
from pymoduleanalyzer.visualization.report_builder import build_report

def main():
    """Generate HTML report."""
    modules = discover_modules(".")
    imports = analyze_imports(modules)
    
    # Convert Path keys to strings for better HTML display
    string_imports = {str(module): deps for module, deps in imports.items()}
    
    html_content = build_report(string_imports)
    
    output_file = Path("repo_analysis.html")
    output_file.write_text(html_content)
    print(f"Generated HTML report: {output_file}")

if __name__ == "__main__":
    main()