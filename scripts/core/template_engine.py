#!/usr/bin/env python3
"""
Antigravity Agent Factory - Jinja2 Template Engine

This module provides a Jinja2-based template rendering engine with custom
filters, globals, and macros for generating Antigravity agent projects.
Usage:
    from scripts.core.template_engine import TemplateEngine
    
    engine = TemplateEngine(template_dirs=[Path('templates')])
    content = engine.render('factory/agent.md.tmpl', {'agent_name': 'code-reviewer'})

Author: Antigravity Agent FactoryVersion: 1.0.0
"""

import re
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union


# Jinja2 import with graceful fallback
try:
    from jinja2 import Environment, FileSystemLoader, BaseLoader, TemplateNotFound
    from jinja2 import select_autoescape, pass_context
    JINJA2_AVAILABLE = True
except ImportError:
    JINJA2_AVAILABLE = False


# =============================================================================
# CUSTOM FILTERS
# =============================================================================

def snake_case(value: str) -> str:
    """
    Convert string to snake_case.
    
    Args:
        value: Input string (e.g., "MyClassName", "my-kebab-case")
        
    Returns:
        Snake case string (e.g., "my_class_name", "my_kebab_case")
        
    Example:
        >>> snake_case("MyClassName")
        'my_class_name'
        >>> snake_case("my-kebab-case")
        'my_kebab_case'
    """
    if not value:
        return value
    # Replace hyphens and spaces with underscores
    s = re.sub(r'[-\s]+', '_', value)
    # Insert underscore before uppercase letters
    s = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s)
    return s.lower()


def pascal_case(value: str) -> str:
    """
    Convert string to PascalCase.
    
    Args:
        value: Input string (e.g., "my_class_name", "my-kebab-case")
        
    Returns:
        Pascal case string (e.g., "MyClassName", "MyKebabCase")
        
    Example:
        >>> pascal_case("my_class_name")
        'MyClassName'
        >>> pascal_case("my-kebab-case")
        'MyKebabCase'
    """
    if not value:
        return value
    # Split on underscores, hyphens, and spaces
    words = re.split(r'[-_\s]+', value)
    return ''.join(word.capitalize() for word in words if word)


def camel_case(value: str) -> str:
    """
    Convert string to camelCase.
    
    Args:
        value: Input string (e.g., "my_class_name", "my-kebab-case")
        
    Returns:
        Camel case string (e.g., "myClassName", "myKebabCase")
        
    Example:
        >>> camel_case("my_class_name")
        'myClassName'
        >>> camel_case("my-kebab-case")
        'myKebabCase'
    """
    pascal = pascal_case(value)
    if not pascal:
        return pascal
    return pascal[0].lower() + pascal[1:]


def kebab_case(value: str) -> str:
    """
    Convert string to kebab-case.
    
    Args:
        value: Input string (e.g., "MyClassName", "my_snake_case")
        
    Returns:
        Kebab case string (e.g., "my-class-name", "my-snake-case")
        
    Example:
        >>> kebab_case("MyClassName")
        'my-class-name'
        >>> kebab_case("my_snake_case")
        'my-snake-case'
    """
    if not value:
        return value
    # First convert to snake_case, then replace underscores with hyphens
    s = snake_case(value)
    return s.replace('_', '-')


def title_case(value: str) -> str:
    """
    Convert string to Title Case with proper word splitting.
    
    Args:
        value: Input string (e.g., "my_class_name", "my-kebab-case")
        
    Returns:
        Title case string (e.g., "My Class Name", "My Kebab Case")
        
    Example:
        >>> title_case("my_class_name")
        'My Class Name'
        >>> title_case("my-kebab-case")
        'My Kebab Case'
    """
    if not value:
        return value
    # Split on underscores, hyphens, and existing spaces
    words = re.split(r'[-_\s]+', value)
    return ' '.join(word.capitalize() for word in words if word)


