"""
Comprehensive tests for skill file structure validation.

Tests validate that all skill files have:
- Valid YAML frontmatter with required fields (name, description, type)
- Proper markdown sections (When to Use, Prerequisites, Process, Best Practices)
- Correct file structure and naming conventions
"""

import re
import sys
from pathlib import Path
from typing import List

import pytest
import yaml

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.validation.validate_yaml_frontmatter import (
    extract_frontmatter,
    validate_yaml_syntax,
)


class TestSkillFileStructure:
    """Tests for skill file structure and organization."""

    @pytest.fixture
    def skills_dir(self, factory_root: Path) -> Path:
        """Get the skills directory."""
        return factory_root / ".agent" / "skills"

    @pytest.fixture
    def all_skill_files(self, skills_dir: Path) -> List[Path]:
        """Get all skill files recursively."""
        skill_files = []
        for skill_dir in skills_dir.rglob("SKILL.md"):
            skill_files.append(skill_dir)
        return skill_files

    def test_skill_files_exist(self, all_skill_files: List[Path]):
        """Test that skill files are found."""
        assert len(all_skill_files) > 0, "Should find at least one skill file"

    def test_skill_files_have_yaml_frontmatter(self, all_skill_files: List[Path]):
        """Test that all skill files have YAML frontmatter."""
        errors = []
        for skill_file in all_skill_files:
            content = skill_file.read_text(encoding="utf-8")
            frontmatter = extract_frontmatter(content)
            if not frontmatter:
                errors.append(
                    f"{skill_file.relative_to(skill_file.parent.parent.parent.parent)}: Missing YAML frontmatter"
                )

        if errors:
            pytest.fail(
                f"Found {len(errors)} skill file(s) without YAML frontmatter:\n"
                + "\n".join(f"  - {e}" for e in errors)
            )

    def test_skill_frontmatter_has_required_fields(self, all_skill_files: List[Path]):
        """Test that skill frontmatter has required fields: name, description, type."""
        errors = []
        for skill_file in all_skill_files:
            content = skill_file.read_text(encoding="utf-8")
            frontmatter = extract_frontmatter(content)
            if not frontmatter:
                continue

            try:
                data = yaml.safe_load(frontmatter)
                required_fields = ["name", "description", "type"]
                missing_fields = [
                    field for field in required_fields if field not in data
                ]

                if missing_fields:
                    rel_path = skill_file.relative_to(
                        skill_file.parent.parent.parent.parent
                    )
                    errors.append(
                        f"{rel_path}: Missing required fields: {', '.join(missing_fields)}"
                    )
            except yaml.YAMLError as e:
                rel_path = skill_file.relative_to(
                    skill_file.parent.parent.parent.parent
                )
                errors.append(f"{rel_path}: Invalid YAML: {e}")

        if errors:
            pytest.fail(
                f"Found {len(errors)} skill file(s) with missing required fields:\n"
                + "\n".join(f"  - {e}" for e in errors)
            )

    def test_skill_frontmatter_type_is_skill(self, all_skill_files: List[Path]):
        """Test that skill frontmatter type field is 'skill'."""
        errors = []
        for skill_file in all_skill_files:
            content = skill_file.read_text(encoding="utf-8")
            frontmatter = extract_frontmatter(content)
            if not frontmatter:
                continue

            try:
                data = yaml.safe_load(frontmatter)
                skill_type = data.get("type", "")
                if skill_type != "skill":
                    rel_path = skill_file.relative_to(
                        skill_file.parent.parent.parent.parent
                    )
                    errors.append(
                        f"{rel_path}: type should be 'skill', got '{skill_type}'"
                    )
            except yaml.YAMLError:
                continue

        if errors:
            pytest.fail(
                f"Found {len(errors)} skill file(s) with incorrect type:\n"
                + "\n".join(f"  - {e}" for e in errors)
            )

    def test_skill_frontmatter_name_matches_directory(
        self, all_skill_files: List[Path]
    ):
        """Test that skill name matches the directory name."""
        errors = []
        for skill_file in all_skill_files:
            content = skill_file.read_text(encoding="utf-8")
            frontmatter = extract_frontmatter(content)
            if not frontmatter:
                continue

            try:
                data = yaml.safe_load(frontmatter)
                skill_name = data.get("name", "")
                directory_name = skill_file.parent.name

                if skill_name != directory_name:
                    rel_path = skill_file.relative_to(
                        skill_file.parent.parent.parent.parent
                    )
                    errors.append(
                        f"{rel_path}: name '{skill_name}' doesn't match directory '{directory_name}'"
                    )
            except yaml.YAMLError:
                continue

        if errors:
            pytest.fail(
                f"Found {len(errors)} skill file(s) with name mismatch:\n"
                + "\n".join(f"  - {e}" for e in errors)
            )

    def test_skill_frontmatter_valid_yaml(self, all_skill_files: List[Path]):
        """Test that skill frontmatter has valid YAML syntax."""
        errors = []
        for skill_file in all_skill_files:
            content = skill_file.read_text(encoding="utf-8")
            frontmatter = extract_frontmatter(content)
            if not frontmatter:
                continue

            error = validate_yaml_syntax(frontmatter, str(skill_file))
            if error:
                rel_path = skill_file.relative_to(
                    skill_file.parent.parent.parent.parent
                )
                errors.append(f"{rel_path}: {error}")

        if errors:
            pytest.fail(
                f"Found {len(errors)} skill file(s) with invalid YAML:\n"
                + "\n".join(f"  - {e}" for e in errors)
            )


