"""
Unit tests for TemplateEngine class and custom filters.

Tests cover:
- Filter functions (snake_case, pascal_case, etc.)
- TemplateEngine initialization
- Template rendering with Jinja2 syntax
- Legacy placeholder support
- Custom globals (now(), env())
- Template variable extraction
"""

import sys
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import pytest

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.core.template_engine import (
    TemplateEngine,
    create_engine,
    render_template,
    # Filters
    snake_case,
    pascal_case,
    camel_case,
    kebab_case,
    title_case,
    pluralize,
    quote,
    indent_text,
    wrap_code,
    default_if_empty,
    join_lines,
    to_json,
    to_yaml_list,
    # Globals
    now,
    env,
    range_list,
)


# =============================================================================
# FILTER TESTS
# =============================================================================

class TestSnakeCaseFilter:
    """Tests for snake_case filter."""
    
    def test_from_pascal_case(self):
        """Test conversion from PascalCase."""
        assert snake_case("MyClassName") == "my_class_name"
        # Note: Consecutive capitals stay together (common behavior)
        assert snake_case("HTTPServer") == "httpserver"
        assert snake_case("XMLParser") == "xmlparser"
    
    def test_from_camel_case(self):
        """Test conversion from camelCase."""
        assert snake_case("myClassName") == "my_class_name"
        assert snake_case("getUserById") == "get_user_by_id"
    
    def test_from_kebab_case(self):
        """Test conversion from kebab-case."""
        assert snake_case("my-class-name") == "my_class_name"
        assert snake_case("user-service") == "user_service"
    
    def test_with_spaces(self):
        """Test conversion from space-separated words."""
        assert snake_case("My Class Name") == "my_class_name"
    
    def test_empty_and_none(self):
        """Test with empty string."""
        assert snake_case("") == ""
        assert snake_case(None) is None


class TestPascalCaseFilter:
    """Tests for pascal_case filter."""
    
    def test_from_snake_case(self):
        """Test conversion from snake_case."""
        assert pascal_case("my_class_name") == "MyClassName"
        assert pascal_case("user_service") == "UserService"
    
    def test_from_kebab_case(self):
        """Test conversion from kebab-case."""
        assert pascal_case("my-class-name") == "MyClassName"
        assert pascal_case("user-service") == "UserService"
    
    def test_from_spaces(self):
        """Test conversion from space-separated words."""
        assert pascal_case("my class name") == "MyClassName"
    
    def test_empty(self):
        """Test with empty string."""
        assert pascal_case("") == ""


class TestCamelCaseFilter:
    """Tests for camel_case filter."""
    
    def test_from_snake_case(self):
        """Test conversion from snake_case."""
        assert camel_case("my_class_name") == "myClassName"
        assert camel_case("get_user_by_id") == "getUserById"
    
    def test_from_kebab_case(self):
        """Test conversion from kebab-case."""
        assert camel_case("my-class-name") == "myClassName"
    
    def test_empty(self):
        """Test with empty string."""
        assert camel_case("") == ""


class TestKebabCaseFilter:
    """Tests for kebab_case filter."""
    
    def test_from_pascal_case(self):
        """Test conversion from PascalCase."""
        assert kebab_case("MyClassName") == "my-class-name"
    
    def test_from_snake_case(self):
        """Test conversion from snake_case."""
        assert kebab_case("my_snake_case") == "my-snake-case"
    
    def test_empty(self):
        """Test with empty string."""
        assert kebab_case("") == ""


class TestTitleCaseFilter:
    """Tests for title_case filter."""
    
    def test_from_snake_case(self):
        """Test conversion from snake_case."""
        assert title_case("my_class_name") == "My Class Name"
    
    def test_from_kebab_case(self):
        """Test conversion from kebab-case."""
        assert title_case("my-kebab-case") == "My Kebab Case"
    
    def test_empty(self):
        """Test with empty string."""
        assert title_case("") == ""


class TestPluralizeFilter:
    """Tests for pluralize filter."""
    
    def test_regular_plurals(self):
        """Test regular plural forms."""
        assert pluralize("agent") == "agents"
        assert pluralize("skill") == "skills"
    
    def test_special_endings(self):
        """Test words with special endings."""
        assert pluralize("entity") == "entities"
        assert pluralize("class") == "classes"
        assert pluralize("box") == "boxes"
    
    def test_count_one(self):
        """Test with count=1 (should not pluralize)."""
        assert pluralize("agent", 1) == "agent"
    
    def test_irregulars(self):
        """Test irregular plurals."""
        assert pluralize("child") == "children"
        assert pluralize("person") == "people"
    
    def test_empty(self):
        """Test with empty string."""
        assert pluralize("") == ""


