"""
YAML Frontmatter validation tests.

Tests validate that markdown files with YAML frontmatter have valid
syntax, catching errors before they break tooling or documentation.

This prevents YAML parsing errors like:
- Comma-separated values that should be arrays
- Unbalanced quotes
- Invalid key-value syntax
"""

import sys
from pathlib import Path

import pytest

# Add project root and scripts to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from scripts.validation.validate_yaml_frontmatter import (
    extract_frontmatter,
    validate_yaml_syntax,
    validate_file,
    find_markdown_files,
)


class TestFrontmatterExtraction:
    """Tests for extracting YAML frontmatter from markdown files."""

    def test_extract_valid_frontmatter(self):
        """Test extraction of valid frontmatter."""
        content = """---
name: test-agent
description: A test agent
---

# Test Agent

Content here.
"""
        result = extract_frontmatter(content)
        assert result is not None
        assert "name: test-agent" in result
        assert "description: A test agent" in result

    def test_extract_no_frontmatter(self):
        """Test extraction when no frontmatter exists."""
        content = """# Just a Heading

No frontmatter here.
"""
        result = extract_frontmatter(content)
        assert result is None

    def test_extract_frontmatter_only_at_start(self):
        """Test that frontmatter must be at the start of the file."""
        content = """Some content first

---
name: not-frontmatter
---
"""
        result = extract_frontmatter(content)
        assert result is None

    def test_extract_multiline_frontmatter(self):
        """Test extraction of multiline frontmatter values."""
        content = """---
name: test
description: |
  This is a multiline
  description value
tags:
  - one
  - two
---

# Content
"""
        result = extract_frontmatter(content)
        assert result is not None
        assert "multiline" in result


class TestYamlSyntaxValidation:
    """Tests for YAML syntax validation."""

    def test_valid_simple_yaml(self):
        """Test that valid simple YAML passes."""
        yaml_content = """name: test-agent
description: A simple test
type: agent
"""
        error = validate_yaml_syntax(yaml_content, "test.md")
        assert error is None

    def test_valid_yaml_with_array(self):
        """Test that valid YAML array syntax passes."""
        yaml_content = """name: test-agent
activation:
  - "trigger one"
  - "trigger two"
  - trigger three
"""
        error = validate_yaml_syntax(yaml_content, "test.md")
        assert error is None

    def test_invalid_comma_separated_strings(self, tmp_path):
        """Test detection of comma-separated quoted strings (common error)."""
        # Use full file validation to test the complete pipeline
        test_file = tmp_path / "comma_sep.md"
        test_file.write_text(
            """---
name: test-agent
activation: "value1", "value2", value3
---

# Test
""",
            encoding="utf-8",
        )

        is_valid, error = validate_file(test_file)
        assert (
            is_valid is False
        ), "Comma-separated strings should be detected as invalid"
        assert error is not None
        # PyYAML reports "found ','" or our custom check reports "comma" or "array"
        error_lower = error.lower()
        assert any(
            x in error_lower for x in ["comma", "array", "','"]
        ), f"Error should mention comma or array issue, got: {error}"

    def test_invalid_tab_indentation(self):
        """Test detection of tab characters."""
        yaml_content = "name: test\n\tdescription: tabbed"
        error = validate_yaml_syntax(yaml_content, "test.md")
        assert error is not None
        assert "tab" in error.lower()

    def test_unbalanced_quotes(self, tmp_path):
        """Test detection of unbalanced quotes."""
        # Use full file validation to test the complete pipeline
        test_file = tmp_path / "unbalanced.md"
        test_file.write_text(
            """---
name: test
description: "unbalanced quote
---

# Test
""",
            encoding="utf-8",
        )

        is_valid, error = validate_file(test_file)
        assert is_valid is False, "Unbalanced quotes should be detected as invalid"
        assert error is not None
        assert "quote" in error.lower()

    def test_valid_yaml_with_special_chars(self):
        """Test that valid YAML with special characters passes."""
        yaml_content = """name: test-agent
description: "Contains: colons and 'quotes'"
url: https://example.com
"""
        error = validate_yaml_syntax(yaml_content, "test.md")
        assert error is None


class TestFileValidation:
    """Tests for full file validation."""

    def test_validate_file_with_valid_frontmatter(self, tmp_path):
        """Test validation of file with valid frontmatter."""
        test_file = tmp_path / "valid.md"
        test_file.write_text(
            """---
name: test-agent
description: Valid agent
type: agent
---

# Test Agent

Content here.
""",
            encoding="utf-8",
        )

        is_valid, error = validate_file(test_file)
        assert is_valid is True
        assert error is None

    def test_validate_file_without_frontmatter(self, tmp_path):
        """Test validation of file without frontmatter (should pass)."""
        test_file = tmp_path / "no_frontmatter.md"
        test_file.write_text(
            """# Just a Document

No frontmatter here, and that's fine.
""",
            encoding="utf-8",
        )

        is_valid, error = validate_file(test_file)
        assert is_valid is True
        assert error is None

    def test_validate_file_with_invalid_frontmatter(self, tmp_path):
        """Test validation of file with invalid frontmatter."""
        test_file = tmp_path / "invalid.md"
        test_file.write_text(
            """---
name: test-agent
activation: "value1", "value2", value3
---

# Test Agent
""",
            encoding="utf-8",
        )

        is_valid, error = validate_file(test_file)
        assert is_valid is False
        assert error is not None


