#!/usr/bin/env python3
"""Generate a mermaid diagram with better grouping and layout."""

from pathlib import Path
from collections import defaultdict
from pymoduleanalyzer.analyzer.module_discovery import discover_modules
from pymoduleanalyzer.analyzer.import_analyzer import analyze_imports

def is_stdlib_module(module_name):
    """Check if a module is part of Python's standard library."""
    # Common stdlib modules (not exhaustive but covers most cases)
    stdlib_modules = {
        'os', 'sys', 'json', 'ast', 'pathlib', 'typing', 'collections', 
        'functools', 'itertools', 'operator', 'copy', 'pickle', 'io',
        'datetime', 'time', 'calendar', 'random', 'math', 'statistics',
        're', 'string', 'textwrap', 'unicodedata', 'codecs', 'locale',
        'threading', 'multiprocessing', 'subprocess', 'socket', 'ssl',
        'urllib', 'http', 'email', 'html', 'xml', 'csv', 'sqlite3',
        'logging', 'warnings', 'traceback', 'inspect', 'types',
        'importlib', 'pkgutil', 'unittest', 'doctest', 'tempfile',
        'shutil', 'glob', 'zipfile', 'tarfile', 'gzip', 'bz2',
        'argparse', 'configparser', 'dataclasses', 'enum', 'abc',
        'contextlib', 'weakref', 'gc', 'ctypes', '__future__',
        'builtins', 'site', 'keyword', 'token', 'tokenize'
    }
    
    # Get the root module name (before first dot)
    root_module = module_name.split('.')[0]
    return root_module in stdlib_modules

