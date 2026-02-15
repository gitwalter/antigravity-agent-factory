"""
End-to-end integration tests for project generation.

Tests cover:
- Complete project generation from blueprints
- Generated file structure validation
- Generated content validation
- Multi-blueprint generation consistency
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.core.generate_project import ProjectConfig, ProjectGenerator


class TestFullProjectGeneration:
    """Tests for complete project generation."""

    def test_generate_creates_complete_structure(self, temp_output_dir):
        """Test that generation creates complete directory structure."""
        config = ProjectConfig(
            project_name="complete-structure-test",
            project_description="Testing complete structure",
            primary_language="python",
            agents=["code-reviewer"],
            skills=["bugfix-workflow"],
            triggers=["jira", "confluence"],
        )

        generator = ProjectGenerator(config, str(temp_output_dir))
        result = generator.generate()

        assert result["success"]

        # Verify directory structure
        expected_dirs = [
            ".agent/agents",
            ".agent/skills",
            "knowledge",
            "templates",
            "workflows",
            "scripts",
            "diagrams",
            "docs",
            "src",
        ]

        for dir_path in expected_dirs:
            assert (
                temp_output_dir / dir_path
            ).exists(), f"Missing directory: {dir_path}"

    def test_generate_creates_cursorrules(self, temp_output_dir):
        """Test that .agentrules is created with correct content."""
        config = ProjectConfig(
            project_name="cursorrules-test",
            project_description="Testing cursorrules generation",
            domain="testing-domain",
            primary_language="typescript",
            style_guide="google",
        )

        generator = ProjectGenerator(config, str(temp_output_dir))
        result = generator.generate()

        assert result["success"]

        cursorrules_path = temp_output_dir / ".agentrules"
        assert cursorrules_path.exists()

        content = cursorrules_path.read_text(encoding="utf-8")
        assert "cursorrules-test" in content
        assert "Testing cursorrules generation" in content
        assert "typescript" in content
        assert "testing-domain" in content

    def test_generate_creates_readme(self, temp_output_dir):
        """Test that README.md is created with correct content."""
        config = ProjectConfig(
            project_name="readme-test-project",
            project_description="Testing README generation",
            domain="readme-domain",
        )

        generator = ProjectGenerator(config, str(temp_output_dir))
        result = generator.generate()

        assert result["success"]

        readme_path = temp_output_dir / "README.md"
        assert readme_path.exists()

        content = readme_path.read_text(encoding="utf-8")
        assert "readme-test-project" in content
        assert "Testing README generation" in content

    def test_generate_creates_agents(self, temp_output_dir):
        """Test that agent files are created when specified."""
        config = ProjectConfig(
            project_name="agents-test", agents=["code-reviewer", "test-generator"]
        )

        generator = ProjectGenerator(config, str(temp_output_dir))
        result = generator.generate()

        assert result["success"]

        agents_dir = temp_output_dir / ".agent" / "agents"
        assert agents_dir.exists()

        # Check that agent files were created
        agent_files = list(agents_dir.glob("*.md"))
        assert len(agent_files) > 0

    def test_generate_creates_skills(self, temp_output_dir):
        """Test that skill files are created when specified."""
        config = ProjectConfig(
            project_name="skills-test", skills=["bugfix-workflow", "tdd"]
        )

        generator = ProjectGenerator(config, str(temp_output_dir))
        result = generator.generate()

        assert result["success"]

        skills_dir = temp_output_dir / ".agent" / "skills"
        assert skills_dir.exists()

        # Check that skill directories were created
        skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir()]
        assert len(skill_dirs) > 0


class TestBlueprintGeneration:
    """Tests for blueprint-based generation."""

    def test_python_fastapi_blueprint_generation(self, temp_output_dir):
        """Test generation from python-fastapi blueprint."""
        config = ProjectConfig(
            project_name="fastapi-test",
            project_description="FastAPI test project",
            primary_language="python",
            blueprint_id="python-fastapi",
            agents=["code-reviewer"],
            skills=["bugfix-workflow", "tdd"],
        )

        generator = ProjectGenerator(config, str(temp_output_dir))
        result = generator.generate()

        assert result["success"]
        assert (temp_output_dir / ".agentrules").exists()
        assert (temp_output_dir / "README.md").exists()

    def test_blueprint_generates_knowledge_files(self, temp_output_dir, factory_root):
        """Test that knowledge files are copied from factory."""
        config = ProjectConfig(
            project_name="knowledge-test", blueprint_id="python-fastapi"
        )

        generator = ProjectGenerator(config, str(temp_output_dir))
        result = generator.generate()

        assert result["success"]

        knowledge_dir = temp_output_dir / "knowledge"
        assert knowledge_dir.exists()

        # Check that some knowledge files exist
        knowledge_files = list(knowledge_dir.glob("*.json"))
        assert len(knowledge_files) > 0


class TestGeneratedContentValidation:
    """Tests for validating generated file contents."""

    def test_agent_markdown_has_frontmatter(self, temp_output_dir):
        """Test that generated agent files have YAML frontmatter."""
        config = ProjectConfig(
            project_name="frontmatter-test", agents=["code-reviewer"]
        )

        generator = ProjectGenerator(config, str(temp_output_dir))
        result = generator.generate()

        assert result["success"]

        agents_dir = temp_output_dir / ".agent" / "agents"
        agent_files = list(agents_dir.glob("*.md"))

        for agent_file in agent_files:
            content = agent_file.read_text(encoding="utf-8")
            assert content.startswith(
                "---"
            ), f"Agent {agent_file} should start with frontmatter"
            assert (
                content.count("---") >= 2
            ), f"Agent {agent_file} should have closing frontmatter"

    def test_skill_markdown_has_process_section(self, temp_output_dir):
        """Test that generated skill files have process section."""
        config = ProjectConfig(project_name="process-test", skills=["bugfix-workflow"])

        generator = ProjectGenerator(config, str(temp_output_dir))
        result = generator.generate()

        assert result["success"]

        skills_dir = temp_output_dir / ".agent" / "skills"
        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir():
                skill_file = skill_dir / "SKILL.md"
                if skill_file.exists():
                    content = skill_file.read_text(encoding="utf-8")
                    assert "## Process" in content or "## When to Use" in content

    def test_cursorrules_has_mcp_section_when_configured(self, temp_output_dir):
        """Test that .agentrules has MCP section when servers configured."""
        config = ProjectConfig(
            project_name="mcp-test",
            mcp_servers=[
                {
                    "name": "atlassian",
                    "url": "https://mcp.atlassian.com",
                    "purpose": "Jira",
                },
                {
                    "name": "deepwiki",
                    "url": "https://deepwiki.com",
                    "purpose": "GitHub",
                },
            ],
        )

        generator = ProjectGenerator(config, str(temp_output_dir))
        result = generator.generate()

        assert result["success"]

        cursorrules_path = temp_output_dir / ".agentrules"
        content = cursorrules_path.read_text(encoding="utf-8")
        assert "atlassian" in content
        assert "deepwiki" in content

    def test_templates_are_created(self, temp_output_dir):
        """Test that template files are created."""
        config = ProjectConfig(project_name="templates-test")

        generator = ProjectGenerator(config, str(temp_output_dir))
        result = generator.generate()

        assert result["success"]

        templates_dir = temp_output_dir / "templates"
        template_files = list(templates_dir.glob("*.md"))

        assert len(template_files) > 0, "Template files should be created"


class TestWorkflowGeneration:
    """Tests for workflow file generation."""

    def test_workflows_readme_created(self, temp_output_dir):
        """Test that workflows README is created."""
        config = ProjectConfig(project_name="workflow-readme-test", triggers=["jira"])

        generator = ProjectGenerator(config, str(temp_output_dir))
        result = generator.generate()

        assert result["success"]

        workflows_readme = temp_output_dir / "workflows" / "README.md"
        assert workflows_readme.exists()

    def test_bugfix_workflow_created_with_jira_trigger(self, temp_output_dir):
        """Test that bugfix workflow is created when jira trigger is specified."""
        config = ProjectConfig(project_name="bugfix-workflow-test", triggers=["jira"])

        generator = ProjectGenerator(config, str(temp_output_dir))
        result = generator.generate()

        assert result["success"]

        bugfix_workflow = temp_output_dir / "workflows" / "bugfix_workflow.md"
        assert bugfix_workflow.exists()

    def test_feature_workflow_created_with_confluence_trigger(self, temp_output_dir):
        """Test that feature workflow is created when confluence trigger is specified."""
        config = ProjectConfig(
            project_name="feature-workflow-test", triggers=["confluence"]
        )

        generator = ProjectGenerator(config, str(temp_output_dir))
        result = generator.generate()

        assert result["success"]

        feature_workflow = temp_output_dir / "workflows" / "feature_workflow.md"
        assert feature_workflow.exists()


class TestGenerationErrors:
    """Tests for error handling during generation."""

    def test_missing_agent_pattern_warning(self, temp_output_dir, capsys):
        """Test that missing agent patterns are handled gracefully."""
        config = ProjectConfig(
            project_name="missing-agent-test", agents=["nonexistent-agent"]
        )

        generator = ProjectGenerator(config, str(temp_output_dir))
        result = generator.generate()

        # Should still succeed but with warning
        assert result["success"]

        # The nonexistent agent should not create a file
        agents_dir = temp_output_dir / ".agent" / "agents"
        agent_files = list(agents_dir.glob("nonexistent-agent.md"))
        assert len(agent_files) == 0

    def test_missing_skill_pattern_warning(self, temp_output_dir, capsys):
        """Test that missing skill patterns are handled gracefully."""
        config = ProjectConfig(
            project_name="missing-skill-test", skills=["nonexistent-skill"]
        )

        generator = ProjectGenerator(config, str(temp_output_dir))
        result = generator.generate()

        # Should still succeed but with warning
        assert result["success"]


class TestFileTracking:
    """Tests for file tracking during generation."""

    def test_all_files_tracked(self, temp_output_dir):
        """Test that all generated files are tracked."""
        config = ProjectConfig(
            project_name="tracking-test",
            agents=["code-reviewer"],
            skills=["bugfix-workflow"],
            triggers=["jira"],
        )

        generator = ProjectGenerator(config, str(temp_output_dir))
        result = generator.generate()

        assert result["success"]

        # All tracked files should exist
        for file_path in result["files_created"]:
            assert Path(file_path).exists(), f"Tracked file {file_path} should exist"

    def test_file_count_matches_tracked(self, temp_output_dir):
        """Test that file count matches tracked files."""
        config = ProjectConfig(
            project_name="count-test",
            agents=["code-reviewer"],
            skills=["bugfix-workflow"],
        )

        generator = ProjectGenerator(config, str(temp_output_dir))
        result = generator.generate()

        assert result["success"]
        assert len(result["files_created"]) > 5, "Should create multiple files"
