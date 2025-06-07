"""CLI command definitions for PyModuleAnalyzer."""

import json
from pathlib import Path

import typer

from ..analyzer.module_discovery import discover_modules
from ..analyzer.import_analyzer import analyze_imports, detect_circular_dependencies
from ..metrics.coupling import afferent_coupling, efferent_coupling, instability
from ..visualization.graph_generator import generate_dot, generate_mermaid


app = typer.Typer(help="Repository analysis commands")

@app.command()
def repository(
    path: str = ".",
    json_output: str | None = None,
) -> None:
    """Analyze the given repository."""
    modules = discover_modules(path)
    typer.echo(f"Discovered {len(modules)} module(s).")

    imports = analyze_imports(modules)
    abs_count = sum(1 for deps in imports.values() for d in deps if not d.startswith("."))
    rel_count = sum(1 for deps in imports.values() for d in deps if d.startswith("."))

    aff = afferent_coupling(imports)
    eff = efferent_coupling(imports)
    inst = instability(aff, eff)

    cycles = detect_circular_dependencies(imports)

    analysis = {
        "module_count": len(modules),
        "absolute_imports": abs_count,
        "relative_imports": rel_count,
        "modules": {
            module.stem: {
                "afferent": aff[module],
                "efferent": eff[module],
                "instability": round(inst[module], 2),
            }
            for module in modules
        },
        "circular_dependencies": cycles,
    }

    if json_output:
        Path(json_output).write_text(json.dumps(analysis, indent=2))
        typer.echo(f"Wrote {json_output}")
        return

    typer.echo(f"Absolute imports: {abs_count}, Relative imports: {rel_count}")
    typer.echo("Module coupling:")
    for module in modules:
        typer.echo(
            f" - {module.stem}: Ca={aff[module]} Ce={eff[module]} I={inst[module]:.2f}"
        )

    if cycles:
        typer.echo("Circular dependencies detected:")
        for a, b in cycles:
            typer.echo(f" - {a} <-> {b}")
    else:
        typer.echo("No circular dependencies found.")


@app.command()
def graph(
    path: str = ".",
    output: str = "dependencies.dot",
    format: str = typer.Option(
        "dot", "--format", "-f", help="graph format: dot or mermaid"
    ),
) -> None:
    """Generate a dependency graph."""
    modules = discover_modules(path)
    imports = analyze_imports(modules)
    if format == "mermaid" or output.endswith(".mmd"):
        data = generate_mermaid(imports)
    else:
        data = generate_dot(imports)
    Path(output).write_text(data)
    typer.echo(f"Wrote {output}")

