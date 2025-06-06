# PyModuleAnalyzer: Python Repository Structure Analysis Tool

## Project Overview

PyModuleAnalyzer is a command-line tool that performs static analysis of Python repositories to understand module dependencies, coupling patterns, and encapsulation opportunities. Using Abstract Syntax Tree (AST) parsing, it maps the architecture of Python projects, visualizes module relationships, and provides actionable recommendations for improving code organization and encapsulation.

## Core Features

### 1. Module Discovery and Analysis
- Automatic discovery of all Python modules within a repository
- Static analysis of import statements using AST parsing
- Identification of module dependencies and relationships
- Detection of circular dependencies
- Analysis of import patterns (absolute vs. relative imports)

### 2. Method and Function Analysis
- Enumeration of all public and private methods/functions per module
- Detection of methods that could be made private based on usage patterns
- Analysis of method signatures and complexity metrics
- Identification of unused or potentially dead code

### 3. Coupling Analysis
- Calculation of coupling metrics between modules:
  - Afferent coupling (incoming dependencies)
  - Efferent coupling (outgoing dependencies)
  - Instability metrics
- Classification of coupling as tight, moderate, or loose
- Identification of highly coupled modules that may benefit from refactoring

### 4. Visualization
- Generation of module dependency diagrams in multiple formats (DOT, SVG, PNG)
- Interactive HTML reports with collapsible module details
- Dependency matrix visualization
- Call graph generation for inter-module function calls

### 5. Linting and Recommendations
- Suggestions for methods that should be made private (underscore prefix)
- Detection of violations of common Python conventions
- Recommendations for reducing coupling between modules
- Pre-commit hook integration for continuous code quality checks

## Technical Architecture

### Core Components

```
pymoduleanalyzer/
├── cli/
│   ├── __init__.py
│   ├── main.py              # Main entry point
│   └── commands.py          # CLI command definitions
├── analyzer/
│   ├── __init__.py
│   ├── ast_parser.py        # AST parsing logic
│   ├── module_discovery.py  # Module discovery
│   ├── import_analyzer.py   # Import relationship analysis
│   └── method_analyzer.py   # Method/function analysis
├── metrics/
│   ├── __init__.py
│   ├── coupling.py          # Coupling metrics calculation
│   ├── complexity.py        # Code complexity metrics
│   └── encapsulation.py     # Encapsulation analysis
├── visualization/
│   ├── __init__.py
│   ├── graph_generator.py   # Dependency graph generation
│   ├── report_builder.py    # HTML report generation
│   └── templates/           # HTML templates
├── linter/
│   ├── __init__.py
│   ├── rules.py             # Linting rules
│   ├── suggestions.py       # Improvement suggestions
│   └── precommit.py         # Pre-commit integration
└── utils/
    ├── __init__.py
    ├── file_utils.py        # File system operations
    └── config.py            # Configuration management
```

### Key Technologies
- **AST Parsing**: Python's built-in `ast` module for static analysis
- **Graph Visualization**: NetworkX for graph analysis, Graphviz for rendering
- **CLI Framework**: Click or Typer for command-line interface
- **Reporting**: Jinja2 for HTML template rendering
- **Testing**: pytest for unit and integration tests

## Implementation Plan

### Phase 1: Foundation (Weeks 1-2)
- [ ] Set up project structure and development environment
- [ ] Implement basic module discovery using file system traversal
- [ ] Create AST parser for extracting import statements
- [ ] Build initial CLI interface with basic commands
- [ ] Implement self-testing capability (analyze own repository)

### Phase 2: Core Analysis (Weeks 3-4)
- [ ] Develop import relationship analyzer
- [ ] Implement method/function discovery and classification
- [ ] Create coupling metrics calculator
- [ ] Build basic text-based output formatters
- [ ] Add circular dependency detection

### Phase 3: Visualization (Weeks 5-6)
- [ ] Integrate Graphviz for dependency graph generation
- [ ] Implement HTML report generation
- [ ] Create interactive visualizations using D3.js
- [ ] Add export capabilities for different formats

### Phase 4: Linting and Suggestions (Weeks 7-8)
- [ ] Develop rule engine for linting
- [ ] Implement privatization suggestions
- [ ] Create pre-commit hook integration
- [ ] Add configuration file support (.pymoduleanalyzer.yml)

### Phase 5: Polish and Optimization (Weeks 9-10)
- [ ] Performance optimization for large repositories
- [ ] Comprehensive documentation
- [ ] Package for PyPI distribution
- [ ] Add example configurations and use cases

## Usage Examples

### Basic Analysis
```bash
# Analyze current directory
pymoduleanalyzer analyze .

# Analyze with specific output format
pymoduleanalyzer analyze . --output-format html --output-dir reports/

# Show module coupling metrics
pymoduleanalyzer coupling . --threshold 0.7
```

### Linting Mode
```bash
# Check for privatization opportunities
pymoduleanalyzer lint . --suggest-private

# Apply suggestions automatically
pymoduleanalyzer lint . --fix

# Check specific modules
pymoduleanalyzer lint . --modules src/core,src/utils
```

### Visualization
```bash
# Generate dependency graph
pymoduleanalyzer graph . --format svg --output deps.svg

# Create interactive HTML report
pymoduleanalyzer report . --output report.html
```

## Configuration

### .pymoduleanalyzer.yml
```yaml
exclude_patterns:
  - "tests/*"
  - "docs/*"
  - "*_test.py"

analysis:
  include_private: false
  follow_imports: true
  max_depth: 10

coupling:
  tight_threshold: 0.8
  loose_threshold: 0.3

linting:
  suggest_private: true
  min_usage_for_private: 1
  ignore_patterns:
    - "test_*"
    - "*_test"
```

## Metrics and Calculations

### Coupling Metrics
- **Afferent Coupling (Ca)**: Number of modules that depend on this module
- **Efferent Coupling (Ce)**: Number of modules this module depends on
- **Instability (I)**: Ce / (Ca + Ce)
- **Abstractness (A)**: Number of abstract classes / Total classes

### Encapsulation Score
- Based on ratio of private to public methods
- Usage analysis to identify methods only used within module
- Naming convention compliance

## Testing Strategy

### Self-Testing
The project will use itself as a test subject:
```bash
# From project root
pymoduleanalyzer analyze .
pymoduleanalyzer lint . --suggest-private
```

### Unit Tests
- Test each analyzer component independently
- Mock file system for controlled testing
- Test AST parsing with various Python constructs

### Integration Tests
- Test full analysis pipeline on sample repositories
- Verify output formats and visualizations
- Test pre-commit hook integration

## Future Enhancements

1. **Dynamic Analysis Support**: Optional runtime import tracking
2. **IDE Integration**: Plugins for VS Code, PyCharm
3. **CI/CD Integration**: GitHub Actions, GitLab CI templates
4. **Advanced Metrics**: Cyclomatic complexity, maintainability index
5. **Refactoring Suggestions**: Automated module splitting recommendations
6. **Multi-Language Support**: Extend to other languages with similar import systems

## Success Criteria

- Accurately identifies all static imports in Python repositories
- Provides actionable recommendations that improve code quality
- Generates clear, informative visualizations
- Integrates seamlessly with existing development workflows
- Performs analysis on large repositories (10k+ files) within reasonable time

## License

MIT License - Open source and freely available for commercial and non-commercial use.
