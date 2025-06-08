#!/usr/bin/env python3
"""Generate interactive HTML report with dependency graph visualization."""

import json
from pathlib import Path
from pymoduleanalyzer.analyzer.module_discovery import discover_modules
from pymoduleanalyzer.analyzer.import_analyzer import analyze_imports

def generate_interactive_html(imports):
    """Generate HTML with vis.js network visualization."""
    
    # Filter to show only project modules (not external libraries)
    project_modules = {}
    for module, deps in imports.items():
        module_str = str(module)
        if 'pymoduleanalyzer' in module_str or module_str in ['main']:
            # Filter dependencies to only include project modules
            project_deps = [dep for dep in deps if 'pymoduleanalyzer' in dep or dep in ['main', '.'] or dep.startswith('.')]
            if project_deps:
                project_modules[module_str] = project_deps
    
    # Create nodes and edges for vis.js
    nodes = []
    edges = []
    node_ids = {}
    
    # Create nodes
    for i, module in enumerate(project_modules.keys()):
        clean_name = module.replace('.py', '').split('/')[-1]
        nodes.append({
            'id': i,
            'label': clean_name,
            'title': module,
            'color': {'background': '#97C2FC', 'border': '#2B7CE9'}
        })
        node_ids[module] = i
    
    # Create edges
    for module, deps in project_modules.items():
        if module in node_ids:
            for dep in deps:
                # Try to find matching module for dependency
                for target_module in project_modules.keys():
                    if dep in target_module or target_module.endswith(f'/{dep}.py') or target_module.endswith(f'{dep}.py'):
                        if target_module in node_ids and module != target_module:
                            edges.append({
                                'from': node_ids[module],
                                'to': node_ids[target_module],
                                'arrows': 'to'
                            })
                            break
    
    html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <title>PyModuleAnalyzer Dependency Graph</title>
    <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style type="text/css">
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
        }}
        #mynetworkid {{
            width: 100%;
            height: 600px;
            border: 1px solid lightgray;
        }}
        .stats {{
            margin: 20px 0;
            padding: 15px;
            background-color: #f5f5f5;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <h1>PyModuleAnalyzer Dependency Graph</h1>
    
    <div class="stats">
        <h3>Project Statistics</h3>
        <p><strong>Project Modules:</strong> {len(project_modules)}</p>
        <p><strong>Dependencies:</strong> {len(edges)}</p>
        <p><strong>Total Modules Analyzed:</strong> {len(imports)}</p>
    </div>
    
    <div id="mynetworkid"></div>
    
    <div class="stats">
        <h3>Module Details</h3>
        <ul>
        {"".join(f"<li><strong>{module.split('/')[-1]}:</strong> {', '.join(deps[:5])}{'...' if len(deps) > 5 else ''}</li>" for module, deps in list(project_modules.items())[:10])}
        </ul>
    </div>

    <script type="text/javascript">
        var nodes = new vis.DataSet({json.dumps(nodes)});
        var edges = new vis.DataSet({json.dumps(edges)});
        var container = document.getElementById('mynetworkid');
        var data = {{
            nodes: nodes,
            edges: edges
        }};
        var options = {{
            layout: {{
                improvedLayout: true,
                hierarchical: {{
                    enabled: true,
                    direction: 'UD',
                    sortMethod: 'directed'
                }}
            }},
            physics: {{
                enabled: true,
                hierarchicalRepulsion: {{
                    centralGravity: 0.0,
                    springLength: 100,
                    springConstant: 0.01,
                    nodeDistance: 120,
                    damping: 0.09
                }},
                maxVelocity: 50,
                solver: 'hierarchicalRepulsion',
                timestep: 0.35,
                stabilization: {{iterations: 150}}
            }},
            nodes: {{
                shape: 'box',
                margin: 10,
                font: {{
                    size: 12,
                    face: 'Arial'
                }}
            }},
            edges: {{
                arrows: {{
                    to: {{enabled: true, scaleFactor: 1, type: 'arrow'}}
                }},
                color: '#848484',
                width: 2
            }},
            interaction: {{
                dragNodes: true,
                dragView: true,
                zoomView: true
            }}
        }};
        var network = new vis.Network(container, data, options);
        
        network.on("click", function (params) {{
            if (params.nodes.length > 0) {{
                var nodeId = params.nodes[0];
                var node = nodes.get(nodeId);
                alert("Module: " + node.title + "\\nLabel: " + node.label);
            }}
        }});
    </script>
</body>
</html>
"""
    return html_template

def main():
    """Generate interactive HTML report."""
    modules = discover_modules(".")
    imports = analyze_imports(modules)
    
    # Convert Path keys to strings
    string_imports = {str(module): deps for module, deps in imports.items()}
    
    html_content = generate_interactive_html(string_imports)
    
    output_file = Path("repo_analysis.html")
    output_file.write_text(html_content)
    print(f"Generated interactive HTML report: {output_file}")
    print("Open in browser to view the dependency graph visualization")

if __name__ == "__main__":
    main()