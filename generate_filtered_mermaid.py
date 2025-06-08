#!/usr/bin/env python3
"""Generate a filtered mermaid diagram showing only project modules."""

from pathlib import Path
from pymoduleanalyzer.analyzer.module_discovery import discover_modules
from pymoduleanalyzer.analyzer.import_analyzer import analyze_imports

def generate_filtered_mermaid(imports):
    """Generate mermaid diagram with only project modules."""
    
    # Filter to only project modules
    project_modules = set()
    project_imports = {}
    
    for module, deps in imports.items():
        module_str = str(module)
        # Include main entry point and pymoduleanalyzer modules
        if 'pymoduleanalyzer' in module_str or module_str.endswith('main.py'):
            project_modules.add(module_str)
            # Filter dependencies to only include project modules or relative imports
            filtered_deps = []
            for dep in deps:
                if ('pymoduleanalyzer' in dep or 
                    dep.startswith('.') or 
                    dep == 'typer' or  # Keep some key external deps for context
                    dep == 'pathlib' or
                    dep == 'json'):
                    filtered_deps.append(dep)
            if filtered_deps:
                project_imports[module_str] = filtered_deps
    
    # Generate mermaid syntax
    lines = ["flowchart TD"]
    
    # Create clean node names
    node_mapping = {}
    for module in project_modules:
        clean_name = module.replace('.py', '').replace('/', '_').replace('.', '_')
        # Make it even cleaner
        if 'pymoduleanalyzer' in clean_name:
            clean_name = clean_name.replace('pymoduleanalyzer_', '').replace('__', '_')
        node_mapping[module] = clean_name
    
    # Add edges
    added_edges = set()
    for module, deps in project_imports.items():
        if module in node_mapping:
            source = node_mapping[module]
            for dep in deps:
                # Handle relative imports
                if dep.startswith('.'):
                    continue  # Skip relative imports for now
                
                # Find target module
                target = None
                if dep in ['typer', 'pathlib', 'json']:
                    target = dep
                else:
                    for target_module in project_modules:
                        if dep in target_module:
                            target = node_mapping[target_module]
                            break
                
                if target and target != source:
                    edge = f"    {source} --> {target}"
                    if edge not in added_edges:
                        lines.append(edge)
                        added_edges.add(edge)
    
    # Add styling
    lines.extend([
        "",
        "    classDef cli fill:#e1f5fe",
        "    classDef analyzer fill:#f3e5f5", 
        "    classDef metrics fill:#e8f5e8",
        "    classDef visualization fill:#fff3e0",
        "    classDef linter fill:#fce4ec",
        "    classDef external fill:#f5f5f5"
    ])
    
    # Apply styles
    for module, clean_name in node_mapping.items():
        if 'cli' in module:
            lines.append(f"    class {clean_name} cli")
        elif 'analyzer' in module:
            lines.append(f"    class {clean_name} analyzer")
        elif 'metrics' in module:
            lines.append(f"    class {clean_name} metrics")
        elif 'visualization' in module:
            lines.append(f"    class {clean_name} visualization")
        elif 'linter' in module:
            lines.append(f"    class {clean_name} linter")
    
    # Style external dependencies
    for external in ['typer', 'pathlib', 'json']:
        lines.append(f"    class {external} external")
    
    return "\n".join(lines)

def main():
    """Generate filtered mermaid diagram."""
    modules = discover_modules(".")
    imports = analyze_imports(modules)
    
    # Convert Path keys to strings
    string_imports = {str(module): deps for module, deps in imports.items()}
    
    mermaid_content = generate_filtered_mermaid(string_imports)
    
    output_file = Path("project_diagram.mmd")
    output_file.write_text(mermaid_content)
    print(f"Generated filtered mermaid diagram: {output_file}")
    print(f"Diagram has {len(mermaid_content.splitlines())} lines")

if __name__ == "__main__":
    main()