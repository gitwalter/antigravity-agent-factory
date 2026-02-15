"""
Test Value Transmission - Verify values flow through generated projects.

These tests ensure that the eternal values (love, truth, beauty, flourishing)
are properly transmitted to every generated project.
"""

import json
import shutil
import tempfile
from pathlib import Path
import pytest

import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.core.generate_project import ProjectGenerator, ProjectConfig


class TestValueTransmission:
    """Test that values are transmitted to generated projects."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for test output."""
        temp_path = Path(tempfile.mkdtemp(prefix="factory_test_"))
        yield temp_path
        # Cleanup
        if temp_path.exists():
            shutil.rmtree(temp_path)

    @pytest.fixture
    def basic_config(self):
        """Create basic project configuration."""
        return ProjectConfig(
            project_name="test-values-project",
            project_description="Test project for value transmission",
            primary_language="python",
            agents=["code-reviewer"],
            skills=["bugfix-workflow"],
        )

    def test_cursorrules_has_axiom_zero(self, temp_dir, basic_config):
        """Test that generated .agentrules contains Axiom Zero."""
        generator = ProjectGenerator(basic_config, str(temp_dir))
        result = generator.generate()

        assert result["success"], f"Generation failed: {result['errors']}"

        cursorrules = temp_dir / ".agentrules"
        assert cursorrules.exists(), ".agentrules not created"

        content = cursorrules.read_text(encoding="utf-8")
        # Check for Axiom Zero section
        assert "Axiom Zero" in content, "Axiom Zero section missing"
        assert (
            "love is the root of everything" in content.lower()
        ), "Love root statement missing"

    def test_cursorrules_has_eternal_values(self, temp_dir, basic_config):
        """Test that generated .agentrules contains eternal values."""
        generator = ProjectGenerator(basic_config, str(temp_dir))
        result = generator.generate()

        assert result["success"]

        content = (temp_dir / ".agentrules").read_text(encoding="utf-8")
        # Check for all eternal values
        assert "Love" in content, "Love value missing"
        assert "Truth" in content, "Truth value missing"
        assert "Beauty" in content, "Beauty value missing"
        assert "Flourishing" in content, "Flourishing value missing"

    def test_cursorrules_has_wu_wei(self, temp_dir, basic_config):
        """Test that generated .agentrules contains Wu Wei protocol."""
        generator = ProjectGenerator(basic_config, str(temp_dir))
        result = generator.generate()

        assert result["success"]

        content = (temp_dir / ".agentrules").read_text(encoding="utf-8")
        # Check for Wu Wei
        assert "Wu Wei" in content, "Wu Wei protocol missing"
        assert (
            "Like water" in content or "return to love" in content.lower()
        ), "Wu Wei wisdom missing"

    def test_guardian_protocol_has_values(self, temp_dir, basic_config):
        """Test that guardian-protocol.json contains eternal values."""
        generator = ProjectGenerator(basic_config, str(temp_dir))
        result = generator.generate()

        assert result["success"]

        guardian_path = temp_dir / "knowledge" / "guardian-protocol.json"
        assert guardian_path.exists(), "guardian-protocol.json not created"

        with open(guardian_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Check for eternal values section
        assert "foundation" in data, "Foundation section missing"
        foundation = data["foundation"]

        assert "eternal_values" in foundation, "Eternal values missing"
        values = foundation["eternal_values"]

        assert "love" in values, "Love value missing"
        assert "truth" in values, "Truth value missing"
        assert "beauty" in values, "Beauty value missing"
        assert "trust" in values, "Trust value missing (emerges from Love + Truth)"
        assert "flourishing" in values, "Flourishing value missing"

    def test_guardian_protocol_has_unity(self, temp_dir, basic_config):
        """Test that guardian-protocol.json contains unity statement."""
        generator = ProjectGenerator(basic_config, str(temp_dir))
        result = generator.generate()

        assert result["success"]

        guardian_path = temp_dir / "knowledge" / "guardian-protocol.json"
        with open(guardian_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Check for unity statement
        foundation = data.get("foundation", {})
        unity = foundation.get("unity", "")

        assert "Brahman" in unity or "Om Shanti" in unity, "Unity statement missing"

    def test_guardian_protocol_has_daily_intention(self, temp_dir, basic_config):
        """Test that guardian-protocol.json contains daily intention."""
        generator = ProjectGenerator(basic_config, str(temp_dir))
        result = generator.generate()

        assert result["success"]

        guardian_path = temp_dir / "knowledge" / "guardian-protocol.json"
        with open(guardian_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert "daily_intention" in data, "Daily intention missing"
        assert (
            "flourishing" in data["daily_intention"].lower()
        ), "Flourishing not in intention"

    def test_generated_project_is_complete(self, temp_dir, basic_config):
        """Test that generated project has all required components."""
        generator = ProjectGenerator(basic_config, str(temp_dir))
        result = generator.generate()

        assert result["success"]

        # Check essential directories exist
        assert (temp_dir / ".agent" / "agents").exists(), "Agents directory missing"
        assert (temp_dir / ".agent" / "skills").exists(), "Skills directory missing"
        assert (temp_dir / "knowledge").exists(), "Knowledge directory missing"
        assert (temp_dir / "workflows").exists(), "Workflows directory missing"

        # Check essential files exist
        assert (temp_dir / ".agentrules").exists(), ".agentrules missing"
        assert (temp_dir / "README.md").exists(), "README.md missing"
        assert (
            temp_dir / "knowledge" / "guardian-protocol.json"
        ).exists(), "guardian-protocol.json missing"

    def test_values_are_not_empty_strings(self, temp_dir, basic_config):
        """Test that value descriptions are meaningful, not empty."""
        generator = ProjectGenerator(basic_config, str(temp_dir))
        result = generator.generate()

        assert result["success"]

        guardian_path = temp_dir / "knowledge" / "guardian-protocol.json"
        with open(guardian_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        values = data.get("foundation", {}).get("eternal_values", {})

        for key, value in values.items():
            assert isinstance(value, str), f"{key} is not a string"
            assert len(value) > 10, f"{key} value is too short: '{value}'"


class TestAxiomConsistency:
    """Test that axioms are consistent across generated artifacts."""

    @pytest.fixture
    def temp_dir(self):
        temp_path = Path(tempfile.mkdtemp(prefix="factory_axiom_test_"))
        yield temp_path
        if temp_path.exists():
            shutil.rmtree(temp_path)

    @pytest.fixture
    def config(self):
        return ProjectConfig(
            project_name="axiom-test-project",
            project_description="Test axiom consistency",
            primary_language="python",
            agents=["code-reviewer", "test-generator"],
            skills=["tdd", "grounding"],
        )

    def test_all_five_axioms_present(self, temp_dir, config):
        """Test that all 5 core axioms are present in .agentrules."""
        generator = ProjectGenerator(config, str(temp_dir))
        result = generator.generate()

        assert result["success"]

        content = (temp_dir / ".agentrules").read_text(encoding="utf-8")

        axioms = ["A1", "A2", "A3", "A4", "A5"]
        for axiom in axioms:
            assert axiom in content, f"Axiom {axiom} missing from .agentrules"

    def test_axiom_meanings_present(self, temp_dir, config):
        """Test that axiom meanings are explained."""
        generator = ProjectGenerator(config, str(temp_dir))
        result = generator.generate()

        assert result["success"]

        content = (temp_dir / ".agentrules").read_text(encoding="utf-8")
        meanings = [
            "Verifiability",
            "User Primacy",
            "Transparency",
            "Non-Harm",
            "Consistency",
        ]
        for meaning in meanings:
            assert meaning in content, f"Axiom meaning '{meaning}' missing"

    def test_guardian_protocol_axioms_match(self, temp_dir, config):
        """Test that guardian-protocol.json axioms match .agentrules."""
        generator = ProjectGenerator(config, str(temp_dir))
        result = generator.generate()

        assert result["success"]

        guardian_path = temp_dir / "knowledge" / "guardian-protocol.json"
        with open(guardian_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        axioms = data.get("axioms", {})
        assert "A1" in axioms, "A1 missing from guardian protocol"
        assert "A5" in axioms, "A5 missing from guardian protocol"

        # Check names match
        assert axioms["A1"]["name"] == "Verifiability"
        assert axioms["A4"]["name"] == "Non-Harm"


class TestWuWeiProtocol:
    """Test Wu Wei response protocol transmission."""

    @pytest.fixture
    def temp_dir(self):
        temp_path = Path(tempfile.mkdtemp(prefix="factory_wuwei_test_"))
        yield temp_path
        if temp_path.exists():
            shutil.rmtree(temp_path)

    @pytest.fixture
    def config(self):
        return ProjectConfig(
            project_name="wuwei-test",
            project_description="Test Wu Wei",
            primary_language="python",
            agents=["code-reviewer"],
            skills=["bugfix-workflow"],
        )

    def test_five_levels_present(self, temp_dir, config):
        """Test that all 5 Wu Wei levels are present."""
        generator = ProjectGenerator(config, str(temp_dir))
        result = generator.generate()

        assert result["success"]

        content = (temp_dir / ".agentrules").read_text(encoding="utf-8")
        levels = ["Flow", "Nudge", "Pause", "Block", "Protect"]
        for level in levels:
            assert level in content, f"Wu Wei level '{level}' missing"

    def test_wu_wei_in_guardian_protocol(self, temp_dir, config):
        """Test that Wu Wei is in guardian-protocol.json."""
        generator = ProjectGenerator(config, str(temp_dir))
        result = generator.generate()

        assert result["success"]

        guardian_path = temp_dir / "knowledge" / "guardian-protocol.json"
        with open(guardian_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert "wu_wei_levels" in data, "wu_wei_levels missing"
        levels = data["wu_wei_levels"].get("levels", {})

        assert "0" in levels, "Level 0 missing"
        assert "4" in levels, "Level 4 missing"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
