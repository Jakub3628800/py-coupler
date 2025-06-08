# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PyModuleAnalyzer is a Python AST-based tool for analyzing module dependencies, coupling patterns, and encapsulation opportunities in Python repositories. The project implements the full package structure with working CLI commands for repository analysis and dependency graph generation.

## Development Commands

**Package Management:**
- `uv sync` - Install dependencies using uv
- `uv add <package>` - Add new dependencies

**Running the Tool:**
```bash
# Analyze repository and output JSON
python -m pymoduleanalyzer.cli.main analyze repository --path . --json-output analysis.json

# Generate DOT dependency graph
python -m pymoduleanalyzer.cli.main analyze graph --path . --output deps.dot

# Generate Mermaid dependency graph
python -m pymoduleanalyzer.cli.main analyze graph --path . --output deps.mmd --format mermaid

# Generate from JSON input
python -m pymoduleanalyzer.cli.main analyze graph --json-input examples/imports_example.json --output example.mmd --format mermaid
```

**Testing:**
- `make test` - Runs analysis on the current repository, generating test outputs
- Tests are run automatically on pushes and PRs to master branch

**Code Quality:**
- `pre-commit run --all-files` - Run pre-commit hooks
- Pre-commit checks run automatically in CI

## Architecture

The project follows a modular structure with these core components:

- **cli/**: Typer-based CLI with main.py entry point and commands.py
- **analyzer/**: AST parsing, module discovery, import analysis, method analysis
- **metrics/**: Coupling metrics, complexity analysis, encapsulation scoring  
- **visualization/**: Graph generation and HTML reporting with templates
- **linter/**: Rule engine and improvement suggestions with pre-commit integration
- **utils/**: File utilities and configuration management

**Key Technologies:**
- Typer for CLI framework
- Python AST module for static analysis
- Graphviz for DOT graph generation
- Jinja2 for templating
- PyYAML for configuration

## Development Environment

- Python 3.12+ required
- Uses `uv` for dependency management
- GitHub Actions for CI/CD with test and pre-commit workflows
- Entry point available as `pymoduleanalyzer` command after installation

## File Structure

The project has working implementations across all planned modules, with the CLI providing repository analysis and graph generation capabilities. Examples and test outputs are available in `examples/` and `tests/` directories.