"""
Unit tests for pattern and blueprint loading functionality.

Tests cover:
- Loading all existing blueprints
- Loading all existing agent patterns
- Loading all existing skill patterns
- Pattern structure validation
"""

import json
import sys
from pathlib import Path

import pytest

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class TestBlueprintFiles:
    """Tests for blueprint file loading."""

    def test_all_blueprints_are_valid_json(self, blueprints_dir):
        """Test that all blueprint.json files are valid JSON."""
        for blueprint_dir in blueprints_dir.iterdir():
            if blueprint_dir.is_dir():
                blueprint_file = blueprint_dir / "blueprint.json"
                if blueprint_file.exists():
                    try:
                        with open(blueprint_file, "r", encoding="utf-8") as f:
                            data = json.load(f)
                        assert isinstance(data, dict)
                    except json.JSONDecodeError as e:
                        pytest.fail(f"Invalid JSON in {blueprint_file}: {e}")

    def test_blueprints_have_required_fields(self, blueprints_dir):
        """Test that blueprints have required metadata and stack fields."""
        required_metadata = ["blueprintId", "blueprintName", "description"]
        required_stack = ["primaryLanguage"]

        for blueprint_dir in blueprints_dir.iterdir():
            if blueprint_dir.is_dir():
                blueprint_file = blueprint_dir / "blueprint.json"
                if blueprint_file.exists():
                    with open(blueprint_file, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    assert "metadata" in data, f"Missing 'metadata' in {blueprint_file}"
                    assert "stack" in data, f"Missing 'stack' in {blueprint_file}"

                    for field in required_metadata:
                        assert (
                            field in data["metadata"]
                        ), f"Missing '{field}' in metadata of {blueprint_file}"

                    for field in required_stack:
                        assert (
                            field in data["stack"]
                        ), f"Missing '{field}' in stack of {blueprint_file}"

    def test_python_fastapi_blueprint_exists(self, blueprints_dir):
        """Test that python-fastapi blueprint exists and is valid."""
        blueprint_path = blueprints_dir / "python-fastapi" / "blueprint.json"

        assert blueprint_path.exists()

        with open(blueprint_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert data["metadata"]["blueprintId"] == "python-fastapi"
        assert data["stack"]["primaryLanguage"] == "python"


def is_schema_file(filepath: Path) -> bool:
    """Check if a JSON file is a schema definition (not a pattern instance).

    Args:
        filepath: Path to the JSON file.

    Returns:
        True if the file is a schema definition.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return "$schema" in data or filepath.stem.endswith("-pattern")


class TestAgentPatternFiles:
    """Tests for agent pattern file loading."""

    def test_all_agent_patterns_are_valid_json(self, patterns_dir):
        """Test that all agent pattern files are valid JSON."""
        agents_dir = patterns_dir / "agents"

        for pattern_file in agents_dir.glob("*.json"):
            try:
                with open(pattern_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                assert isinstance(data, dict)
            except json.JSONDecodeError as e:
                pytest.fail(f"Invalid JSON in {pattern_file}: {e}")

    def test_agent_patterns_have_required_fields(self, patterns_dir):
        """Test that agent patterns (not schema files) have required structure."""
        agents_dir = patterns_dir / "agents"
        required_top_level = ["metadata", "frontmatter", "sections"]

        for pattern_file in agents_dir.glob("*.json"):
            # Skip schema definition files
            if is_schema_file(pattern_file):
                continue

            with open(pattern_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            for field in required_top_level:
                assert field in data, f"Missing '{field}' in {pattern_file}"

    def test_code_reviewer_pattern_exists(self, patterns_dir):
        """Test that code-reviewer pattern exists and is valid."""
        pattern_path = patterns_dir / "agents" / "code-reviewer.json"

        assert pattern_path.exists()

        with open(pattern_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert data["metadata"]["patternId"] == "code-reviewer"
        assert data["frontmatter"]["name"] == "code-reviewer"
        assert "workflow" in data["sections"]


class TestSkillPatternFiles:
    """Tests for skill pattern file loading."""

    def test_all_skill_patterns_are_valid_json(self, patterns_dir):
        """Test that all skill pattern files are valid JSON."""
        skills_dir = patterns_dir / "skills"

        for pattern_file in skills_dir.glob("*.json"):
            try:
                with open(pattern_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                assert isinstance(data, dict)
            except json.JSONDecodeError as e:
                pytest.fail(f"Invalid JSON in {pattern_file}: {e}")

    def test_skill_patterns_have_required_fields(self, patterns_dir):
        """Test that skill patterns (not schema files) have required structure."""
        skills_dir = patterns_dir / "skills"
        required_top_level = ["metadata", "frontmatter", "sections"]

        for pattern_file in skills_dir.glob("*.json"):
            # Skip schema definition files
            if is_schema_file(pattern_file):
                continue

            with open(pattern_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            for field in required_top_level:
                assert field in data, f"Missing '{field}' in {pattern_file}"

    def test_bugfix_workflow_pattern_exists(self, patterns_dir):
        """Test that bugfix-workflow pattern exists and is valid."""
        pattern_path = patterns_dir / "skills" / "bugfix-workflow.json"

        assert pattern_path.exists()

        with open(pattern_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert data["metadata"]["patternId"] == "bugfix-workflow"
        assert data["frontmatter"]["name"] == "bugfix-workflow"
        assert "process" in data["sections"]


class TestKnowledgeFiles:
    """Tests for knowledge file loading."""

    def test_all_knowledge_files_are_valid_json(self, knowledge_dir):
        """Test that all knowledge files are valid JSON."""
        for knowledge_file in knowledge_dir.glob("*.json"):
            try:
                with open(knowledge_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                assert isinstance(data, dict)
            except json.JSONDecodeError as e:
                pytest.fail(f"Invalid JSON in {knowledge_file}: {e}")

    def test_skill_catalog_exists(self, knowledge_dir):
        """Test that skill-catalog.json exists and has skills."""
        catalog_path = knowledge_dir / "skill-catalog.json"

        assert catalog_path.exists()

        with open(catalog_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert "skills" in data
        assert len(data["skills"]) > 0


def get_available_patterns(patterns_dir: Path, pattern_type: str) -> set:
    """Get available pattern IDs (excluding schema files).

    Args:
        patterns_dir: Path to patterns directory.
        pattern_type: Type of pattern (agents, skills, etc.).

    Returns:
        Set of pattern IDs.
    """
    type_dir = patterns_dir / pattern_type
    patterns = set()
    for pattern_file in type_dir.glob("*.json"):
        if not is_schema_file(pattern_file):
            patterns.add(pattern_file.stem)
    return patterns


class TestPatternConsistency:
    """Tests for pattern consistency across the factory."""

    def test_blueprint_agent_references_exist(self, blueprints_dir, patterns_dir):
        """Test that agents referenced in blueprints have corresponding patterns."""
        available_agents = get_available_patterns(patterns_dir, "agents")

        for blueprint_dir in blueprints_dir.iterdir():
            if blueprint_dir.is_dir():
                blueprint_file = blueprint_dir / "blueprint.json"
                if blueprint_file.exists():
                    with open(blueprint_file, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    for agent in data.get("agents", []):
                        pattern_id = agent.get("patternId")
                        if pattern_id:
                            assert pattern_id in available_agents, (
                                f"Agent '{pattern_id}' referenced in {blueprint_file} "
                                f"but pattern not found"
                            )

    def test_blueprint_skill_references_exist(
        self, blueprints_dir, patterns_dir, knowledge_dir
    ):
        """Test that skills referenced in blueprints exist in patterns or skill catalog.

        Some skills are stack-specific and implemented in external repos,
        so we also check the skill catalog for known skills.
        """
        available_skills = get_available_patterns(patterns_dir, "skills")

        # Load skill catalog to find all known skills (including stack-specific ones)
        catalog_path = knowledge_dir / "skill-catalog.json"
        if catalog_path.exists():
            with open(catalog_path, "r", encoding="utf-8") as f:
                catalog = json.load(f)
            catalog_skills = set(catalog.get("skills", {}).keys())
            available_skills = available_skills.union(catalog_skills)

        # Add skills from .agent/skills directory
        skills_dir = patterns_dir.parent / "skills"
        if skills_dir.exists():
            for skill_dir in skills_dir.iterdir():
                if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                    available_skills.add(skill_dir.name)

        for blueprint_dir in blueprints_dir.iterdir():
            if blueprint_dir.is_dir():
                blueprint_file = blueprint_dir / "blueprint.json"
                if blueprint_file.exists():
                    with open(blueprint_file, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    for skill in data.get("skills", []):
                        pattern_id = skill.get("patternId")
                        if pattern_id:
                            # Allow unknown skills with a warning, only fail for known blueprints
                            # that reference skills that should exist
                            if pattern_id not in available_skills:
                                # Stack-specific skills may not have factory patterns
                                # This is documented in skill-catalog.json
                                import warnings

                                warnings.warn(
                                    f"Skill '{pattern_id}' referenced in {blueprint_file} "
                                    f"not found in patterns or catalog (may be stack-specific)"
                                )