def pluralize(value: str, count: int = 2) -> str:
    """
    Simple English pluralization.
    
    Args:
        value: Singular word
        count: Number to check (default 2 for plural)
        
    Returns:
        Pluralized word if count != 1
        
    Example:
        >>> pluralize("agent")
        'agents'
        >>> pluralize("entity")
        'entities'
    """
    if count == 1:
        return value
    if not value:
        return value
    
    # Common irregular plurals
    irregulars = {
        'child': 'children',
        'person': 'people',
        'man': 'men',
        'woman': 'women',
        'mouse': 'mice',
        'goose': 'geese',
    }
    
    lower = value.lower()
    if lower in irregulars:
        # Preserve original capitalization pattern
        if value[0].isupper():
            return irregulars[lower].capitalize()
        return irregulars[lower]
    
    # Rules for regular pluralization
    if value.endswith(('s', 'sh', 'ch', 'x', 'z')):
        return value + 'es'
    if value.endswith('y') and len(value) > 1 and value[-2] not in 'aeiou':
        return value[:-1] + 'ies'
    if value.endswith('f'):
        return value[:-1] + 'ves'
    if value.endswith('fe'):
        return value[:-2] + 'ves'
    
    return value + 's'


def quote(value: str, style: str = 'double') -> str:
    """
    Wrap string in quotes.
    
    Args:
        value: String to quote
        style: 'single', 'double', or 'backtick'
        
    Returns:
        Quoted string
        
    Example:
        >>> quote("hello")
        '"hello"'
        >>> quote("hello", "single")
        "'hello'"
    """
    quotes = {
        'single': ("'", "'"),
        'double': ('"', '"'),
        'backtick': ('`', '`'),
    }
    left, right = quotes.get(style, ('"', '"'))
    return f"{left}{value}{right}"


def indent_text(value: str, width: int = 4, first: bool = False) -> str:
    """
    Indent text by specified width.
    
    Args:
        value: Text to indent
        width: Number of spaces (default 4)
        first: Whether to indent the first line too
        
    Returns:
        Indented text
        
    Example:
        >>> indent_text("line1\\nline2", 2)
        'line1\\n  line2'
    """
    if not value:
        return value
    
    indent = ' ' * width
    lines = value.split('\n')
    
    if first:
        return '\n'.join(indent + line for line in lines)
    else:
        result = [lines[0]]
        result.extend(indent + line if line else line for line in lines[1:])
        return '\n'.join(result)


def wrap_code(value: str, lang: str = '') -> str:
    """
    Wrap text in markdown code block.
    
    Args:
        value: Code to wrap
        lang: Language identifier for syntax highlighting
        
    Returns:
        Markdown code block
        
    Example:
        >>> wrap_code("print('hello')", "python")
        '```python\\nprint(\\'hello\\')\\n```'
    """
    return f"```{lang}\n{value}\n```"


def default_if_empty(value: Any, default: Any = '') -> Any:
    """
    Return default if value is empty/None/falsy.
    
    Args:
        value: Value to check
        default: Default to return if empty
        
    Returns:
        Value or default
    """
    if value is None or value == '' or value == [] or value == {}:
        return default
    return value


def join_lines(value: List[str], separator: str = '\n') -> str:
    """
    Join list of strings with separator.
    
    Args:
        value: List of strings
        separator: Separator (default newline)
        
    Returns:
        Joined string
    """
    if not value:
        return ''
    return separator.join(str(v) for v in value)


def to_json(value: Any, indent: int = 2) -> str:
    """
    Convert value to JSON string.
    
    Args:
        value: Value to serialize
        indent: Indentation level
        
    Returns:
        JSON string
    """
    import json
    return json.dumps(value, indent=indent, ensure_ascii=False)


