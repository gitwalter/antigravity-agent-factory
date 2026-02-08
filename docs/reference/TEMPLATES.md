# Template System Reference

> **Philosophy:** Templates embody our [Culture and Values](../CULTURE_AND_VALUES.md)—craftsmanship patterns that serve future maintainers with love and care.

The Cursor Agent Factory uses a template-based code generation system to produce consistent, high-quality project artifacts. This document explains how templates work and how to create your own.

## Credits and Inspiration

The template system is built on **Jinja**, a powerful templating engine for Python.

**Creator**: [Armin Ronacher](https://github.com/mitsuhiko) - The brilliant mind behind Jinja, Flask, Click, and many other foundational Python tools. His work on Jinja (first released in 2008) has shaped how millions of developers generate dynamic content.

- **Jinja Repository**: https://github.com/pallets/jinja
- **Documentation**: https://jinja.palletsprojects.com/

We gratefully acknowledge Armin's contributions to the Python ecosystem. The elegance and power of Jinja enables the Cursor Agent Factory to generate complex, customized project structures from simple template definitions.

## How Templates Work

### The Generation Flow

```mermaid
flowchart LR
    subgraph Input["Input"]
        BP["📋 Blueprint<br/>Configuration"]
        VAR["Variables from<br/>config + stack"]
    end

    subgraph Engine["Template Engine"]
        TE["⚙️ Jinja<br/>Processor"]
        TF["📁 Templates from<br/>templates/ directory"]
    end

    subgraph Output["Output"]
        GEN["📂 Generated<br/>Project Files"]
    end

    BP --> TE
    VAR --> BP
    TF --> TE
    TE --> GEN

    style Input fill:#e3f2fd,stroke:#1976d2
    style Engine fill:#fff3e0,stroke:#ff9800
    style Output fill:#e8f5e9,stroke:#4caf50
```

1. **Load Configuration**: Blueprint defines variables (project name, stack, options)
2. **Select Templates**: Engine picks templates based on stack and features
3. **Render**: Jinja processes templates, replacing variables with values
4. **Write**: Generated files are written to target directory

### Template Location

Templates are organized by stack and purpose:

```
templates/
├── factory/           # Core factory templates
│   ├── cursorrules-template.md
│   ├── PURPOSE.md.tmpl
│   └── methodology.yaml.tmpl
├── python/            # Python stack templates
│   ├── fastapi/
│   └── streamlit/
├── typescript/        # TypeScript stack templates
│   └── nextjs/
├── ai/                # AI agent templates
│   ├── agent/
│   ├── prompt/
│   └── workflow/
├── java/              # Java Spring templates
├── csharp/            # C# .NET templates
├── abap/              # SAP ABAP/RAP templates
├── cap/               # SAP CAP templates
├── integration/       # SAP CPI/PI templates
├── automation/        # n8n automation templates
├── workflows/         # CI/CD workflow templates
├── methodology/       # Development methodology templates
└── docs/              # Documentation templates
```

## Jinja Syntax

### Variables

Insert values using double curly braces:

```jinja
# Template
class {{ class_name }}:
    """{{ description }}"""
    pass

# With variables: class_name="UserService", description="Handles user operations"
# Output
class UserService:
    """Handles user operations"""
    pass
```

### Control Structures

#### Conditionals

```jinja
{% if authentication %}
from app.auth import require_auth

@require_auth
{% endif %}
def {{ function_name }}():
    pass
```

#### Loops

```jinja
# Available endpoints:
{% for endpoint in endpoints %}
- {{ endpoint.method }} {{ endpoint.path }}: {{ endpoint.description }}
{% endfor %}
```

### Filters

Transform values with filters (pipe syntax):

#### Built-in Jinja2 Filters

| Filter | Example | Result |
|--------|---------|--------|
| `upper` | `{{ name\|upper }}` | `MYPROJECT` |
| `lower` | `{{ name\|lower }}` | `myproject` |
| `title` | `{{ name\|title }}` | `My Project` |
| `capitalize` | `{{ name\|capitalize }}` | `My project` |
| `replace` | `{{ name\|replace('-', '_') }}` | `my_project` |
| `default` | `{{ port\|default(8000) }}` | `8000` (if port undefined) |

#### Custom Factory Filters

The Cursor Agent Factory provides additional custom filters:

| Filter | Example | Result | Description |
|--------|---------|--------|-------------|
| `snake_case` | `{{ "MyClass"\|snake_case }}` | `my_class` | Convert to snake_case |
| `pascal_case` | `{{ "my_class"\|pascal_case }}` | `MyClass` | Convert to PascalCase |
| `camel_case` | `{{ "my_class"\|camel_case }}` | `myClass` | Convert to camelCase |
| `kebab_case` | `{{ "MyClass"\|kebab_case }}` | `my-class` | Convert to kebab-case |
| `title_case` | `{{ "my_class"\|title_case }}` | `My Class` | Convert to Title Case |
| `pluralize` | `{{ "agent"\|pluralize }}` | `agents` | Pluralize English word |
| `quote` | `{{ "value"\|quote }}` | `"value"` | Wrap in quotes |
| `wrap_code` | `{{ code\|wrap_code("python") }}` | ` ```python ... ``` ` | Wrap in code block |
| `to_json` | `{{ data\|to_json }}` | `{"key": "value"}` | Serialize to JSON |
| `to_yaml_list` | `{{ items\|to_yaml_list }}` | `- item1\n- item2` | Format as YAML list |

#### Custom Global Functions

| Function | Example | Description |
|----------|---------|-------------|
| `now('%Y-%m-%d')` | `{{ now('%Y-%m-%d') }}` | Current date/time formatted |
| `env('VAR_NAME')` | `{{ env('API_KEY', 'default') }}` | Get environment variable |
| `range_list(0, 5)` | `{{ range_list(0, 5) }}` | Generate a list from range |

### Comments

Comments are not included in output:

```jinja
{# This comment will not appear in the generated file #}
class {{ class_name }}:
    pass
```

### Whitespace Control

Use minus signs to control whitespace:

```jinja
{% for item in items -%}
  {{ item }}
{%- endfor %}
```

## Available Template Variables

### Core Variables (All Templates)

| Variable | Description | Example |
|----------|-------------|---------|
| `project_name` | Project name | `my-awesome-project` |
| `project_description` | Project description | `A FastAPI service for...` |
| `author` | Project author | `John Doe` |
| `generated_date` | Generation timestamp | `2026-01-30` |
| `stack` | Technology stack ID | `python-fastapi` |
| `language` | Primary language | `Python` |

### Stack-Specific Variables

#### Python

| Variable | Description |
|----------|-------------|
| `python_version` | Python version (e.g., `3.11`) |
| `package_name` | Python package name |
| `use_async` | Whether to use async/await |

#### TypeScript/Next.js

| Variable | Description |
|----------|-------------|
| `node_version` | Node.js version |
| `use_typescript` | TypeScript enabled |
| `styling` | CSS framework (tailwind, etc.) |

#### AI Agent

| Variable | Description |
|----------|-------------|
| `llm_provider` | LLM provider (openai, anthropic) |
| `model_name` | Default model name |
| `agent_framework` | Framework (langchain, langgraph) |
| `mcp_servers` | List of MCP servers |

#### SAP

| Variable | Description |
|----------|-------------|
| `namespace` | SAP namespace |
| `package` | Development package |
| `transport` | Transport request |

### Computed Variables

Some variables are computed from others:

| Variable | Derived From | Example |
|----------|--------------|---------|
| `class_name` | `project_name` | `MyAwesomeProject` |
| `module_name` | `project_name` | `my_awesome_project` |
| `kebab_name` | `project_name` | `my-awesome-project` |

## Creating Custom Templates

### Step 1: Create Template File

Create a `.tmpl` file in the appropriate directory:

```jinja
{# templates/python/service.py.tmpl #}
"""
{{ service_name }} Service
{{ '=' * (service_name|length + 8) }}

{{ description }}

Generated: {{ generated_date }}
"""

from typing import Optional, List
{% if use_async %}
import asyncio
{% endif %}

class {{ service_name }}Service:
    """{{ description }}"""
    
    def __init__(self):
        self._initialized = False
    
    {% if use_async %}
    async def initialize(self) -> None:
    {% else %}
    def initialize(self) -> None:
    {% endif %}
        """Initialize the service."""
        self._initialized = True
    
    {% for method in methods %}
    {% if use_async %}
    async def {{ method.name }}(self{{ method.params }}) -> {{ method.return_type }}:
    {% else %}
    def {{ method.name }}(self{{ method.params }}) -> {{ method.return_type }}:
    {% endif %}
        """{{ method.description }}"""
        raise NotImplementedError()
    
    {% endfor %}
```

### Step 2: Register in Blueprint

Add template reference to your blueprint:

```json
{
  "templates": [
    {
      "source": "python/service.py.tmpl",
      "target": "src/services/{{ service_name|lower }}_service.py",
      "variables": {
        "service_name": "User",
        "description": "Handles user operations",
        "use_async": true,
        "methods": [
          {
            "name": "get_by_id",
            "params": ", user_id: int",
            "return_type": "Optional[User]",
            "description": "Get user by ID"
          }
        ]
      }
    }
  ]
}
```

### Step 3: Test Generation

Run the generator to verify:

```bash
python cli/factory_cli.py --blueprint your-blueprint --output ./test-output
```

## Template Best Practices

### 1. Use Meaningful Variable Names

```jinja
{# Good #}
class {{ entity_name }}Repository:

{# Avoid #}
class {{ x }}Repository:
```

### 2. Provide Defaults for Optional Variables

```jinja
{% set port = port | default(8000) %}
{% set debug = debug | default(false) %}

DEBUG = {{ debug }}
PORT = {{ port }}
```

### 3. Include Generated File Headers

```jinja
"""
This file was generated by Cursor Agent Factory.
Generated: {{ generated_date }}
Blueprint: {{ blueprint_name }}

Do not edit manually - changes will be overwritten.
"""
```

### 4. Use Comments for Template Logic

```jinja
{# Loop through all configured endpoints #}
{% for endpoint in endpoints %}
{# Skip deprecated endpoints #}
{% if not endpoint.deprecated %}
...
{% endif %}
{% endfor %}
```

### 5. Handle Empty Collections

```jinja
{% if methods %}
# Methods
{% for method in methods %}
def {{ method.name }}(): pass
{% endfor %}
{% else %}
# No methods defined
pass
{% endif %}
```

## Debugging Templates

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `UndefinedError` | Variable not provided | Add default or check blueprint |
| `TemplateSyntaxError` | Invalid Jinja syntax | Check brackets and keywords |
| `TypeError` | Wrong variable type | Verify variable types in config |

### Debug Mode

Enable verbose output to see template processing:

```bash
python cli/factory_cli.py --blueprint your-blueprint --output ./test --verbose
```

### Validate Syntax

Test template syntax using the TemplateEngine:

```python
from scripts.core.template_engine import create_engine, TemplateEngine

# Quick rendering
engine = create_engine()
content = engine.render('python/service.py.tmpl', {
    'service_name': 'Test',
    'description': 'Test service'
})
print(content)

# Render a string directly
engine = TemplateEngine(template_dirs=[])
result = engine.render_string('Hello {{ name | title_case }}!', {'name': 'world'})
print(result)  # "Hello World!"
```

### Using the TemplateEngine API

The `TemplateEngine` class provides full control over template rendering:

```python
from pathlib import Path
from scripts.core.template_engine import TemplateEngine, create_engine

# Create engine with default factory templates
engine = create_engine()

# Or create with custom template directories
engine = TemplateEngine(
    template_dirs=[Path('templates'), Path('custom_templates')],
    legacy_placeholder_support=True  # Enable {UPPERCASE} conversion
)

# Render a template file
content = engine.render('factory/agent.md.tmpl', {
    'agent_name': 'code-reviewer',
    'agent_description': 'Reviews code quality',
    'skills': ['grounding', 'code-review'],
})

# Render a string template
result = engine.render_string(
    '{% for s in skills %}{{ s | pascal_case }}, {% endfor %}',
    {'skills': ['code-review', 'grounding']}
)

# Add custom filters
engine.add_filter('reverse', lambda x: x[::-1])

# Add custom globals
engine.add_global('company_name', 'Acme Corp')

# Extract variables from template
vars = engine.get_template_variables('{{ name }} - {{ version }}')
print(vars)  # ['name', 'version']
```

## Template File Naming

| Convention | Example | Use Case |
|------------|---------|----------|
| `name.ext.tmpl` | `app.py.tmpl` | Standard template |
| `name-type.ext.tmpl` | `model-entity.py.tmpl` | Variant templates |
| `_partial.tmpl` | `_imports.tmpl` | Includable partials |

## Extending the Template System

### Adding New Template Categories

1. Create directory under `templates/`
2. Add templates with `.tmpl` extension
3. Update blueprint to reference new templates
4. Document variables in this file

### Creating Template Macros

For reusable template snippets:

```jinja
{# templates/_macros/python.tmpl #}
{% macro class_header(name, description) %}
class {{ name }}:
    """{{ description }}"""
{% endmacro %}

{% macro import_block(imports) %}
{% for imp in imports %}
from {{ imp.module }} import {{ imp.name }}
{% endfor %}
{% endmacro %}
```

Use in templates:

```jinja
{% from "_macros/python.tmpl" import class_header, import_block %}

{{ import_block(imports) }}

{{ class_header(class_name, description) }}
    pass
```

## See Also

- [Jinja Documentation](https://jinja.palletsprojects.com/) - Official Jinja docs
- [FACTORY_COMPONENTS.md](FACTORY_COMPONENTS.md) - How templates integrate with generation
- [BLUEPRINTS.md](BLUEPRINTS.md) - Blueprint configuration reference
- [EXTENSION_GUIDE.md](../EXTENSION_GUIDE.md) - Adding new stacks and templates
