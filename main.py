"""Convenience entry point for the CLI."""

from pymoduleanalyzer.cli.main import app


def main() -> None:
    """Execute the PyModuleAnalyzer command line interface."""
    app()


if __name__ == "__main__":
    main()
