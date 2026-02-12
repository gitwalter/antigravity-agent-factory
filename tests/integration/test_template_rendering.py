"""
Integration tests for template rendering with TemplateEngine.

Tests cover:
- End-to-end template rendering from files
- Factory template rendering
- Template rendering with project generator
- Macro usage in templates
"""

import json
import sys
from pathlib import Path

import pytest

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.core.template_engine import TemplateEngine, create_engine


# =============================================================================
# FACTORY TEMPLATE TESTS
# =============================================================================

class TestFactoryTemplateRendering:
    """Tests for rendering factory templates."""
    
    @pytest.fixture
    def engine(self, factory_root):
        """Create template engine with factory templates."""
        return create_engine(factory_root)
    
    def test_guardian_protocol_template(self, engine, factory_root):
        """Test rendering guardian-protocol.json.tmpl."""
        template_path = factory_root / '.agent' / 'templates' / 'knowledge' / 'guardian-protocol.json.tmpl'
        
        if not template_path.exists():
            pytest.skip("guardian-protocol.json.tmpl not found")
        
        context = {
            'project_name': 'Test Project',
            'generated_date': '2026-01-31T12:00:00Z',
        }
        
        result = engine.render_file(template_path, context)
        
        # Verify it's valid JSON
        data = json.loads(result)
        assert data['description'] == 'Lightweight Layer 0 Integrity Guardian for Test Project'
        assert data['last_updated'] == '2026-01-31T12:00:00Z'
    
    def test_agent_template_rendering(self, engine, factory_root):
        """Test rendering agent.md.tmpl with Jinja2 features."""
        template_path = factory_root / '.agent' / 'templates' / 'factory' / 'agent.md.tmpl'
        
        if not template_path.exists():
            pytest.skip("agent.md.tmpl not found")
        
        context = {
            'agent_name': 'code-reviewer',
            'agent_description': 'Reviews code for quality',
            'agent_title': 'Code Reviewer Agent',
            'purpose': 'Review and improve code quality',
            'activation_triggers': [
                {'pattern': 'review', 'example': 'Review this code'},
                {'pattern': 'check', 'example': 'Check the implementation'},
            ],
            'skills': ['code-review', 'grounding'],
            'templates': [],
            'patterns': [],
            'knowledge': ['best-practices'],
            'workflow_steps': [
                {
                    'name': 'Analyze',
                    'description': 'Analyze the code structure',
                    'actions': ['Read files', 'Check style'],
                }
            ],
            'rules': ['Follow style guide', 'Check tests'],
        }
        
        result = engine.render_file(template_path, context)
        
        # Verify key sections are present
        assert '# Code Reviewer Agent' in result
        assert 'code-reviewer' in result
        assert '## Purpose' in result
        assert 'Review and improve code quality' in result
        assert '## Activation Triggers' in result
        assert 'review' in result
    
    def test_skill_template_rendering(self, engine, factory_root):
        """Test rendering skill.md.tmpl with Jinja2 features."""
        template_path = factory_root / '.agent' / 'templates' / 'factory' / 'skill.md.tmpl'
        
        if not template_path.exists():
            pytest.skip("skill.md.tmpl not found")
        
        context = {
            'skill_name': 'bugfix-workflow',
            'skill_description': 'Workflow for fixing bugs',
            'skill_title': 'Bugfix Workflow',
            'skill_introduction': 'This skill guides bug fixing.',
            'agents': ['code-reviewer'],
            'templates': [],
            'patterns': [],
            'knowledge': [],
            'when_to_use': [
                'Bug reported in Jira',
                'Test failure detected',
            ],
            'process_steps': [
                {
                    'name': 'Investigate',
                    'description': 'Find the root cause',
                    'actions': ['Read logs', 'Reproduce issue'],
                }
            ],
            'fallback_procedures': [
                {'issue': 'Cannot reproduce', 'resolution': 'Ask for more details'},
            ],
        }
        
        result = engine.render_file(template_path, context)
        
        # Verify key sections are present
        assert '# Bugfix Workflow' in result
        assert 'bugfix-workflow' in result
        assert '## When to Use' in result
        assert 'Bug reported in Jira' in result
        assert '## Process' in result


class TestTemplateWithFilters:
    """Tests for templates using custom filters."""
    
    @pytest.fixture
    def engine(self):
        """Create template engine."""
        return TemplateEngine(template_dirs=[])
    
    def test_case_conversion_in_template(self, engine):
        """Test case conversion filters in template context."""
        template = """
Class: {{ name | pascal_case }}
Variable: {{ name | snake_case }}
File: {{ name | kebab_case }}
Title: {{ name | title_case }}
"""
        context = {'name': 'my_service_class'}
        result = engine.render_string(template, context)
        
        assert 'Class: MyServiceClass' in result
        assert 'Variable: my_service_class' in result
        assert 'File: my-service-class' in result
        assert 'Title: My Service Class' in result
    
    def test_pluralize_in_template(self, engine):
        """Test pluralize filter in template context."""
        template = "{{ item | pluralize }}"
        
        assert engine.render_string(template, {'item': 'agent'}) == 'agents'
        assert engine.render_string(template, {'item': 'entity'}) == 'entities'
    
    def test_code_block_in_template(self, engine):
        """Test wrap_code filter in template context."""
        template = '{{ code | wrap_code("python") }}'
        context = {'code': 'print("hello")'}
        result = engine.render_string(template, context)
        
        assert '```python' in result
        assert 'print("hello")' in result
        assert '```' in result