class TestSkillMarkdownSections:
    """Tests for required markdown sections in skill files."""

    @pytest.fixture
    def skills_dir(self, factory_root: Path) -> Path:
        """Get the skills directory."""
        return factory_root / ".agent" / "skills"

    @pytest.fixture
    def all_skill_files(self, skills_dir: Path) -> List[Path]:
        """Get all skill files recursively."""
        skill_files = []
        for skill_dir in skills_dir.rglob("SKILL.md"):
            skill_files.append(skill_dir)
        return skill_files

    def test_skill_has_when_to_use_section(self, all_skill_files: List[Path]):
        """Test that skill files have 'When to Use' section."""
        errors = []
        for skill_file in all_skill_files:
            content = skill_file.read_text(encoding="utf-8")
            # Check for "## When to Use" or "### When to Use"
            if not re.search(
                r"^##+\s+When to Use", content, re.MULTILINE | re.IGNORECASE
            ):
                rel_path = skill_file.relative_to(
                    skill_file.parent.parent.parent.parent
                )
                errors.append(f"{rel_path}: Missing 'When to Use' section")

        if errors:
            pytest.fail(
                f"Found {len(errors)} skill file(s) without 'When to Use' section:\n"
                + "\n".join(f"  - {e}" for e in errors)
            )

    def test_skill_has_prerequisites_section(self, all_skill_files: List[Path]):
        """Test that skill files have 'Prerequisites' section."""
        errors = []
        for skill_file in all_skill_files:
            content = skill_file.read_text(encoding="utf-8")
            # Check for "## Prerequisites" or "### Prerequisites"
            if not re.search(
                r"^##+\s+Prerequisites", content, re.MULTILINE | re.IGNORECASE
            ):
                rel_path = skill_file.relative_to(
                    skill_file.parent.parent.parent.parent
                )
                errors.append(f"{rel_path}: Missing 'Prerequisites' section")

        if errors:
            pytest.fail(
                f"Found {len(errors)} skill file(s) without 'Prerequisites' section:\n"
                + "\n".join(f"  - {e}" for e in errors)
            )

    def test_skill_has_process_section(self, all_skill_files: List[Path]):
        """Test that skill files have 'Process' section."""
        errors = []
        for skill_file in all_skill_files:
            content = skill_file.read_text(encoding="utf-8")
            # Check for "## Process" or "### Process"
            if not re.search(r"^##+\s+Process", content, re.MULTILINE | re.IGNORECASE):
                rel_path = skill_file.relative_to(
                    skill_file.parent.parent.parent.parent
                )
                errors.append(f"{rel_path}: Missing 'Process' section")

        if errors:
            pytest.fail(
                f"Found {len(errors)} skill file(s) without 'Process' section:\n"
                + "\n".join(f"  - {e}" for e in errors)
            )

    def test_skill_has_best_practices_section(self, all_skill_files: List[Path]):
        """Test that skill files have 'Best Practices' section."""
        errors = []
        for skill_file in all_skill_files:
            content = skill_file.read_text(encoding="utf-8")
            # Check for "## Best Practices" or "### Best Practices"
            if not re.search(
                r"^##+\s+Best Practices", content, re.MULTILINE | re.IGNORECASE
            ):
                rel_path = skill_file.relative_to(
                    skill_file.parent.parent.parent.parent
                )
                errors.append(f"{rel_path}: Missing 'Best Practices' section")

        if errors:
            pytest.fail(
                f"Found {len(errors)} skill file(s) without 'Best Practices' section:\n"
                + "\n".join(f"  - {e}" for e in errors)
            )

    def test_skill_sections_have_content(self, all_skill_files: List[Path]):
        """Test that skill sections have actual content (not just headers)."""
        errors = []
        for skill_file in all_skill_files:
            content = skill_file.read_text(encoding="utf-8")

            # Extract content after each section header
            sections = {
                "When to Use": re.search(
                    r"^##+\s+When to Use\s*\n(.*?)(?=^##+|\Z)",
                    content,
                    re.MULTILINE | re.DOTALL | re.IGNORECASE,
                ),
                "Prerequisites": re.search(
                    r"^##+\s+Prerequisites\s*\n(.*?)(?=^##+|\Z)",
                    content,
                    re.MULTILINE | re.DOTALL | re.IGNORECASE,
                ),
                "Process": re.search(
                    r"^##+\s+Process\s*\n(.*?)(?=^##+|\Z)",
                    content,
                    re.MULTILINE | re.DOTALL | re.IGNORECASE,
                ),
                "Best Practices": re.search(
                    r"^##+\s+Best Practices\s*\n(.*?)(?=^##+|\Z)",
                    content,
                    re.MULTILINE | re.DOTALL | re.IGNORECASE,
                ),
            }

            rel_path = skill_file.relative_to(skill_file.parent.parent.parent.parent)
            for section_name, match in sections.items():
                if match:
                    section_content = match.group(1).strip()
                    # Check if section has meaningful content (more than just whitespace)
                    if len(section_content) < 10:  # Arbitrary minimum length
                        errors.append(
                            f"{rel_path}: '{section_name}' section has insufficient content"
                        )
                else:
                    errors.append(
                        f"{rel_path}: '{section_name}' section not found or empty"
                    )

        if errors:
            pytest.fail(
                f"Found {len(errors)} skill file(s) with empty or missing sections:\n"
                + "\n".join(f"  - {e}" for e in errors[:20])  # Limit output
                + (f"\n... and {len(errors) - 20} more" if len(errors) > 20 else "")
            )


