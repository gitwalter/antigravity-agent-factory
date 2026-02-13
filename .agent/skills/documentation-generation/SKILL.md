---
description: Automated documentation generation from code including docstrings, API
  docs, and architecture diagrams
name: documentation-generation
type: skill
---
# Documentation Generation

Automated documentation generation from code including docstrings, API docs, and architecture diagrams

Automates documentation from code: parses modules, extracts docstrings, generates API docs, and produces architecture diagrams.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Code Parsing

Parse Python modules and extract structure:

```python
import ast
from pathlib import Path
from typing import Any

def parse_module(filepath: str) -> dict[str, Any]:
    """Parse module and extract classes, functions, docstrings.
    
    Args:
        filepath: Path to Python file.
        
    Returns:
        Dict with functions, classes, and docstrings.
    """
    with open(filepath) as f:
        tree = ast.parse(f.read())
    result = {"functions": [], "classes": []}
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef):
            result["functions"].append({
                "name": node.name,
                "docstring": ast.get_docstring(node),
                "args": [a.arg for a in node.args.args],
            })
        elif isinstance(node, ast.ClassDef):
            result["classes"].append({
                "name": node.name,
                "docstring": ast.get_docstring(node),
                "methods": [n.name for n in node.body if isinstance(n, ast.FunctionDef)],
            })
    return result
```

### Step 2: Docstring Extraction

Extract and format docstrings:

```python
def extract_docstring(obj: Any) -> str:
    """Extract docstring from function or class.
    
    Args:
        obj: Callable or class to inspect.
        
    Returns:
        Docstring text or empty string.
    """
    return (obj.__doc__ or "").strip()

def format_google_docstring(summary: str, args: list, returns: str) -> str:
    """Build Google-style docstring."""
    lines = [summary, "", "Args:", *[f"    {a}: Description." for a in args], ""]
    if returns:
        lines += ["Returns:", f"    {returns}"]
    return "\n".join(lines)
```

### Step 3: API Doc Generation

Generate API documentation sections:

```python
def generate_api_section(parsed: dict[str, Any]) -> str:
    """Generate Markdown API section from parsed module."""
    lines = ["## API Reference", ""]
    for fn in parsed.get("functions", []):
        lines.append(f"### `{fn['name']}`")
        lines.append("")
        if fn.get("docstring"):
            lines.append(fn["docstring"])
        lines.append(f"**Parameters:** {', '.join(fn.get('args', []))}")
        lines.append("")
    return "\n".join(lines)
```

### Step 4: Diagram Creation

Create simple ASCII architecture diagrams:

```python
def create_module_diagram(parsed: dict[str, Any], module_name: str) -> str:
    """Generate simple module dependency diagram.
    
    Args:
        parsed: Output from parse_module.
        module_name: Name of module.
        
    Returns:
        ASCII diagram string.
    """
    lines = [f"```", f"{module_name}", "├── " + " | ".join(f["name"] for f in parsed.get("functions", [])[:5])]
    for cls in parsed.get("classes", [])[:3]:
        lines.append(f"└── {cls['name']}")
        lines.append("    └── " + ", ".join(cls.get("methods", [])[:5]))
    lines.append("```")
    return "\n".join(lines)
```

### Step 5: Output Assembly

Assemble final documentation:

```python
def get_module_docstring(tree: ast.AST) -> str:
    """Get module-level docstring from AST."""
    return ast.get_docstring(tree) or "No module docstring."

def assemble_docs(parsed: dict[str, Any], module_name: str, filepath: str) -> str:
    """Assemble full documentation from parsed module."""
    tree = ast.parse(Path(filepath).read_text())
    sections = [
        f"# {module_name}",
        "",
        get_module_docstring(tree),
        "",
        create_module_diagram(parsed, module_name),
        "",
        generate_api_section(parsed),
    ]
    return "\n".join(sections)
```

## Best Practices

- Use Google or NumPy docstring style consistently
- Include type hints; Sphinx autodoc can use them
- Run documentation build in CI
- Version docs with code releases

## References

- [Sphinx Documentation](https://www.sphinx-doc.org/)
- [pdoc](https://pdoc.dev/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
