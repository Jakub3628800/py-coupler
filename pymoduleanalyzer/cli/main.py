"""Entry point for PyModuleAnalyzer CLI."""

import typer

from . import commands

app = typer.Typer(help="Python Repository Structure Analysis Tool")

app.add_typer(commands.app, name="analyze")

if __name__ == "__main__":
    app()
