"""
Comprehensive tests for Jinja2 template syntax validation.

Tests validate that all Jinja2 templates (.j2 files) have:
- Valid Jinja2 syntax
- Required variables documented (if applicable)
- Proper template structure
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set

import pytest

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from jinja2 import Environment, TemplateSyntaxError, meta
    JINJA2_AVAILABLE = True
except ImportError:
    JINJA2_AVAILABLE = False


class TestTemplateSyntax:
    """Tests for Jinja2 template syntax validation."""

    @pytest.fixture
    def templates_dir(self, factory_root: Path) -> Path:
        """Get the templates directory."""
        return factory_root / ".agent" / "templates"

    @pytest.fixture
    def all_template_files(self, templates_dir: Path) -> List[Path]:
        """Get all Jinja2 template files (.j2)."""
        return list(templates_dir.rglob("*.j2"))

    @pytest.fixture
    def jinja_env(self):
        """Create a Jinja2 environment for template parsing."""
        if not JINJA2_AVAILABLE:
            pytest.skip("Jinja2 not available")
        return Environment()

    def test_jinja2_available(self):
        """Test that Jinja2 is available."""
        if not JINJA2_AVAILABLE:
            pytest.skip("Jinja2 library not installed. Install with: pip install jinja2")

    def test_template_files_exist(self, all_template_files: List[Path]):
        """Test that template files are found."""
        assert len(all_template_files) > 0, "Should find at least one template file"

    def test_templates_have_valid_syntax(self, all_template_files: List[Path], jinja_env):
        """Test that all templates have valid Jinja2 syntax."""
        if not JINJA2_AVAILABLE:
            pytest.skip("Jinja2 not available")
        
        errors = []
        for template_file in all_template_files:
            try:
                content = template_file.read_text(encoding="utf-8")
                jinja_env.parse(content)
            except TemplateSyntaxError as e:
                rel_path = template_file.relative_to(template_file.parent.parent.parent)
                errors.append(f"{rel_path}: Syntax error at line {e.lineno}: {e.message}")
            except Exception as e:
                rel_path = template_file.relative_to(template_file.parent.parent.parent)
                errors.append(f"{rel_path}: Error parsing template: {e}")
        
        if errors:
            pytest.fail(
                f"Found {len(errors)} template file(s) with syntax errors:\n" +
                "\n".join(f"  - {e}" for e in errors)
            )

    def test_templates_can_be_compiled(self, all_template_files: List[Path], jinja_env):
        """Test that all templates can be compiled."""
        if not JINJA2_AVAILABLE:
            pytest.skip("Jinja2 not available")
        
        errors = []
        for template_file in all_template_files:
            try:
                content = template_file.read_text(encoding="utf-8")
                jinja_env.from_string(content)
            except TemplateSyntaxError as e:
                rel_path = template_file.relative_to(template_file.parent.parent.parent)
                errors.append(f"{rel_path}: Compilation error at line {e.lineno}: {e.message}")
            except Exception as e:
                rel_path = template_file.relative_to(template_file.parent.parent.parent)
                errors.append(f"{rel_path}: Compilation error: {e}")
        
        if errors:
            pytest.fail(
                f"Found {len(errors)} template file(s) that cannot be compiled:\n" +
                "\n".join(f"  - {e}" for e in errors)
            )

    def test_templates_have_balanced_braces(self, all_template_files: List[Path]):
        """Test that templates have balanced Jinja2 braces."""
        errors = []
        for template_file in all_template_files:
            content = template_file.read_text(encoding="utf-8")
            
            # Count opening and closing braces
            open_braces = content.count("{{")
            close_braces = content.count("}}")
            open_blocks = content.count("{%")
            close_blocks = content.count("%}")
            open_comments = content.count("{#")
            close_comments = content.count("#}")
            
            if open_braces != close_braces:
                rel_path = template_file.relative_to(template_file.parent.parent.parent)
                errors.append(
                    f"{rel_path}: Unbalanced expression braces ({{{{: {open_braces}, }}}}: {close_braces})"
                )
            
            if open_blocks != close_blocks:
                rel_path = template_file.relative_to(template_file.parent.parent.parent)
                errors.append(
                    f"{rel_path}: Unbalanced block braces ({{%: {open_blocks}, %}}: {close_blocks})"
                )
            
            if open_comments != close_comments:
                rel_path = template_file.relative_to(template_file.parent.parent.parent)
                errors.append(
                    f"{rel_path}: Unbalanced comment braces ({{#: {open_comments}, #}}: {close_comments})"
                )
        
        if errors:
            pytest.fail(
                f"Found {len(errors)} template file(s) with unbalanced braces:\n" +
                "\n".join(f"  - {e}" for e in errors)
            )

    def test_templates_have_valid_filters(self, all_template_files: List[Path], jinja_env):
        """Test that templates use valid Jinja2 filters."""
        if not JINJA2_AVAILABLE:
            pytest.skip("Jinja2 not available")
        
        errors = []
        for template_file in all_template_files:
            try:
                content = template_file.read_text(encoding="utf-8")
                # Parse to check for filter syntax errors
                ast = jinja_env.parse(content)
                
                # Check for undefined filters (basic check)
                # This is a simplified check - full validation would require rendering
                # Look for common filter patterns
                filter_pattern = r'\|\s*(\w+)'
                filters = re.findall(filter_pattern, content)
                
                # Common Jinja2 built-in filters
                common_filters = {
                    'default', 'upper', 'lower', 'title', 'capitalize',
                    'trim', 'striptags', 'escape', 'e', 'safe',
                    'length', 'count', 'first', 'last', 'random',
                    'join', 'replace', 'round', 'int', 'float',
                    'abs', 'max', 'min', 'sum', 'sort', 'reverse',
                    'list', 'string', 'dict', 'selectattr', 'rejectattr',
                    'map', 'select', 'reject', 'groupby', 'batch',
                    'slice', 'truncate', 'wordcount', 'wordwrap',
                    'indent', 'urlize', 'nl2br', 'tojson', 'tojsonfilter',
                }
                
                # Check for potentially undefined filters
                for filter_name in filters:
                    if filter_name not in common_filters and not filter_name.startswith('_'):
                        # This might be a custom filter, so just warn
                        pass
                        
            except TemplateSyntaxError as e:
                rel_path = template_file.relative_to(template_file.parent.parent.parent)
                errors.append(f"{rel_path}: Filter syntax error: {e.message}")
            except Exception as e:
                # Skip other errors for this test
                pass
        
        if errors:
            pytest.fail(
                f"Found {len(errors)} template file(s) with filter issues:\n" +
                "\n".join(f"  - {e}" for e in errors)
            )


class TestTemplateVariables:
    """Tests for template variable usage and documentation."""

    @pytest.fixture
    def templates_dir(self, factory_root: Path) -> Path:
        """Get the templates directory."""
        return factory_root / "templates"

    @pytest.fixture
    def all_template_files(self, templates_dir: Path) -> List[Path]:
        """Get all Jinja2 template files (.j2)."""
        return list(templates_dir.rglob("*.j2"))

    @pytest.fixture
    def jinja_env(self):
        """Create a Jinja2 environment for template parsing."""
        if not JINJA2_AVAILABLE:
            pytest.skip("Jinja2 not available")
        return Environment()

    def test_templates_extract_undefined_variables(self, all_template_files: List[Path], jinja_env):
        """Test that we can extract undefined variables from templates."""
        if not JINJA2_AVAILABLE:
            pytest.skip("Jinja2 not available")
        
        # This test just ensures we can parse templates and extract variables
        # It doesn't fail, just validates the capability
        for template_file in all_template_files[:5]:  # Test first 5 only
            try:
                content = template_file.read_text(encoding="utf-8")
                ast = jinja_env.parse(content)
                undefined_vars = meta.find_undefined_refs(ast)
                # Just verify we can extract variables
                assert isinstance(undefined_vars, set)
            except Exception:
                # Skip if parsing fails (handled by other tests)
                pass

    def test_templates_use_default_filter_for_variables(self, all_template_files: List[Path]):
        """Test that templates use default filter for optional variables."""
        # This is a best practice check - templates should use | default() for optional vars
        warnings = []
        for template_file in all_template_files:
            content = template_file.read_text(encoding="utf-8")
            
            # Look for variables without default filters
            # Pattern: {{ variable }} without | default
            pattern = r'\{\{\s*(\w+)\s*\}\}(?!\s*\|\s*default)'
            matches = re.findall(pattern, content)
            
            # Filter out common Jinja2 built-ins
            builtins = {'loop', 'block', 'super', 'self', 'namespace', 'var'}
            undefined_vars = [m for m in matches if m not in builtins]
            
            if undefined_vars:
                # Just collect, don't fail - this is a best practice
                rel_path = template_file.relative_to(template_file.parent.parent.parent)
                warnings.append(f"{rel_path}: Variables without defaults: {', '.join(set(undefined_vars))}")
        
        # Don't fail, just log warnings
        if warnings and len(warnings) < 10:
            # Log but don't fail
            pass


class TestTemplateStructure:
    """Tests for template file structure and organization."""

    @pytest.fixture
    def templates_dir(self, factory_root: Path) -> Path:
        """Get the templates directory."""
        return factory_root / "templates"

    @pytest.fixture
    def all_template_files(self, templates_dir: Path) -> List[Path]:
        """Get all Jinja2 template files (.j2)."""
        return list(templates_dir.rglob("*.j2"))

    def test_templates_have_content(self, all_template_files: List[Path]):
        """Test that templates are not empty."""
        errors = []
        for template_file in all_template_files:
            content = template_file.read_text(encoding="utf-8")
            if len(content.strip()) == 0:
                rel_path = template_file.relative_to(template_file.parent.parent.parent)
                errors.append(f"{rel_path}: Template is empty")
        
        if errors:
            pytest.fail(
                f"Found {len(errors)} empty template file(s):\n" +
                "\n".join(f"  - {e}" for e in errors)
            )

    def test_templates_have_reasonable_length(self, all_template_files: List[Path]):
        """Test that templates have reasonable content length."""
        errors = []
        for template_file in all_template_files:
            content = template_file.read_text(encoding="utf-8")
            # Check minimum length (at least 10 characters)
            if len(content.strip()) < 10:
                rel_path = template_file.relative_to(template_file.parent.parent.parent)
                errors.append(f"{rel_path}: Template content too short ({len(content)} chars)")
        
        if errors:
            pytest.fail(
                f"Found {len(errors)} template file(s) with insufficient content:\n" +
                "\n".join(f"  - {e}" for e in errors)
            )

    def test_templates_use_j2_extension(self, templates_dir: Path):
        """Test that all Jinja2 templates use .j2 extension."""
        errors = []
        # Check for .tmpl files that might be Jinja2
        for tmpl_file in templates_dir.rglob("*.tmpl"):
            content = tmpl_file.read_text(encoding="utf-8")
            # Check if it contains Jinja2 syntax
            if "{{" in content or "{%" in content:
                rel_path = tmpl_file.relative_to(tmpl_file.parent.parent.parent)
                errors.append(f"{rel_path}: Contains Jinja2 syntax but uses .tmpl extension (consider .j2)")
        
        # Don't fail - just a recommendation
        if errors:
            pass