def to_yaml_list(value: List[str], indent: int = 0) -> str:
    """
    Convert list to YAML list format.
    
    Args:
        value: List of strings
        indent: Base indentation
        
    Returns:
        YAML formatted list
        
    Example:
        >>> to_yaml_list(["item1", "item2"])
        '- item1\\n- item2'
    """
    if not value:
        return ''
    prefix = ' ' * indent
    return '\n'.join(f"{prefix}- {item}" for item in value)


# =============================================================================
# CUSTOM GLOBALS (Functions available in templates)
# =============================================================================

def now(format_str: str = '%Y-%m-%d') -> str:
    """
    Get current datetime formatted.
    
    Args:
        format_str: strftime format string
        
    Returns:
        Formatted datetime string
        
    Example:
        {{ now('%Y-%m-%d') }}  -> "2026-01-31"
        {{ now('%H:%M:%S') }}  -> "14:30:00"
    """
    return datetime.now().strftime(format_str)


def env(name: str, default: str = '') -> str:
    """
    Get environment variable.
    
    Args:
        name: Environment variable name
        default: Default value if not set
        
    Returns:
        Environment variable value or default
    """
    import os
    return os.environ.get(name, default)


def range_list(start: int, end: int, step: int = 1) -> List[int]:
    """
    Generate a range as a list (for use in templates).
    
    Args:
        start: Start value
        end: End value (exclusive)
        step: Step value
        
    Returns:
        List of integers
    """
    return list(range(start, end, step))


# =============================================================================
# TEMPLATE ENGINE CLASS
# =============================================================================