class TestFindMarkdownFiles:
    """Tests for markdown file discovery."""

    def test_find_markdown_files_returns_list(self, project_root):
        """Test that find_markdown_files returns a list."""
        files = find_markdown_files(project_root)
        assert isinstance(files, list)
        assert len(files) > 0

    def test_find_markdown_files_all_are_md(self, project_root):
        """Test that all found files are markdown files."""
        files = find_markdown_files(project_root)
        for f in files:
            assert f.suffix == ".md", f"Expected .md file, got {f}"

    def test_find_markdown_files_includes_agents(self, project_root):
        """Test that agent files are included."""
        files = find_markdown_files(project_root)
        agent_files = [
            f for f in files if ".agent/agents" in str(f) or ".agent\\agents" in str(f)
        ]
        assert len(agent_files) > 0, "Should find agent markdown files"

    def test_find_markdown_files_includes_skills(self, project_root):
        """Test that skill files are included."""
        files = find_markdown_files(project_root)
        skill_files = [
            f for f in files if ".agent/skills" in str(f) or ".agent\\skills" in str(f)
        ]
        assert len(skill_files) > 0, "Should find skill markdown files"


class TestAllProjectFilesValid:
    """Tests that all markdown files in the project have valid frontmatter."""

    def test_all_agent_files_have_valid_yaml(self, project_root):
        """Test that all agent files have valid YAML frontmatter."""
        agents_dir = project_root / ".agent" / "agents"
        if not agents_dir.exists():
            pytest.skip("Agents directory not found")

        errors = []
        for md_file in agents_dir.rglob("*.md"):
            is_valid, error = validate_file(md_file)
            if not is_valid:
                errors.append(f"{md_file.relative_to(project_root)}: {error}")

        if errors:
            pytest.fail(
                "Agent files with invalid YAML frontmatter:\n"
                + "\n".join(f"  - {e}" for e in errors)
            )

    def test_all_skill_files_have_valid_yaml(self, project_root):
        """Test that all skill files have valid YAML frontmatter."""
        skills_dir = project_root / ".agent" / "skills"
        if not skills_dir.exists():
            pytest.skip("Skills directory not found")

        errors = []
        for md_file in skills_dir.rglob("*.md"):
            is_valid, error = validate_file(md_file)
            if not is_valid:
                errors.append(f"{md_file.relative_to(project_root)}: {error}")

        if errors:
            pytest.fail(
                "Skill files with invalid YAML frontmatter:\n"
                + "\n".join(f"  - {e}" for e in errors)
            )

    def test_all_docs_have_valid_yaml(self, project_root):
        """Test that all doc files have valid YAML frontmatter."""
        docs_dir = project_root / "docs"
        if not docs_dir.exists():
            pytest.skip("Docs directory not found")

        errors = []
        for md_file in docs_dir.rglob("*.md"):
            is_valid, error = validate_file(md_file)
            if not is_valid:
                errors.append(f"{md_file.relative_to(project_root)}: {error}")

        if errors:
            pytest.fail(
                "Doc files with invalid YAML frontmatter:\n"
                + "\n".join(f"  - {e}" for e in errors)
            )

    def test_all_markdown_files_valid(self, project_root):
        """Comprehensive test: all markdown files in standard locations are valid."""
        files = find_markdown_files(project_root)

        errors = []
        for md_file in files:
            is_valid, error = validate_file(md_file)
            if not is_valid:
                errors.append(f"{md_file.relative_to(project_root)}: {error}")

        if errors:
            pytest.fail(
                f"Found {len(errors)} file(s) with invalid YAML frontmatter:\n"
                + "\n".join(f"  - {e}" for e in errors)
                + "\n\nRun: python scripts/validation/validate_yaml_frontmatter.py --verbose"
            )


class TestEdgeCases:
    """Tests for edge cases and special scenarios."""

    def test_empty_frontmatter(self, tmp_path):
        """Test handling of empty frontmatter."""
        test_file = tmp_path / "empty_fm.md"
        test_file.write_text(
            """---
---

# Empty frontmatter
""",
            encoding="utf-8",
        )

        is_valid, error = validate_file(test_file)
        # Empty frontmatter should be valid (just no content)
        assert is_valid is True

    def test_frontmatter_with_comments(self, tmp_path):
        """Test that YAML comments are handled."""
        test_file = tmp_path / "comments.md"
        test_file.write_text(
            """---
# This is a comment
name: test
# Another comment
type: agent
---

# Content
""",
            encoding="utf-8",
        )

        is_valid, error = validate_file(test_file)
        assert is_valid is True

    def test_frontmatter_with_nested_objects(self, tmp_path):
        """Test handling of nested YAML objects."""
        test_file = tmp_path / "nested.md"
        test_file.write_text(
            """---
name: test
config:
  option1: value1
  option2: value2
  nested:
    deep: value
---

# Content
""",
            encoding="utf-8",
        )

        is_valid, error = validate_file(test_file)
        assert is_valid is True

    def test_unreadable_file(self, tmp_path):
        """Test handling of file read errors."""
        # Create a path that doesn't exist
        fake_file = tmp_path / "nonexistent.md"

        is_valid, error = validate_file(fake_file)
        assert is_valid is False
        assert error is not None
