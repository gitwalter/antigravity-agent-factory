"""
Value propagation validation tests.

Tests validate that value propagation features are correctly implemented:
- All blueprints have required standard agents and skills
- Pattern files exist and are valid
- Pattern schemas are correct
- Generation script includes standard lists and checks
"""

import json
import sys
from pathlib import Path

import pytest

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


# Expected standard agents that should be in all blueprints
EXPECTED_STANDARD_AGENTS = {
    "knowledge-extender",
    "knowledge-evolution",
    "debug-conductor-project",
}

# Expected standard skills that should be in all blueprints
EXPECTED_STANDARD_SKILLS = {
    "grounding-verification",
    "alignment-check",
    "research-first-project",
    "ci-monitor-project",
    "pipeline-error-fix-project",
}

# Expected pattern files that should exist
EXPECTED_AGENT_PATTERNS = [
    "debug-conductor-project.json",
    "knowledge-extender.json",
    "knowledge-evolution.json",
]

EXPECTED_SKILL_PATTERNS = [
    "grounding-verification.json",
    "alignment-check.json",
    "research-first-project.json",
    "ci-monitor-project.json",
    "pipeline-error-fix-project.json",
]

# Required pattern metadata fields
REQUIRED_PATTERN_METADATA = ["patternId", "patternName", "stackAgnostic"]
REQUIRED_PATTERN_FRONTMATTER = ["name", "description"]
REQUIRED_PATTERN_SECTIONS = True  # Sections should exist (non-empty)


