"""CLI command definitions for PyModuleAnalyzer."""

import typer
from pathlib import Path

from ..analyzer.module_discovery import discover_modules
from ..analyzer.import_analyzer import analyze_imports, detect_circular_dependencies
from ..metrics.coupling import afferent_coupling, efferent_coupling, instability
from ..visualization.graph_generator import generate_dot


app = typer.Typer(help="Repository analysis commands")

@app.command()
def repository(path: str = ".") -> None:
    """Analyze the given repository."""
    modules = discover_modules(path)
    typer.echo(f"Discovered {len(modules)} module(s).")

    imports = analyze_imports(modules)
    abs_count = sum(1 for deps in imports.values() for d in deps if not d.startswith("."))
    rel_count = sum(1 for deps in imports.values() for d in deps if d.startswith("."))

    aff = afferent_coupling(imports)
    eff = efferent_coupling(imports)
    inst = instability(aff, eff)

    typer.echo(f"Absolute imports: {abs_count}, Relative imports: {rel_count}")
    typer.echo("Module coupling:")
    for module in modules:
        typer.echo(f" - {module.stem}: Ca={aff[module]} Ce={eff[module]} I={inst[module]:.2f}")

    cycles = detect_circular_dependencies(imports)
    if cycles:
        typer.echo("Circular dependencies detected:")
        for a, b in cycles:
            typer.echo(f" - {a} <-> {b}")
    else:
        typer.echo("No circular dependencies found.")


@app.command()
def graph(path: str = ".", output: str = "dependencies.dot") -> None:
    """Generate a DOT dependency graph."""
    modules = discover_modules(path)
    imports = analyze_imports(modules)
    dot = generate_dot(imports)
    Path(output).write_text(dot)
    typer.echo(f"Wrote {output}")