class TestQuoteFilter:
    """Tests for quote filter."""
    
    def test_double_quotes(self):
        """Test double quote style."""
        assert quote("hello") == '"hello"'
        assert quote("hello", "double") == '"hello"'
    
    def test_single_quotes(self):
        """Test single quote style."""
        assert quote("hello", "single") == "'hello'"
    
    def test_backticks(self):
        """Test backtick style."""
        assert quote("hello", "backtick") == "`hello`"


class TestIndentTextFilter:
    """Tests for indent_text filter."""
    
    def test_basic_indent(self):
        """Test basic indentation."""
        result = indent_text("line1\nline2", 4)
        assert result == "line1\n    line2"
    
    def test_indent_first_line(self):
        """Test with first line indented."""
        result = indent_text("line1\nline2", 2, first=True)
        assert result == "  line1\n  line2"
    
    def test_empty(self):
        """Test with empty string."""
        assert indent_text("", 4) == ""


class TestWrapCodeFilter:
    """Tests for wrap_code filter."""
    
    def test_with_language(self):
        """Test with language specified."""
        result = wrap_code("print('hello')", "python")
        assert result == "```python\nprint('hello')\n```"
    
    def test_without_language(self):
        """Test without language."""
        result = wrap_code("some code")
        assert result == "```\nsome code\n```"


class TestDefaultIfEmptyFilter:
    """Tests for default_if_empty filter."""
    
    def test_with_value(self):
        """Test with non-empty value."""
        assert default_if_empty("hello", "default") == "hello"
    
    def test_with_empty_string(self):
        """Test with empty string."""
        assert default_if_empty("", "default") == "default"
    
    def test_with_none(self):
        """Test with None."""
        assert default_if_empty(None, "default") == "default"
    
    def test_with_empty_list(self):
        """Test with empty list."""
        assert default_if_empty([], "default") == "default"


class TestJoinLinesFilter:
    """Tests for join_lines filter."""
    
    def test_basic_join(self):
        """Test basic joining."""
        assert join_lines(["a", "b", "c"]) == "a\nb\nc"
    
    def test_custom_separator(self):
        """Test with custom separator."""
        assert join_lines(["a", "b", "c"], ", ") == "a, b, c"
    
    def test_empty_list(self):
        """Test with empty list."""
        assert join_lines([]) == ""


class TestToJsonFilter:
    """Tests for to_json filter."""
    
    def test_dict(self):
        """Test with dictionary."""
        result = to_json({"a": 1})
        assert '"a": 1' in result
    
    def test_list(self):
        """Test with list."""
        result = to_json([1, 2, 3])
        assert "1" in result


class TestToYamlListFilter:
    """Tests for to_yaml_list filter."""
    
    def test_basic_list(self):
        """Test basic list."""
        result = to_yaml_list(["item1", "item2"])
        assert result == "- item1\n- item2"
    
    def test_empty_list(self):
        """Test with empty list."""
        assert to_yaml_list([]) == ""


# =============================================================================
# GLOBAL FUNCTION TESTS
# =============================================================================

class TestNowGlobal:
    """Tests for now() global function."""
    
    def test_default_format(self):
        """Test default format."""
        result = now()
        # Should be YYYY-MM-DD format
        assert len(result) == 10
        assert result.count("-") == 2
    
    def test_custom_format(self):
        """Test custom format."""
        result = now("%Y")
        assert result.isdigit()
        assert len(result) == 4


class TestEnvGlobal:
    """Tests for env() global function."""
    
    def test_existing_variable(self):
        """Test with existing environment variable."""
        with patch.dict('os.environ', {'TEST_VAR': 'test_value'}):
            assert env('TEST_VAR') == 'test_value'
    
    def test_missing_variable(self):
        """Test with missing variable and default."""
        assert env('NONEXISTENT_VAR', 'default') == 'default'


class TestRangeListGlobal:
    """Tests for range_list() global function."""
    
    def test_basic_range(self):
        """Test basic range."""
        assert range_list(0, 5) == [0, 1, 2, 3, 4]
    
    def test_with_step(self):
        """Test with step."""
        assert range_list(0, 10, 2) == [0, 2, 4, 6, 8]


# =============================================================================
# TEMPLATE ENGINE TESTS
# =============================================================================

