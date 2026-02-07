"""
Unit tests for ProjectGenerator class.

Tests cover:
- Directory creation
- Blueprint and pattern loading
- Agent and skill rendering from patterns
-Agentrules generation with variable substitution
- File writing and tracking
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.core.generate_project import ProjectGenerator  # noqa: E402


class TestProjectGeneratorInit:
    """Tests for ProjectGenerator initialization."""
    
    def test_init_basic(self, sample_config, temp_output_dir):
        """Test basic initialization."""
        generator = ProjectGenerator(sample_config, str(temp_output_dir))
        
        assert generator.config == sample_config
        assert generator.target_dir == temp_output_dir
        assert generator.generated_files == []
        assert generator.errors == []
    
    def test_init_factory_root(self, sample_config, temp_output_dir, factory_root):
        """Test factory root is correctly determined."""
        generator = ProjectGenerator(sample_config, str(temp_output_dir))
        
        assert generator.factory_root.exists()
        assert (generator.factory_root / "blueprints").exists()
        assert (generator.factory_root / "patterns").exists()


class TestDirectoryCreation:
    """Tests for _create_directories method."""
    
    def test_create_directories_structure(self, sample_generator, temp_output_dir):
        """Test that all expected directories are created."""
        sample_generator._create_directories()
        
        expected_dirs = [
            ".agent/agents",
            ".agent/skills",
            "knowledge",
            "templates",
            "workflows",
            "scripts",
            "diagrams",
            "docs",
            "src"
        ]
        
        for dir_path in expected_dirs:
            full_path = temp_output_dir / dir_path
            assert full_path.exists(), f"Directory {dir_path} should exist"
            assert full_path.is_dir(), f"{dir_path} should be a directory"
    
    def test_create_directories_idempotent(self, sample_generator, temp_output_dir):
        """Test that calling _create_directories twice doesn't cause errors."""
        sample_generator._create_directories()
        sample_generator._create_directories()  # Should not raise
        
        assert (temp_output_dir / ".agent" / "agents").exists()


class TestBlueprintLoading:
    """Tests for _load_blueprint method."""
    
    def test_load_blueprint_valid(self, sample_config, temp_output_dir):
        """Test loading a valid blueprint."""
        sample_config.blueprint_id = "python-fastapi"
        generator = ProjectGenerator(sample_config, str(temp_output_dir))
        
        blueprint = generator._load_blueprint()
        
        assert blueprint is not None
        assert "metadata" in blueprint
        assert "stack" in blueprint
        assert blueprint["metadata"]["blueprintId"] == "python-fastapi"
    
    def test_load_blueprint_none_when_not_specified(self, sample_config, temp_output_dir):
        """Test that None is returned when no blueprint specified."""
        sample_config.blueprint_id = None
        generator = ProjectGenerator(sample_config, str(temp_output_dir))
        
        blueprint = generator._load_blueprint()
        
        assert blueprint is None
    
    def test_load_blueprint_missing(self, sample_config, temp_output_dir):
        """Test loading a non-existent blueprint returns None."""
        sample_config.blueprint_id = "nonexistent-blueprint"
        generator = ProjectGenerator(sample_config, str(temp_output_dir))
        
        blueprint = generator._load_blueprint()
        
        assert blueprint is None


class TestPatternLoading:
    """Tests for _load_pattern method."""
    
    def test_load_pattern_agent_valid(self, sample_generator):
        """Test loading a valid agent pattern."""
        pattern = sample_generator._load_pattern("agents", "code-reviewer")
        
        assert pattern is not None
        assert "metadata" in pattern
        assert "frontmatter" in pattern
        assert "sections" in pattern
        assert pattern["metadata"]["patternId"] == "code-reviewer"
    
    def test_load_pattern_skill_valid(self, sample_generator):
        """Test loading a valid skill pattern."""
        pattern = sample_generator._load_pattern("skills", "bugfix-workflow")
        
        assert pattern is not None
        assert "metadata" in pattern
        assert "frontmatter" in pattern
        assert pattern["metadata"]["patternId"] == "bugfix-workflow"
    
    def test_load_pattern_missing(self, sample_generator):
        """Test loading a non-existent pattern returns None."""
        pattern = sample_generator._load_pattern("agents", "nonexistent-agent")
        
        assert pattern is None
    
    def test_load_pattern_invalid_type(self, sample_generator):
        """Test loading from invalid pattern type returns None."""
        pattern = sample_generator._load_pattern("invalid-type", "code-reviewer")
        
        assert pattern is None