class TestBlueprintCompleteness:
    """Tests for blueprint completeness - all required agents and skills."""

    def test_all_blueprints_have_knowledge_extender_agent(self, blueprints_dir):
        """Test that all 27 blueprints have knowledge-extender agent."""
        missing = []

        for blueprint_dir in blueprints_dir.iterdir():
            if blueprint_dir.is_dir():
                blueprint_file = blueprint_dir / "blueprint.json"
                if blueprint_file.exists():
                    with open(blueprint_file, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    agents = data.get("agents", [])
                    agent_ids = {
                        agent.get("patternId") if isinstance(agent, dict) else agent
                        for agent in agents
                    }

                    if "knowledge-extender" not in agent_ids:
                        missing.append(blueprint_dir.name)

        assert (
            len(missing) == 0
        ), f"Blueprints missing knowledge-extender agent: {', '.join(missing)}"

    def test_all_blueprints_have_knowledge_evolution_agent(self, blueprints_dir):
        """Test that all 27 blueprints have knowledge-evolution agent."""
        missing = []

        for blueprint_dir in blueprints_dir.iterdir():
            if blueprint_dir.is_dir():
                blueprint_file = blueprint_dir / "blueprint.json"
                if blueprint_file.exists():
                    with open(blueprint_file, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    agents = data.get("agents", [])
                    agent_ids = {
                        agent.get("patternId") if isinstance(agent, dict) else agent
                        for agent in agents
                    }

                    if "knowledge-evolution" not in agent_ids:
                        missing.append(blueprint_dir.name)

        assert (
            len(missing) == 0
        ), f"Blueprints missing knowledge-evolution agent: {', '.join(missing)}"

    def test_all_blueprints_have_debug_conductor_project_agent(self, blueprints_dir):
        """Test that all 27 blueprints have debug-conductor-project agent."""
        missing = []

        for blueprint_dir in blueprints_dir.iterdir():
            if blueprint_dir.is_dir():
                blueprint_file = blueprint_dir / "blueprint.json"
                if blueprint_file.exists():
                    with open(blueprint_file, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    agents = data.get("agents", [])
                    agent_ids = {
                        agent.get("patternId") if isinstance(agent, dict) else agent
                        for agent in agents
                    }

                    if "debug-conductor-project" not in agent_ids:
                        missing.append(blueprint_dir.name)

        assert (
            len(missing) == 0
        ), f"Blueprints missing debug-conductor-project agent: {', '.join(missing)}"

    def test_all_blueprints_have_grounding_verification_skill(self, blueprints_dir):
        """Test that all 27 blueprints have grounding-verification skill."""
        missing = []

        for blueprint_dir in blueprints_dir.iterdir():
            if blueprint_dir.is_dir():
                blueprint_file = blueprint_dir / "blueprint.json"
                if blueprint_file.exists():
                    with open(blueprint_file, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    skills = data.get("skills", [])
                    skill_ids = {
                        skill.get("patternId") if isinstance(skill, dict) else skill
                        for skill in skills
                    }

                    if "grounding-verification" not in skill_ids:
                        missing.append(blueprint_dir.name)

        assert (
            len(missing) == 0
        ), f"Blueprints missing grounding-verification skill: {', '.join(missing)}"

    def test_all_blueprints_have_alignment_check_skill(self, blueprints_dir):
        """Test that all 27 blueprints have alignment-check skill."""
        missing = []

        for blueprint_dir in blueprints_dir.iterdir():
            if blueprint_dir.is_dir():
                blueprint_file = blueprint_dir / "blueprint.json"
                if blueprint_file.exists():
                    with open(blueprint_file, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    skills = data.get("skills", [])
                    skill_ids = {
                        skill.get("patternId") if isinstance(skill, dict) else skill
                        for skill in skills
                    }

                    if "alignment-check" not in skill_ids:
                        missing.append(blueprint_dir.name)

        assert (
            len(missing) == 0
        ), f"Blueprints missing alignment-check skill: {', '.join(missing)}"

    def test_all_blueprints_have_research_first_project_skill(self, blueprints_dir):
        """Test that all 27 blueprints have research-first-project skill."""
        missing = []

        for blueprint_dir in blueprints_dir.iterdir():
            if blueprint_dir.is_dir():
                blueprint_file = blueprint_dir / "blueprint.json"
                if blueprint_file.exists():
                    with open(blueprint_file, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    skills = data.get("skills", [])
                    skill_ids = {
                        skill.get("patternId") if isinstance(skill, dict) else skill
                        for skill in skills
                    }

                    if "research-first-project" not in skill_ids:
                        missing.append(blueprint_dir.name)

        assert (
            len(missing) == 0
        ), f"Blueprints missing research-first-project skill: {', '.join(missing)}"

    def test_all_blueprints_have_ci_monitor_project_skill(self, blueprints_dir):
        """Test that all 27 blueprints have ci-monitor-project skill."""
        missing = []

        for blueprint_dir in blueprints_dir.iterdir():
            if blueprint_dir.is_dir():
                blueprint_file = blueprint_dir / "blueprint.json"
                if blueprint_file.exists():
                    with open(blueprint_file, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    skills = data.get("skills", [])
                    skill_ids = {
                        skill.get("patternId") if isinstance(skill, dict) else skill
                        for skill in skills
                    }

                    if "ci-monitor-project" not in skill_ids:
                        missing.append(blueprint_dir.name)

        assert (
            len(missing) == 0
        ), f"Blueprints missing ci-monitor-project skill: {', '.join(missing)}"

    def test_all_blueprints_have_pipeline_error_fix_project_skill(self, blueprints_dir):
        """Test that all 27 blueprints have pipeline-error-fix-project skill."""
        missing = []

        for blueprint_dir in blueprints_dir.iterdir():
            if blueprint_dir.is_dir():
                blueprint_file = blueprint_dir / "blueprint.json"
                if blueprint_file.exists():
                    with open(blueprint_file, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    skills = data.get("skills", [])
                    skill_ids = {
                        skill.get("patternId") if isinstance(skill, dict) else skill
                        for skill in skills
                    }

                    if "pipeline-error-fix-project" not in skill_ids:
                        missing.append(blueprint_dir.name)

        assert (
            len(missing) == 0
        ), f"Blueprints missing pipeline-error-fix-project skill: {', '.join(missing)}"

    def test_all_blueprints_have_pm_integration_section(self, blueprints_dir):
        """Test that all 27 blueprints have pmIntegration section."""
        missing = []

        for blueprint_dir in blueprints_dir.iterdir():
            if blueprint_dir.is_dir():
                blueprint_file = blueprint_dir / "blueprint.json"
                if blueprint_file.exists():
                    with open(blueprint_file, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    if "pmIntegration" not in data:
                        missing.append(blueprint_dir.name)

        assert (
            len(missing) == 0
        ), f"Blueprints missing pmIntegration section: {', '.join(missing)}"

    def test_all_blueprints_have_all_standard_agents(self, blueprints_dir):
        """Test that all blueprints have all standard agents."""
        missing_agents = {}

        for blueprint_dir in blueprints_dir.iterdir():
            if blueprint_dir.is_dir():
                blueprint_file = blueprint_dir / "blueprint.json"
                if blueprint_file.exists():
                    with open(blueprint_file, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    agents = data.get("agents", [])
                    agent_ids = {
                        agent.get("patternId") if isinstance(agent, dict) else agent
                        for agent in agents
                    }

                    missing = EXPECTED_STANDARD_AGENTS - agent_ids
                    if missing:
                        missing_agents[blueprint_dir.name] = missing

        assert len(missing_agents) == 0, (
            "Blueprints missing standard agents:\n"
            + "\n".join(
                f"  {bp}: {', '.join(missing)}"
                for bp, missing in missing_agents.items()
            )
        )

    def test_all_blueprints_have_all_standard_skills(self, blueprints_dir):
        """Test that all blueprints have all standard skills."""
        missing_skills = {}

        for blueprint_dir in blueprints_dir.iterdir():
            if blueprint_dir.is_dir():
                blueprint_file = blueprint_dir / "blueprint.json"
                if blueprint_file.exists():
                    with open(blueprint_file, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    skills = data.get("skills", [])
                    skill_ids = {
                        skill.get("patternId") if isinstance(skill, dict) else skill
                        for skill in skills
                    }

                    missing = EXPECTED_STANDARD_SKILLS - skill_ids
                    if missing:
                        missing_skills[blueprint_dir.name] = missing

        assert len(missing_skills) == 0, (
            "Blueprints missing standard skills:\n"
            + "\n".join(
                f"  {bp}: {', '.join(missing)}"
                for bp, missing in missing_skills.items()
            )
        )


class TestPatternFileExistence:
    """Tests for pattern file existence and validity."""

    def test_debug_conductor_project_pattern_exists(self, patterns_dir):
        """Test that patterns/agents/debug-conductor-project.json exists and is valid JSON."""
        pattern_file = patterns_dir / "agents" / "debug-conductor-project.json"

        assert pattern_file.exists(), f"Pattern file does not exist: {pattern_file}"

        with open(pattern_file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                assert isinstance(
                    data, dict
                ), f"Pattern file is not a valid JSON object: {pattern_file}"
            except json.JSONDecodeError as e:
                pytest.fail(
                    f"Pattern file is not valid JSON: {pattern_file}\nError: {e}"
                )

    def test_knowledge_extender_pattern_exists(self, patterns_dir):
        """Test that patterns/agents/knowledge-extender.json exists and is valid JSON."""
        pattern_file = patterns_dir / "agents" / "knowledge-extender.json"

        assert pattern_file.exists(), f"Pattern file does not exist: {pattern_file}"

        with open(pattern_file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                assert isinstance(
                    data, dict
                ), f"Pattern file is not a valid JSON object: {pattern_file}"
            except json.JSONDecodeError as e:
                pytest.fail(
                    f"Pattern file is not valid JSON: {pattern_file}\nError: {e}"
                )

    def test_knowledge_evolution_pattern_exists(self, patterns_dir):
        """Test that patterns/agents/knowledge-evolution.json exists and is valid JSON."""
        pattern_file = patterns_dir / "agents" / "knowledge-evolution.json"

        assert pattern_file.exists(), f"Pattern file does not exist: {pattern_file}"

        with open(pattern_file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                assert isinstance(
                    data, dict
                ), f"Pattern file is not a valid JSON object: {pattern_file}"
            except json.JSONDecodeError as e:
                pytest.fail(
                    f"Pattern file is not valid JSON: {pattern_file}\nError: {e}"
                )

    def test_grounding_verification_pattern_exists(self, patterns_dir):
        """Test that patterns/skills/grounding-verification.json exists and is valid JSON."""
        pattern_file = patterns_dir / "skills" / "grounding-verification.json"

        assert pattern_file.exists(), f"Pattern file does not exist: {pattern_file}"

        with open(pattern_file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                assert isinstance(
                    data, dict
                ), f"Pattern file is not a valid JSON object: {pattern_file}"
            except json.JSONDecodeError as e:
                pytest.fail(
                    f"Pattern file is not valid JSON: {pattern_file}\nError: {e}"
                )

    def test_alignment_check_pattern_exists(self, patterns_dir):
        """Test that patterns/skills/alignment-check.json exists and is valid JSON."""
        pattern_file = patterns_dir / "skills" / "alignment-check.json"

        assert pattern_file.exists(), f"Pattern file does not exist: {pattern_file}"

        with open(pattern_file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                assert isinstance(
                    data, dict
                ), f"Pattern file is not a valid JSON object: {pattern_file}"
            except json.JSONDecodeError as e:
                pytest.fail(
                    f"Pattern file is not valid JSON: {pattern_file}\nError: {e}"
                )

    def test_research_first_project_pattern_exists(self, patterns_dir):
        """Test that patterns/skills/research-first-project.json exists and is valid JSON."""
        pattern_file = patterns_dir / "skills" / "research-first-project.json"

        assert pattern_file.exists(), f"Pattern file does not exist: {pattern_file}"

        with open(pattern_file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                assert isinstance(
                    data, dict
                ), f"Pattern file is not a valid JSON object: {pattern_file}"
            except json.JSONDecodeError as e:
                pytest.fail(
                    f"Pattern file is not valid JSON: {pattern_file}\nError: {e}"
                )

    def test_ci_monitor_project_pattern_exists(self, patterns_dir):
        """Test that patterns/skills/ci-monitor-project.json exists and is valid JSON."""
        pattern_file = patterns_dir / "skills" / "ci-monitor-project.json"

        assert pattern_file.exists(), f"Pattern file does not exist: {pattern_file}"

        with open(pattern_file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                assert isinstance(
                    data, dict
                ), f"Pattern file is not a valid JSON object: {pattern_file}"
            except json.JSONDecodeError as e:
                pytest.fail(
                    f"Pattern file is not valid JSON: {pattern_file}\nError: {e}"
                )

    def test_pipeline_error_fix_project_pattern_exists(self, patterns_dir):
        """Test that patterns/skills/pipeline-error-fix-project.json exists and is valid JSON."""
        pattern_file = patterns_dir / "skills" / "pipeline-error-fix-project.json"

        assert pattern_file.exists(), f"Pattern file does not exist: {pattern_file}"

        with open(pattern_file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                assert isinstance(
                    data, dict
                ), f"Pattern file is not a valid JSON object: {pattern_file}"
            except json.JSONDecodeError as e:
                pytest.fail(
                    f"Pattern file is not valid JSON: {pattern_file}\nError: {e}"
                )

    def test_all_agent_patterns_exist(self, patterns_dir):
        """Test that all expected agent pattern files exist and are valid JSON."""
        agents_dir = patterns_dir / "agents"
        missing = []
        invalid = []

        for pattern_file in EXPECTED_AGENT_PATTERNS:
            pattern_path = agents_dir / pattern_file
            if not pattern_path.exists():
                missing.append(pattern_file)
            else:
                try:
                    with open(pattern_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if not isinstance(data, dict):
                            invalid.append(pattern_file)
                except json.JSONDecodeError:
                    invalid.append(pattern_file)

        assert len(missing) == 0, f"Missing agent pattern files: {', '.join(missing)}"
        assert len(invalid) == 0, f"Invalid agent pattern files: {', '.join(invalid)}"

    def test_all_skill_patterns_exist(self, patterns_dir):
        """Test that all expected skill pattern files exist and are valid JSON."""
        skills_dir = patterns_dir / "skills"
        missing = []
        invalid = []

        for pattern_file in EXPECTED_SKILL_PATTERNS:
            pattern_path = skills_dir / pattern_file
            if not pattern_path.exists():
                missing.append(pattern_file)
            else:
                try:
                    with open(pattern_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if not isinstance(data, dict):
                            invalid.append(pattern_file)
                except json.JSONDecodeError:
                    invalid.append(pattern_file)

        assert len(missing) == 0, f"Missing skill pattern files: {', '.join(missing)}"
        assert len(invalid) == 0, f"Invalid skill pattern files: {', '.join(invalid)}"


class TestPatternSchemaValidation:
    """Tests for pattern schema validation."""

    def test_patterns_have_required_metadata(self, patterns_dir):
        """Test that each pattern has required metadata fields."""
        errors = []

        # Check agent patterns
        agents_dir = patterns_dir / "agents"
        for pattern_file in EXPECTED_AGENT_PATTERNS:
            pattern_path = agents_dir / pattern_file
            if pattern_path.exists():
                with open(pattern_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                metadata = data.get("metadata", {})
                for field in REQUIRED_PATTERN_METADATA:
                    if field not in metadata:
                        errors.append(f"{pattern_file}: missing metadata.{field}")

        # Check skill patterns
        skills_dir = patterns_dir / "skills"
        for pattern_file in EXPECTED_SKILL_PATTERNS:
            pattern_path = skills_dir / pattern_file
            if pattern_path.exists():
                with open(pattern_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                metadata = data.get("metadata", {})
                for field in REQUIRED_PATTERN_METADATA:
                    if field not in metadata:
                        errors.append(f"{pattern_file}: missing metadata.{field}")

        assert len(errors) == 0, "Pattern schema validation errors:\n" + "\n".join(
            f"  - {e}" for e in errors
        )

    def test_patterns_have_frontmatter_with_name_and_description(self, patterns_dir):
        """Test that each pattern has frontmatter with name and description."""
        errors = []

        # Check agent patterns
        agents_dir = patterns_dir / "agents"
        for pattern_file in EXPECTED_AGENT_PATTERNS:
            pattern_path = agents_dir / pattern_file
            if pattern_path.exists():
                with open(pattern_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                frontmatter = data.get("frontmatter", {})
                for field in REQUIRED_PATTERN_FRONTMATTER:
                    if field not in frontmatter:
                        errors.append(f"{pattern_file}: missing frontmatter.{field}")

        # Check skill patterns
        skills_dir = patterns_dir / "skills"
        for pattern_file in EXPECTED_SKILL_PATTERNS:
            pattern_path = skills_dir / pattern_file
            if pattern_path.exists():
                with open(pattern_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                frontmatter = data.get("frontmatter", {})
                for field in REQUIRED_PATTERN_FRONTMATTER:
                    if field not in frontmatter:
                        errors.append(f"{pattern_file}: missing frontmatter.{field}")

        assert len(errors) == 0, "Pattern frontmatter validation errors:\n" + "\n".join(
            f"  - {e}" for e in errors
        )

    def test_patterns_have_sections(self, patterns_dir):
        """Test that each pattern has sections."""
        errors = []

        # Check agent patterns
        agents_dir = patterns_dir / "agents"
        for pattern_file in EXPECTED_AGENT_PATTERNS:
            pattern_path = agents_dir / pattern_file
            if pattern_path.exists():
                with open(pattern_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                sections = data.get("sections")
                if not sections or not isinstance(sections, dict) or len(sections) == 0:
                    errors.append(f"{pattern_file}: missing or empty sections")

        # Check skill patterns
        skills_dir = patterns_dir / "skills"
        for pattern_file in EXPECTED_SKILL_PATTERNS:
            pattern_path = skills_dir / pattern_file
            if pattern_path.exists():
                with open(pattern_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                sections = data.get("sections")
                if not sections or not isinstance(sections, dict) or len(sections) == 0:
                    errors.append(f"{pattern_file}: missing or empty sections")

        assert len(errors) == 0, "Pattern sections validation errors:\n" + "\n".join(
            f"  - {e}" for e in errors
        )


class TestGenerationScriptValidation:
    """Tests for generation script validation."""

    def test_generate_project_includes_standard_agents_list(self, factory_root):
        """Test that scripts/core/generate_project.py includes standard_agents list."""
        script_path = factory_root / "scripts" / "core" / "generate_project.py"

        assert script_path.exists(), f"Generation script does not exist: {script_path}"

        with open(script_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check for standard_agents list definition
        assert (
            "standard_agents" in content
        ), "generate_project.py does not include standard_agents list"

        # Check that it includes debug-conductor-project
        assert (
            "debug-conductor-project" in content
            or "'debug-conductor-project'" in content
            or '"debug-conductor-project"' in content
        ), "standard_agents list does not include debug-conductor-project"

    def test_generate_project_includes_standard_skills_list(self, factory_root):
        """Test that scripts/core/generate_project.py includes standard_skills list."""
        script_path = factory_root / "scripts" / "core" / "generate_project.py"

        assert script_path.exists(), f"Generation script does not exist: {script_path}"

        with open(script_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check for standard_skills list definition
        assert (
            "standard_skills" in content
        ), "generate_project.py does not include standard_skills list"

        # Check that it includes all expected standard skills
        expected_in_content = [
            "grounding-verification",
            "alignment-check",
            "research-first-project",
            "ci-monitor-project",
            "pipeline-error-fix-project",
        ]

        missing = [skill for skill in expected_in_content if skill not in content]
        assert len(missing) == 0, f"standard_skills list missing: {', '.join(missing)}"

    def test_generate_project_checks_pm_integration_enabled(self, factory_root):
        """Test that scripts/core/generate_project.py checks pmIntegration.enabled."""
        script_path = factory_root / "scripts" / "core" / "generate_project.py"

        assert script_path.exists(), f"Generation script does not exist: {script_path}"

        with open(script_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check for pmIntegration check
        assert (
            "pmIntegration" in content
        ), "generate_project.py does not check pmIntegration"

        # Check for enabled check pattern
        assert "pmIntegration" in content and (
            ".get('enabled'" in content
            or "['enabled']" in content
            or ".get('pmIntegration'" in content
        ), "generate_project.py does not check pmIntegration.enabled"

    def test_generate_project_adds_standard_agents(self, factory_root):
        """Test that generate_project.py adds standard agents to agents list."""
        script_path = factory_root / "scripts" / "core" / "generate_project.py"

        with open(script_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Find the section where standard_agents is used
        found_standard_agents = False
        found_append = False

        for i, line in enumerate(lines):
            if "standard_agents" in line and "=" in line:
                found_standard_agents = True
            if found_standard_agents and (
                "agents_to_generate" in line or "append" in line.lower()
            ):
                found_append = True
                break

        assert (
            found_standard_agents
        ), "generate_project.py does not define standard_agents"
        assert (
            found_append
        ), "generate_project.py does not add standard_agents to agents list"

    def test_generate_project_adds_standard_skills(self, factory_root):
        """Test that generate_project.py adds standard skills to skills list."""
        script_path = factory_root / "scripts" / "core" / "generate_project.py"

        with open(script_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Find the section where standard_skills is used
        found_standard_skills = False
        found_append = False

        for i, line in enumerate(lines):
            if "standard_skills" in line and "=" in line:
                found_standard_skills = True
            if found_standard_skills and (
                "skills_to_generate" in line or "append" in line.lower()
            ):
                found_append = True
                break

        assert (
            found_standard_skills
        ), "generate_project.py does not define standard_skills"
        assert (
            found_append
        ), "generate_project.py does not add standard_skills to skills list"