def generate_grouped_mermaid(imports):
    """Generate mermaid diagram with subgraphs for better organization."""
    
    # Detect project modules by finding the most common package prefix
    project_prefixes = set()
    for module in imports.keys():
        module_str = str(module)
        if '/' in module_str:
            parts = module_str.split('/')
            if len(parts) >= 2 and not parts[0].startswith('.'):
                project_prefixes.add(parts[0])
    
    # Group modules by package
    packages = defaultdict(list)
    for module in imports.keys():
        module_str = str(module)
        
        # Check if it's a project module
        is_project_module = False
        for prefix in project_prefixes:
            if module_str.startswith(prefix + '/'):
                is_project_module = True
                break
        
        if is_project_module:
            # Extract package name for project modules
            parts = module_str.split('/')
            if len(parts) >= 2:
                package = parts[-2]  # Get the parent directory name
                packages[package].append(module_str)
            else:
                packages['root'].append(module_str)
        else:
            # It's a script at the root level
            packages['scripts'].append(module_str)
    
    # Start building the mermaid diagram
    lines = ["flowchart TB"]
    lines.append("")
    
    # Create subgraphs for each package
    node_counter = 0
    node_mapping = {}
    
    for package, modules in packages.items():
        if not modules:
            continue
            
        lines.append(f"    subgraph {package}[{package}]")
        
        for module in modules:
            # Create clean node name
            clean_name = f"node{node_counter}"
            node_counter += 1
            
            # Get just the filename for display
            display_name = module.split('/')[-1].replace('.py', '')
            
            lines.append(f"        {clean_name}[{display_name}]")
            node_mapping[module] = clean_name
        
        lines.append("    end")
        lines.append("")
    
    # Separate external dependencies into stdlib and third-party
    stdlib_deps = set()
    thirdparty_deps = set()
    
    for deps in imports.values():
        for dep in deps:
            if not any(dep in mod for mod in imports.keys()) and not dep.startswith('.'):
                if is_stdlib_module(dep):
                    stdlib_deps.add(dep)
                else:
                    thirdparty_deps.add(dep)
    
    # Add stdlib dependencies
    if stdlib_deps:
        lines.append("    subgraph stdlib[Standard Library]")
        stdlib_nodes = {}
        for dep in sorted(stdlib_deps):
            clean_name = f"std_{dep.replace('.', '_').replace('-', '_')}"
            lines.append(f"        {clean_name}[{dep}]")
            stdlib_nodes[dep] = clean_name
        lines.append("    end")
        lines.append("")
        node_mapping.update(stdlib_nodes)
    
    # Add third-party dependencies  
    if thirdparty_deps:
        lines.append("    subgraph thirdparty[Third-party Packages]")
        thirdparty_nodes = {}
        for dep in sorted(thirdparty_deps):
            clean_name = f"pkg_{dep.replace('.', '_').replace('-', '_')}"
            lines.append(f"        {clean_name}[{dep}]")
            thirdparty_nodes[dep] = clean_name
        lines.append("    end")
        lines.append("")
        node_mapping.update(thirdparty_nodes)
    
    # Add edges between nodes
    lines.append("    %% Dependencies")
    for module, deps in imports.items():
        if str(module) in node_mapping:
            source = node_mapping[str(module)]
            for dep in deps:
                if dep in node_mapping:
                    target = node_mapping[dep]
                    lines.append(f"    {source} --> {target}")
                elif not dep.startswith('.'):  # Skip relative imports
                    # Check if it matches any module partially
                    for mod_key, mod_node in node_mapping.items():
                        if dep in mod_key:
                            lines.append(f"    {source} --> {mod_node}")
                            break
    
    lines.append("")
    
    # Generate dynamic styling based on discovered packages
    colors = [
        ("#4CAF50", "#2E7D32"),  # Green
        ("#2196F3", "#1565C0"),  # Blue  
        ("#FF9800", "#F57C00"),  # Orange
        ("#9C27B0", "#6A1B9A"),  # Purple
        ("#E91E63", "#C2185B"),  # Pink
        ("#00BCD4", "#0097A7"),  # Cyan
        ("#FFC107", "#F57F17"),  # Yellow
        ("#607D8B", "#37474F"),  # Blue Grey
        ("#795548", "#4E342E"),  # Brown
        ("#673AB7", "#4527A0"),  # Deep Purple
    ]
    
    lines.append("    %% Styling")
    
    # Stdlib and third-party styles
    lines.append("    classDef stdlibStyle fill:#F5F5F5,stroke:#757575,stroke-width:2px,color:#333333")
    lines.append("    classDef thirdpartyStyle fill:#FFE0B2,stroke:#F57C00,stroke-width:2px,color:#333333")
    
    # Generate styles for each package
    package_list = sorted(packages.keys())
    for i, package in enumerate(package_list):
        color_idx = i % len(colors)
        fill_color, stroke_color = colors[color_idx]
        text_color = "#ffffff" if package != "scripts" else "#000000"  # Dark text for yellow
        lines.append(f"    classDef {package}Style fill:{fill_color},stroke:{stroke_color},stroke-width:3px,color:{text_color}")
    
    # Apply styles to nodes based on their package
    lines.append("")
    lines.append("    %% Apply styles")
    for package, modules in packages.items():
        style_name = f"{package}Style"
        for module in modules:
            if module in node_mapping:
                lines.append(f"    class {node_mapping[module]} {style_name}")
    
    # Apply stdlib and third-party styles
    if stdlib_deps:
        for dep in stdlib_deps:
            if dep in node_mapping:
                lines.append(f"    class {node_mapping[dep]} stdlibStyle")
    
    if thirdparty_deps:
        for dep in thirdparty_deps:
            if dep in node_mapping:
                lines.append(f"    class {node_mapping[dep]} thirdpartyStyle")
    
    return "\n".join(lines)

def main():
    """Generate grouped mermaid diagram."""
    modules = discover_modules(".")
    imports = analyze_imports(modules)
    
    # Convert Path keys to strings
    string_imports = {str(module): deps for module, deps in imports.items()}
    
    mermaid_content = generate_grouped_mermaid(string_imports)
    
    output_file = Path("grouped_diagram.mmd")
    output_file.write_text(mermaid_content)
    print(f"Generated grouped mermaid diagram: {output_file}")
    print(f"Diagram has {len(mermaid_content.splitlines())} lines")

if __name__ == "__main__":
    main()