class TestAgentRendering:
    """Tests for _render_agent_from_pattern method."""
    
    def test_render_agent_basic_structure(self, sample_generator):
        """Test that rendered agent has correct markdown structure."""
        pattern = sample_generator._load_pattern("agents", "code-reviewer")
        content = sample_generator._render_agent_from_pattern(pattern)
        
        # Check frontmatter
        assert content.startswith("---")
        assert "name: code-reviewer" in content
        assert "type: agent" in content
        
        # Check sections
        assert "# Code Reviewer Agent" in content
        assert "## Purpose" in content
        assert "## Workflow" in content
    
    def test_render_agent_contains_skills_section(self, sample_generator):
        """Test that rendered agent contains skills used section."""
        pattern = sample_generator._load_pattern("agents", "code-reviewer")
        content = sample_generator._render_agent_from_pattern(pattern)
        
        assert "## Skills Used" in content
        assert "clean-code-review" in content
    
    def test_render_agent_contains_rules(self, sample_generator):
        """Test that rendered agent contains important rules."""
        pattern = sample_generator._load_pattern("agents", "code-reviewer")
        content = sample_generator._render_agent_from_pattern(pattern)
        
        assert "## Important Rules" in content


class TestSkillRendering:
    """Tests for _render_skill_from_pattern method."""
    
    def test_render_skill_basic_structure(self, sample_generator):
        """Test that rendered skill has correct markdown structure."""
        pattern = sample_generator._load_pattern("skills", "bugfix-workflow")
        content = sample_generator._render_skill_from_pattern(pattern)
        
        # Check frontmatter
        assert content.startswith("---")
        assert "name: bugfix-workflow" in content
        assert "type: skill" in content
        
        # Check sections
        assert "# Bugfix Workflow Skill" in content
        assert "## When to Use" in content
        assert "## Process" in content
    
    def test_render_skill_contains_mcp_tools(self, sample_generator):
        """Test that rendered skill contains MCP tools references."""
        pattern = sample_generator._load_pattern("skills", "bugfix-workflow")
        content = sample_generator._render_skill_from_pattern(pattern)
        
        assert "MCP Tools:" in content or "atlassian" in content.lower()
    
    def test_render_skill_contains_fallback(self, sample_generator):
        """Test that rendered skill contains fallback procedures."""
        pattern = sample_generator._load_pattern("skills", "bugfix-workflow")
        content = sample_generator._render_skill_from_pattern(pattern)
        
        assert "## Fallback Procedures" in content


class TestFileWriting:
    """Tests for _write_file method."""
    
    def test_write_file_creates_file(self, sample_generator, temp_output_dir):
        """Test that _write_file creates the file."""
        test_path = temp_output_dir / "test_file.txt"
        content = "Test content"
        
        sample_generator._write_file(test_path, content)
        
        assert test_path.exists()
        assert test_path.read_text() == content
    
    def test_write_file_creates_parent_dirs(self, sample_generator, temp_output_dir):
        """Test that _write_file creates parent directories."""
        test_path = temp_output_dir / "deep" / "nested" / "dir" / "file.txt"
        content = "Nested content"
        
        sample_generator._write_file(test_path, content)
        
        assert test_path.exists()
        assert test_path.read_text() == content
    
    def test_write_file_tracks_files(self, sample_generator, temp_output_dir):
        """Test that written files are tracked."""
        test_path = temp_output_dir / "tracked.txt"
        
        sample_generator._write_file(test_path, "content")
        
        assert str(test_path) in sample_generator.generated_files
    
    def test_write_file_utf8_encoding(self, sample_generator, temp_output_dir):
        """Test that files are written with UTF-8 encoding."""
        test_path = temp_output_dir / "unicode.txt"
        content = "Unicode: äöü ñ 日本語 🚀"
        
        sample_generator._write_file(test_path, content)
        
        assert test_path.read_text(encoding='utf-8') == content


