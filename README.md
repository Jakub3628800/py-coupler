# PyModuleAnalyzer

This project aims to implement the **PyModuleAnalyzer** described in
`docs/project_definition.md`.  The goal is to provide a command line tool that
can inspect Python repositories, analyze coupling metrics and generate simple
reports or graphs.

Currently only a very small subset of the planned functionality is present. The
package layout has been created along with stub implementations of the main
modules so development can begin immediately.

To run the CLI from the repository root:

```bash
python -m pymoduleanalyzer.cli.main analyze repository --path .
```

Generate a DOT dependency graph:

```bash
python -m pymoduleanalyzer.cli.main analyze graph --path . --output deps.dot
```