class TestSkillFileNaming:
    """Tests for skill file naming conventions."""

    @pytest.fixture
    def skills_dir(self, factory_root: Path) -> Path:
        """Get the skills directory."""
        return factory_root / ".agent" / "skills"

    def test_skill_files_named_skill_md(self, skills_dir: Path):
        """Test that the primary skill files are named SKILL.md.
        Note: Subdirectories like references/ or assets/ can contain other .md files.
        """
        errors = []
        # Walk only Level 1 pattern directories and Level 2 skill directories
        for pattern_dir in skills_dir.iterdir():
            if not pattern_dir.is_dir():
                continue
            for skill_dir in pattern_dir.iterdir():
                if not skill_dir.is_dir():
                    continue
                # Check for any .md file in the skill root that is NOT SKILL.md
                for md_file in skill_dir.glob("*.md"):
                    if md_file.name != "SKILL.md":
                        rel_path = md_file.relative_to(
                            md_file.parent.parent.parent.parent
                        )
                        errors.append(
                            f"{rel_path}: Root skill file should be named SKILL.md, got {md_file.name}"
                        )

        if errors:
            pytest.fail(
                f"Found {len(errors)} skill file(s) with incorrect naming:\n"
                + "\n".join(f"  - {e}" for e in errors)
            )

    def test_skill_directories_use_kebab_case(self, skills_dir: Path):
        """Test that skill directories use kebab-case naming."""
        errors = []
        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir():
                dir_name = skill_dir.name
                # Check for kebab-case (lowercase with hyphens, no underscores or spaces)
                if dir_name != dir_name.lower():
                    errors.append(f"{dir_name}: Should be lowercase")
                if "_" in dir_name:
                    errors.append(f"{dir_name}: Should use hyphens, not underscores")
                if " " in dir_name:
                    errors.append(f"{dir_name}: Should not contain spaces")

        if errors:
            pytest.fail(
                f"Found {len(errors)} skill directory(ies) with incorrect naming:\n"
                + "\n".join(f"  - {e}" for e in errors)
            )
