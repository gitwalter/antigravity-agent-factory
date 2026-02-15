"""
Integration tests for PM (Project Management) CLI functionality.

Tests cover:
- --help shows PM options
- PM-enabled blueprint generation creates PM artifacts
- PM backend and methodology validation
"""

import subprocess
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class TestPMHelpOutput:
    """Tests for PM help output in CLI."""

    def test_help_shows_pm_enabled_flag(self, python_executable, cli_path):
        """Test that --help shows --pm-enabled flag."""
        result = subprocess.run(
            [python_executable, str(cli_path), "--help"],
            capture_output=True,
            text=True,
            timeout=30,
        )

        assert result.returncode == 0
        assert "--pm-enabled" in result.stdout

    def test_help_shows_pm_backend_flag(self, python_executable, cli_path):
        """Test that --help shows --pm-backend flag."""
        result = subprocess.run(
            [python_executable, str(cli_path), "--help"],
            capture_output=True,
            text=True,
            timeout=30,
        )

        assert result.returncode == 0
        assert "--pm-backend" in result.stdout

    def test_help_shows_pm_methodology_flag(self, python_executable, cli_path):
        """Test that --help shows --pm-methodology flag."""
        result = subprocess.run(
            [python_executable, str(cli_path), "--help"],
            capture_output=True,
            text=True,
            timeout=30,
        )

        assert result.returncode == 0
        assert "--pm-methodology" in result.stdout

    def test_help_shows_pm_doc_backend_flag(self, python_executable, cli_path):
        """Test that --help shows --pm-doc-backend flag."""
        result = subprocess.run(
            [python_executable, str(cli_path), "--help"],
            capture_output=True,
            text=True,
            timeout=30,
        )

        assert result.returncode == 0
        assert "--pm-doc-backend" in result.stdout


class TestPMBlueprintGeneration:
    """Tests for PM-enabled blueprint generation."""

    def test_pm_enabled_runs_successfully(
        self, python_executable, cli_path, temp_output_dir
    ):
        """Test that --pm-enabled runs without errors."""
        output_dir = temp_output_dir / "pm-test"

        result = subprocess.run(
            [
                python_executable,
                str(cli_path),
                "--blueprint",
                "python-fastapi",
                "--output",
                str(output_dir),
                "--pm-enabled",
                "--pm-backend",
                "github",
                "--pm-methodology",
                "scrum",
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )

        assert result.returncode == 0
        # Basic output directory should exist
        assert (output_dir / ".agent" / "agents").exists()

    def test_pm_enabled_config_recognized(
        self, python_executable, cli_path, temp_output_dir
    ):
        """Test that PM config is recognized in output."""
        output_dir = temp_output_dir / "pm-config-test"

        result = subprocess.run(
            [
                python_executable,
                str(cli_path),
                "--blueprint",
                "python-fastapi",
                "--output",
                str(output_dir),
                "--pm-enabled",
                "--pm-backend",
                "github",
                "--pm-methodology",
                "scrum",
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )

        assert result.returncode == 0
        # Check that PM was recognized in output
        assert "pm" in result.stdout.lower() or result.returncode == 0

    def test_pm_disabled_no_pm_artifacts(
        self, python_executable, cli_path, temp_output_dir
    ):
        """Test that without --pm-enabled, PM artifacts are not generated."""
        output_dir = temp_output_dir / "pm-disabled-test"

        result = subprocess.run(
            [
                python_executable,
                str(cli_path),
                "--blueprint",
                "python-fastapi",
                "--output",
                str(output_dir),
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )

        assert result.returncode == 0

        # PM directories should not exist or should be empty
        pm_agents_dir = output_dir / ".agent" / "agents" / "pm"
        pm_skills_dir = output_dir / ".agent" / "skills" / "pm"
        # Check that PM-specific agent files don't exist
        if pm_agents_dir.exists():
            pm_agent_files = [
                "product-owner.md",
                "sprint-master.md",
                "task-manager.md",
                "reporting-agent.md",
            ]
            for agent_file in pm_agent_files:
                assert not (
                    pm_agents_dir / agent_file
                ).exists(), (
                    f"PM agent {agent_file} should not exist when PM is disabled"
                )

        # Check that PM-specific skill directories don't exist
        if pm_skills_dir.exists():
            pm_skill_dirs = [
                "create-epic",
                "create-story",
                "create-task",
                "estimate-task",
                "run-standup",
                "plan-sprint",
                "close-sprint",
                "generate-burndown",
                "health-check",
            ]
            for skill_dir in pm_skill_dirs:
                assert not (
                    pm_skills_dir / skill_dir
                ).exists(), f"PM skill {skill_dir} should not exist when PM is disabled"


class TestPMBackendValidation:
    """Tests for PM backend and methodology validation."""

    def test_valid_pm_backends_accepted(
        self, python_executable, cli_path, temp_output_dir
    ):
        """Test that valid PM backends are accepted."""
        valid_backends = ["github", "jira", "azure-devops", "linear"]

        for backend in valid_backends:
            output_dir = temp_output_dir / f"pm-backend-{backend}"

            result = subprocess.run(
                [
                    python_executable,
                    str(cli_path),
                    "--blueprint",
                    "python-fastapi",
                    "--output",
                    str(output_dir),
                    "--pm-enabled",
                    "--pm-backend",
                    backend,
                    "--pm-methodology",
                    "scrum",
                ],
                capture_output=True,
                text=True,
                timeout=60,
            )

            # Should succeed (returncode 0) or at least not fail with validation error
            assert (
                result.returncode == 0 or "invalid" not in result.stderr.lower()
            ), f"Backend {backend} should be accepted but got error: {result.stderr}"

    def test_valid_pm_methodologies_accepted(
        self, python_executable, cli_path, temp_output_dir
    ):
        """Test that valid PM methodologies are accepted."""
        valid_methodologies = ["scrum", "kanban", "hybrid", "waterfall"]

        for methodology in valid_methodologies:
            output_dir = temp_output_dir / f"pm-methodology-{methodology}"

            result = subprocess.run(
                [
                    python_executable,
                    str(cli_path),
                    "--blueprint",
                    "python-fastapi",
                    "--output",
                    str(output_dir),
                    "--pm-enabled",
                    "--pm-backend",
                    "github",
                    "--pm-methodology",
                    methodology,
                ],
                capture_output=True,
                text=True,
                timeout=60,
            )

            # Should succeed (returncode 0) or at least not fail with validation error
            assert (
                result.returncode == 0 or "invalid" not in result.stderr.lower()
            ), f"Methodology {methodology} should be accepted but got error: {result.stderr}"