class TestTemplateWithLoops:
    """Tests for templates with loop constructs."""
    
    @pytest.fixture
    def engine(self):
        """Create template engine."""
        return TemplateEngine(template_dirs=[])
    
    def test_list_iteration(self, engine):
        """Test iterating over a list."""
        template = """
{% for item in items %}
- {{ item }}
{% endfor %}
"""
        context = {'items': ['Alpha', 'Beta', 'Gamma']}
        result = engine.render_string(template, context)
        
        assert '- Alpha' in result
        assert '- Beta' in result
        assert '- Gamma' in result
    
    def test_dict_iteration(self, engine):
        """Test iterating over a dictionary."""
        template = """
{% for key, value in data.items() %}
{{ key }}: {{ value }}
{% endfor %}
"""
        context = {'data': {'name': 'Test', 'version': '1.0'}}
        result = engine.render_string(template, context)
        
        assert 'name: Test' in result
        assert 'version: 1.0' in result
    
    def test_loop_with_index(self, engine):
        """Test using loop.index."""
        template = """
{% for step in steps %}
{{ loop.index }}. {{ step }}
{% endfor %}
"""
        context = {'steps': ['First', 'Second', 'Third']}
        result = engine.render_string(template, context)
        
        assert '1. First' in result
        assert '2. Second' in result
        assert '3. Third' in result
    
    def test_table_generation(self, engine):
        """Test generating a markdown table."""
        template = """
| Name | Value |
|------|-------|
{% for row in rows %}
| {{ row.name }} | {{ row.value }} |
{% endfor %}
"""
        context = {
            'rows': [
                {'name': 'A', 'value': '1'},
                {'name': 'B', 'value': '2'},
            ]
        }
        result = engine.render_string(template, context)
        
        assert '| A | 1 |' in result
        assert '| B | 2 |' in result


class TestTemplateWithConditionals:
    """Tests for templates with conditional constructs."""
    
    @pytest.fixture
    def engine(self):
        """Create template engine."""
        return TemplateEngine(template_dirs=[])
    
    def test_simple_if(self, engine):
        """Test simple if statement."""
        template = "{% if show %}Visible{% endif %}"
        
        assert engine.render_string(template, {'show': True}) == 'Visible'
        assert engine.render_string(template, {'show': False}) == ''
    
    def test_if_else(self, engine):
        """Test if-else statement."""
        template = "{% if premium %}Premium{% else %}Basic{% endif %}"
        
        assert engine.render_string(template, {'premium': True}) == 'Premium'
        assert engine.render_string(template, {'premium': False}) == 'Basic'
    
    def test_if_with_list_check(self, engine):
        """Test if with list existence check."""
        template = """
{% if items %}
Items exist: {{ items | length }}
{% else %}
No items
{% endif %}
"""
        assert 'Items exist: 3' in engine.render_string(template, {'items': [1, 2, 3]})
        assert 'No items' in engine.render_string(template, {'items': []})
    
    def test_optional_section(self, engine):
        """Test optional section based on variable presence."""
        template = """
## Required Section

Content here.

{% if optional_content %}
## Optional Section

{{ optional_content }}
{% endif %}
"""
        # With optional content
        result = engine.render_string(template, {'optional_content': 'Extra stuff'})
        assert '## Optional Section' in result
        assert 'Extra stuff' in result
        
        # Without optional content
        result = engine.render_string(template, {'optional_content': None})
        assert '## Optional Section' not in result


class TestLegacyPlaceholderSupport:
    """Tests for backward compatibility with {{UPPERCASE}} placeholders."""
    
    @pytest.fixture
    def engine(self):
        """Create template engine with legacy support enabled."""
        return TemplateEngine(template_dirs=[], legacy_placeholder_support=True)
    
    def test_uppercase_placeholder(self, engine):
        """Test uppercase placeholder conversion."""
        template = "Hello {{NAME}}!"
        result = engine.render_string(template, {'name': 'World'})
        assert result == "Hello World!"
    
    def test_mixed_placeholders(self, engine):
        """Test mixing legacy and Jinja2 syntax."""
        template = "{{PROJECT_NAME}} uses {{ language }}"
        result = engine.render_string(template, {
            'project_name': 'MyProject',
            'language': 'Python'
        })
        assert result == "MyProject uses Python"
    
    def test_curly_brace_placeholder(self, engine):
        """Test single-curly-brace placeholders in context."""
        # The engine converts {{UPPER}} to {{ lower }}
        template = "Project: {{PROJECT_NAME}}"
        result = engine.render_string(template, {'project_name': 'TestApp'})
        assert result == "Project: TestApp"


# =============================================================================
# PROJECT GENERATOR INTEGRATION TESTS
# =============================================================================

class TestProjectGeneratorWithTemplates:
    """Tests for ProjectGenerator using template engine."""
    
    def test_generator_has_template_engine(self, sample_generator):
        """Test that generator initializes template engine."""
        # Template engine should be available
        assert hasattr(sample_generator, 'template_engine')
        # May be None if Jinja2 not available, but attribute should exist
    
    def test_build_template_context(self, sample_generator):
        """Test building template context from config."""
        context = sample_generator._build_template_context()
        
        assert 'project_name' in context
        assert 'project_description' in context
        assert 'primary_language' in context
        assert 'frameworks' in context
        assert 'generated_date' in context


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def factory_root():
    """Get the factory root directory."""
    return Path(__file__).parent.parent.parent


@pytest.fixture
def sample_generator(factory_root, tmp_path):
    """Create a sample project generator."""
    from scripts.core.generate_project import ProjectGenerator, ProjectConfig
    
    config = ProjectConfig(
        project_name="Test Project",
        project_description="A test project",
        domain="testing",
        primary_language="python",
        frameworks=["pytest"],
        triggers=["manual"],
        agents=["code-reviewer"],
        skills=["bugfix-workflow"],
        mcp_servers=[],
        style_guide="pep8",
        blueprint_id=None,
        team_context="Test team"
    )
    
    return ProjectGenerator(config, str(tmp_path))