class TestAgentrulesGeneration:
    """Tests for agentrules generation with variable substitution."""
    
    def test_agentrules_variable_substitution(self, sample_config, temp_output_dir):
        """Test that variables are correctly substituted."""
        sample_config.project_name = "test-substitution"
        sample_config.project_description = "Test description for substitution"
        sample_config.primary_language = "typescript"
        sample_config.domain = "web-testing"
        
        generator = ProjectGenerator(sample_config, str(temp_output_dir))
        generator._create_directories()
        generator._generate_agentrules(None)
        
        agentrules_path = temp_output_dir / ".agentrules"
        content = agentrules_path.read_text(encoding='utf-8')
        
        assert "test-substitution" in content
        assert "Test description for substitution" in content
        assert "typescript" in content
        assert "web-testing" in content
    
    def test_agentrules_no_placeholder_remnants(self, sample_generator, temp_output_dir):
        """Test that no unreplaced placeholders remain."""
        sample_generator._create_directories()
        sample_generator._generate_agentrules(None)
        
        agentrules_path = temp_output_dir / ".agentrules"
        content = agentrules_path.read_text(encoding='utf-8')
        
        # Check that common placeholders are replaced
        assert "{PROJECT_NAME}" not in content
        assert "{PROJECT_DESCRIPTION}" not in content
        assert "{PRIMARY_LANGUAGE}" not in content


class TestMcpServerSection:
    """Tests for MCP server section generation."""
    
    def test_mcp_section_with_servers(self, sample_config, temp_output_dir):
        """Test MCP section generation when servers are configured."""
        sample_config.mcp_servers = [
            {"name": "atlassian", "url": "https://mcp.atlassian.com", "purpose": "Jira"},
            {"name": "deepwiki", "url": "https://deepwiki.com", "purpose": "GitHub"}
        ]
        
        generator = ProjectGenerator(sample_config, str(temp_output_dir))
        mcp_section = generator._generate_mcp_section()
        
        assert "atlassian" in mcp_section
        assert "deepwiki" in mcp_section
        assert "Jira" in mcp_section
        assert "GitHub" in mcp_section
    
    def test_mcp_section_table_format(self, sample_config, temp_output_dir):
        """Test that MCP section uses markdown table format."""
        sample_config.mcp_servers = [
            {"name": "test", "url": "https://test.com", "purpose": "Testing"}
        ]
        
        generator = ProjectGenerator(sample_config, str(temp_output_dir))
        mcp_section = generator._generate_mcp_section()
        
        assert "| Server |" in mcp_section
        assert "|--------|" in mcp_section


class TestFullGeneration:
    """Tests for complete project generation."""
    
    def test_generate_returns_result_dict(self, sample_generator):
        """Test that generate() returns proper result dictionary."""
        result = sample_generator.generate()
        
        assert "success" in result
        assert "target_dir" in result
        assert "files_created" in result
        assert "errors" in result
    
    def test_generate_creates_expected_files(self, sample_generator, temp_output_dir):
        """Test that generate() creates expected files."""
        result = sample_generator.generate()
        
        assert result["success"]
        assert (temp_output_dir / ".agentrules").exists()
        assert (temp_output_dir / "README.md").exists()
        assert (temp_output_dir / "workflows" / "README.md").exists()
    
    def test_generate_tracks_all_files(self, sample_generator):
        """Test that all generated files are tracked."""
        result = sample_generator.generate()
        
        assert len(result["files_created"]) > 0
        
        for file_path in result["files_created"]:
            assert Path(file_path).exists()