class TemplateEngine:
    """
    Jinja2-based template rendering engine for Antigravity Agent Factory.    
    Features:
    - Custom filters for case conversion, pluralization, etc.
    - Custom globals for datetime, environment variables
    - Support for macros via template inheritance
    - Legacy placeholder support ({{UPPERCASE}} -> {{ lowercase }})
    
    Attributes:
        env: Jinja2 Environment instance
        template_dirs: List of template directories
        
    Example:
        >>> engine = TemplateEngine([Path('templates')])
        >>> content = engine.render('factory/agent.md.tmpl', {'name': 'test'})
    """
    
    def __init__(
        self,
        template_dirs: Optional[List[Path]] = None,
        enable_autoescape: bool = False,
        legacy_placeholder_support: bool = True
    ):
        """
        Initialize the template engine.
        
        Args:
            template_dirs: List of directories to search for templates
            enable_autoescape: Enable HTML autoescaping (default False for markdown)
            legacy_placeholder_support: Support {{UPPERCASE}} placeholders
            
        Raises:
            ImportError: If Jinja2 is not installed
        """
        if not JINJA2_AVAILABLE:
            raise ImportError(
                "Jinja2 is required for template rendering. "
                "Install it with: pip install Jinja2>=3.1.0"
            )
        
        self.template_dirs = template_dirs or []
        self.legacy_placeholder_support = legacy_placeholder_support
        
        # Convert paths to strings for FileSystemLoader
        search_paths = [str(d) for d in self.template_dirs if d.exists()]
        
        # Create Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(search_paths) if search_paths else None,
            autoescape=select_autoescape(['html', 'xml']) if enable_autoescape else False,
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
            # Use {# #} for comments, {{ }} for variables, {% %} for statements
            comment_start_string='{#',
            comment_end_string='#}',
        )
        
        # Register custom filters
        self._register_filters()
        
        # Register custom globals
        self._register_globals()
    
    def _register_filters(self) -> None:
        """Register custom Jinja2 filters."""
        self.env.filters.update({
            # Case conversion
            'snake_case': snake_case,
            'pascal_case': pascal_case,
            'camel_case': camel_case,
            'kebab_case': kebab_case,
            'title_case': title_case,
            
            # Text manipulation
            'pluralize': pluralize,
            'quote': quote,
            'indent_text': indent_text,
            'wrap_code': wrap_code,
            'default_if_empty': default_if_empty,
            'join_lines': join_lines,
            
            # Serialization
            'to_json': to_json,
            'to_yaml_list': to_yaml_list,
        })
    
    def _register_globals(self) -> None:
        """Register custom Jinja2 global functions."""
        self.env.globals.update({
            'now': now,
            'env': env,
            'range_list': range_list,
        })
    
    def _convert_legacy_placeholders(
        self,
        template_str: str,
        context: Dict[str, Any]
    ) -> str:
        """
        Convert legacy placeholders to Jinja2 {{ lowercase }}.
        
        Supports two legacy formats:
        1. {{UPPERCASE}} - double curly braces (legacy Factory templates)
        2. {UPPERCASE} - single curly braces (cursorrules templates)        
        This provides backward compatibility with existing templates.
        
        Args:
            template_str: Template string with legacy placeholders
            context: Context dictionary (keys are checked for matching)
            
        Returns:
            Template string with converted placeholders
        """
        # First, handle {{UPPERCASE}} patterns (double curly braces)
        pattern_double = r'\{\{([A-Z][A-Z0-9_]*)\}\}'
        
        def replacer_double(match):
            placeholder = match.group(1)
            var_name = placeholder.lower()
            if var_name in context or placeholder in context:
                return f"{{{{ {var_name} }}}}"
            return match.group(0)
        
        result = re.sub(pattern_double, replacer_double, template_str)
        
        # Then, handle {UPPERCASE} patterns (single curly braces)
        # Be careful not to match Jinja2 syntax {{ }} or {% %}
        pattern_single = r'(?<!\{)\{([A-Z][A-Z0-9_]*)\}(?!\})'
        
        def replacer_single(match):
            placeholder = match.group(1)
            var_name = placeholder.lower()
            if var_name in context or placeholder in context:
                return f"{{{{ {var_name} }}}}"
            return match.group(0)
        
        result = re.sub(pattern_single, replacer_single, result)
        
        return result
    
    def render(
        self,
        template_path: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Render a template file with the given context.
        
        Args:
            template_path: Path to template file (relative to template_dirs)
            context: Dictionary of variables to pass to template
            
        Returns:
            Rendered template content
            
        Raises:
            TemplateNotFound: If template file doesn't exist
            
        Example:
            >>> engine.render('factory/agent.md.tmpl', {'agent_name': 'reviewer'})
        """
        context = context or {}
        template = self.env.get_template(template_path)
        return template.render(**context)
    
    def render_string(
        self,
        template_str: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Render a template string with the given context.
        
        Args:
            template_str: Template content as string
            context: Dictionary of variables to pass to template
            
        Returns:
            Rendered content
            
        Example:
            >>> engine.render_string('Hello {{ name }}!', {'name': 'World'})
            'Hello World!'
        """
        context = context or {}
        
        # Convert legacy placeholders if enabled
        if self.legacy_placeholder_support:
            template_str = self._convert_legacy_placeholders(template_str, context)
            # Also add uppercase versions of context keys for legacy support
            legacy_context = {}
            for key, value in context.items():
                legacy_context[key] = value
                legacy_context[key.upper()] = value
            context = legacy_context
        
        template = self.env.from_string(template_str)
        return template.render(**context)
    
    def render_file(
        self,
        file_path: Path,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Render a template from an absolute file path.
        
        Args:
            file_path: Absolute path to template file
            context: Dictionary of variables to pass to template
            
        Returns:
            Rendered content
            
        Example:
            >>> engine.render_file(Path('/path/to/template.tmpl'), {'var': 'value'})
        """
        context = context or {}
        template_str = file_path.read_text(encoding='utf-8')
        return self.render_string(template_str, context)
    
    def add_filter(self, name: str, func: Callable) -> None:
        """
        Add a custom filter to the engine.
        
        Args:
            name: Filter name to use in templates
            func: Filter function
            
        Example:
            >>> engine.add_filter('reverse', lambda x: x[::-1])
            >>> engine.render_string('{{ "hello" | reverse }}', {})
            'olleh'
        """
        self.env.filters[name] = func
    
    def add_global(self, name: str, value: Any) -> None:
        """
        Add a global variable or function to the engine.
        
        Args:
            name: Global name to use in templates
            value: Value or callable
            
        Example:
            >>> engine.add_global('project_name', 'MyProject')
            >>> engine.render_string('Project: {{ project_name }}', {})
            'Project: MyProject'
        """
        self.env.globals[name] = value
    
    def get_template_variables(self, template_str: str) -> List[str]:
        """
        Extract variable names from a template string.
        
        Args:
            template_str: Template content
            
        Returns:
            List of variable names found in the template
            
        Example:
            >>> engine.get_template_variables('{{ name }} - {{ age }}')
            ['name', 'age']
        """
        from jinja2 import meta
        ast = self.env.parse(template_str)
        return list(meta.find_undeclared_variables(ast))


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def create_engine(
    factory_root: Optional[Path] = None,
    additional_dirs: Optional[List[Path]] = None
) -> TemplateEngine:
    """
    Create a TemplateEngine with standard Factory configuration.
    
    Args:
        factory_root: Root directory of the factory (auto-detected if None)
        additional_dirs: Additional template directories to include
        
    Returns:
        Configured TemplateEngine instance
        
    Example:
        >>> engine = create_engine()
        >>> content = engine.render('python/fastapi/app.py.tmpl', context)
    """
    if factory_root is None:
        factory_root = Path(__file__).parent.parent.parent
    
    template_dirs = [
        factory_root / 'templates',
        factory_root / 'templates' / '_macros',
    ]
    
    if additional_dirs:
        template_dirs.extend(additional_dirs)
    
    return TemplateEngine(template_dirs=template_dirs)


def render_template(
    template_path: str,
    context: Dict[str, Any],
    factory_root: Optional[Path] = None
) -> str:
    """
    Convenience function to render a template with minimal setup.
    
    Args:
        template_path: Path to template relative to templates/
        context: Variables to pass to template
        factory_root: Factory root directory (auto-detected if None)
        
    Returns:
        Rendered template content
        
    Example:
        >>> content = render_template('factory/agent.md.tmpl', {'name': 'test'})
    """
    engine = create_engine(factory_root)
    return engine.render(template_path, context)


# =============================================================================
# MODULE TEST
# =============================================================================

if __name__ == '__main__':
    # Quick self-test
    print("Testing TemplateEngine...")
    
    # Test filters
    assert snake_case("MyClassName") == "my_class_name"
    assert pascal_case("my_class_name") == "MyClassName"
    assert camel_case("my_class_name") == "myClassName"
    assert kebab_case("MyClassName") == "my-class-name"
    assert pluralize("agent") == "agents"
    assert pluralize("entity") == "entities"
    
    print("[OK] Filter tests passed")
    
    # Test engine
    engine = TemplateEngine(template_dirs=[])
    
    # Test simple rendering
    result = engine.render_string("Hello {{ name }}!", {"name": "World"})
    assert result == "Hello World!", f"Expected 'Hello World!', got '{result}'"
    
    # Test legacy placeholder conversion
    result = engine.render_string("Hello {{NAME}}!", {"name": "World"})
    assert result == "Hello World!", f"Expected 'Hello World!', got '{result}'"
    
    # Test filters in template
    result = engine.render_string(
        "{{ name | snake_case }}", 
        {"name": "MyClassName"}
    )
    assert result == "my_class_name", f"Expected 'my_class_name', got '{result}'"
    
    print("[OK] Engine tests passed")
    
    # Test globals
    result = engine.render_string("Date: {{ now('%Y') }}", {})
    assert result.startswith("Date: 20"), f"Expected date, got '{result}'"
    
    print("[OK] Global tests passed")
    
    print("\n[SUCCESS] All tests passed!")