class TestTemplateEngineInit:
    """Tests for TemplateEngine initialization."""
    
    def test_init_basic(self):
        """Test basic initialization."""
        engine = TemplateEngine(template_dirs=[])
        assert engine.env is not None
    
    def test_init_with_dirs(self, temp_template_dir):
        """Test initialization with template directories."""
        engine = TemplateEngine(template_dirs=[temp_template_dir])
        assert engine.template_dirs == [temp_template_dir]
    
    def test_filters_registered(self):
        """Test that custom filters are registered."""
        engine = TemplateEngine(template_dirs=[])
        assert 'snake_case' in engine.env.filters
        assert 'pascal_case' in engine.env.filters
        assert 'pluralize' in engine.env.filters
    
    def test_globals_registered(self):
        """Test that custom globals are registered."""
        engine = TemplateEngine(template_dirs=[])
        assert 'now' in engine.env.globals
        assert 'env' in engine.env.globals


class TestTemplateEngineRenderString:
    """Tests for render_string method."""
    
    def test_simple_variable(self):
        """Test simple variable substitution."""
        engine = TemplateEngine(template_dirs=[])
        result = engine.render_string("Hello {{ name }}!", {"name": "World"})
        assert result == "Hello World!"
    
    def test_filter_in_template(self):
        """Test using filter in template."""
        engine = TemplateEngine(template_dirs=[])
        result = engine.render_string(
            "{{ name | snake_case }}", 
            {"name": "MyClassName"}
        )
        assert result == "my_class_name"
    
    def test_conditional(self):
        """Test conditional in template."""
        engine = TemplateEngine(template_dirs=[])
        template = "{% if show %}Visible{% endif %}"
        assert engine.render_string(template, {"show": True}) == "Visible"
        assert engine.render_string(template, {"show": False}) == ""
    
    def test_loop(self):
        """Test loop in template."""
        engine = TemplateEngine(template_dirs=[])
        template = "{% for item in items %}{{ item }}{% endfor %}"
        result = engine.render_string(template, {"items": ["a", "b", "c"]})
        assert result == "abc"
    
    def test_legacy_placeholder_uppercase(self):
        """Test legacy {{UPPERCASE}} placeholder conversion."""
        engine = TemplateEngine(template_dirs=[], legacy_placeholder_support=True)
        result = engine.render_string("Hello {{NAME}}!", {"name": "World"})
        assert result == "Hello World!"
    
    def test_global_now_in_template(self):
        """Test using now() in template."""
        engine = TemplateEngine(template_dirs=[])
        result = engine.render_string("Year: {{ now('%Y') }}", {})
        assert result.startswith("Year: 20")  # 2020s-2030s


class TestTemplateEngineRenderFile:
    """Tests for render_file method."""
    
    def test_render_from_file(self, temp_template_dir):
        """Test rendering from a file path."""
        # Create a test template file
        template_file = temp_template_dir / "test.tmpl"
        template_file.write_text("Hello {{ name }}!")
        
        engine = TemplateEngine(template_dirs=[temp_template_dir])
        result = engine.render_file(template_file, {"name": "World"})
        assert result == "Hello World!"


class TestTemplateEngineAddFilter:
    """Tests for add_filter method."""
    
    def test_add_custom_filter(self):
        """Test adding a custom filter."""
        engine = TemplateEngine(template_dirs=[])
        engine.add_filter('reverse', lambda x: x[::-1])
        
        result = engine.render_string('{{ "hello" | reverse }}', {})
        assert result == "olleh"


class TestTemplateEngineAddGlobal:
    """Tests for add_global method."""
    
    def test_add_custom_global(self):
        """Test adding a custom global."""
        engine = TemplateEngine(template_dirs=[])
        engine.add_global('project_name', 'TestProject')
        
        result = engine.render_string('{{ project_name }}', {})
        assert result == "TestProject"


class TestTemplateEngineGetVariables:
    """Tests for get_template_variables method."""
    
    def test_extract_variables(self):
        """Test extracting variables from template."""
        engine = TemplateEngine(template_dirs=[])
        variables = engine.get_template_variables("{{ name }} - {{ age }}")
        assert 'name' in variables
        assert 'age' in variables


# =============================================================================
# CONVENIENCE FUNCTION TESTS
# =============================================================================

class TestCreateEngine:
    """Tests for create_engine convenience function."""
    
    def test_create_with_defaults(self, factory_root):
        """Test creating engine with default settings."""
        engine = create_engine(factory_root)
        assert engine is not None
        assert isinstance(engine, TemplateEngine)


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def temp_template_dir(tmp_path):
    """Create a temporary template directory."""
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    return template_dir


@pytest.fixture
def factory_root():
    """Get the factory root directory."""
    return Path(__file__).parent.parent.parent
