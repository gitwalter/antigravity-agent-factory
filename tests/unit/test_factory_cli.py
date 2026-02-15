"""
Unit tests for cli/factory_cli.py

Tests the CLI interface for the Antigravity Agent Factory.
"""

import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from cli.factory_cli import (
    get_factory_root,
    display_welcome,
    display_tour,
    display_error_with_help,
    run_quickstart,
    list_blueprints,
    list_patterns,
    interactive_mode,
    generate_from_blueprint,
    generate_from_config_file,
    analyze_repository,
    onboard_repository,
    rollback_session,
    _create_default_config,
    _interactive_conflict_resolver,
    main,
)


class TestGetFactoryRoot:
    """Tests for get_factory_root function."""

    def test_returns_path(self):
        """Test that get_factory_root returns a Path."""
        result = get_factory_root()
        assert isinstance(result, Path)

    def test_path_exists(self):
        """Test that returned path exists."""
        result = get_factory_root()
        assert result.exists()

    def test_contains_blueprints(self):
        """Test that factory root contains blueprints directory."""
        result = get_factory_root()
        assert (result / ".agent" / "blueprints").exists()


class TestDisplayWelcome:
    """Tests for display_welcome function."""

    def test_prints_welcome_message(self, capsys):
        """Test that welcome message is printed."""
        display_welcome()
        captured = capsys.readouterr()

        assert "Welcome" in captured.out
        assert "Antigravity Agent Factory" in captured.out


class TestDisplayTour:
    """Tests for display_tour function."""

    def test_prints_tour_info(self, capsys):
        """Test that tour information is printed."""
        display_tour("/test/output", 42)
        captured = capsys.readouterr()

        assert "Congratulations" in captured.out
        assert "42 files" in captured.out
        assert "/test/output" in captured.out
        assert ".agentrules" in captured.out


class TestDisplayErrorWithHelp:
    """Tests for display_error_with_help function."""

    def test_prints_error_and_suggestion(self, capsys):
        """Test that error and suggestion are printed."""
        display_error_with_help("Something broke", "Try this fix")
        captured = capsys.readouterr()

        assert "Something broke" in captured.out
        assert "Try this fix" in captured.out
        assert "don't worry" in captured.out


class TestListBlueprints:
    """Tests for list_blueprints function."""

    def test_lists_available_blueprints(self, capsys):
        """Test that blueprints are listed."""
        list_blueprints()
        captured = capsys.readouterr()

        assert "Available Blueprints" in captured.out
        assert "python-fastapi" in captured.out or "Blueprint" in captured.out

    def test_shows_blueprint_details(self, capsys):
        """Test that blueprint details are shown."""
        list_blueprints()
        captured = capsys.readouterr()

        assert "Name:" in captured.out or "Description:" in captured.out


class TestListPatterns:
    """Tests for list_patterns function."""

    def test_lists_available_patterns(self, capsys):
        """Test that patterns are listed."""
        list_patterns()
        captured = capsys.readouterr()

        assert "Available Patterns" in captured.out

    def test_shows_pattern_categories(self, capsys):
        """Test that pattern categories are shown."""
        list_patterns()
        captured = capsys.readouterr()

        assert "AGENTS:" in captured.out or "SKILLS:" in captured.out


class TestRunQuickstart:
    """Tests for run_quickstart function."""

    def test_quickstart_with_default_output(self, capsys):
        """Test quickstart with default output directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "quickstart-demo"

            with patch("cli.factory_cli.ProjectGenerator") as mock_gen:
                mock_instance = MagicMock()
                mock_instance.generate.return_value = {
                    "success": True,
                    "files_created": ["file1.py", "file2.py"],
                }
                mock_gen.return_value = mock_instance

                run_quickstart(str(output_dir))

                captured = capsys.readouterr()
                assert "Welcome" in captured.out

    def test_quickstart_with_custom_blueprint(self, capsys):
        """Test quickstart with custom blueprint."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("cli.factory_cli.ProjectGenerator") as mock_gen:
                mock_instance = MagicMock()
                mock_instance.generate.return_value = {
                    "success": True,
                    "files_created": [],
                }
                mock_gen.return_value = mock_instance

                run_quickstart(tmpdir, blueprint_id="typescript-react")

                captured = capsys.readouterr()
                assert "typescript-react" in captured.out

    def test_quickstart_handles_generation_failure(self, capsys):
        """Test quickstart handles generation failure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("cli.factory_cli.ProjectGenerator") as mock_gen:
                mock_instance = MagicMock()
                mock_instance.generate.return_value = {
                    "success": False,
                    "errors": ["Test error"],
                }
                mock_gen.return_value = mock_instance

                with pytest.raises(SystemExit) as exc_info:
                    run_quickstart(tmpdir)

                assert exc_info.value.code == 1

    def test_quickstart_handles_exception(self, capsys):
        """Test quickstart handles exceptions."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("cli.factory_cli.ProjectGenerator") as mock_gen:
                mock_gen.side_effect = Exception("Test exception")

                with pytest.raises(SystemExit) as exc_info:
                    run_quickstart(tmpdir)

                assert exc_info.value.code == 1


class TestInteractiveMode:
    """Tests for interactive_mode function."""

    def test_interactive_mode_basic_flow(self, capsys):
        """Test basic interactive mode flow."""
        inputs = [
            "test-project",  # Project name
            "A test project",  # Description
            "web",  # Domain
            "",  # Team context
            "python",  # Language
            "fastapi",  # Frameworks
            "manual",  # Triggers
            "code-reviewer",  # Agents
            "tdd,bugfix-workflow",  # Skills
            "n",  # PM enabled
            "1",  # MCP starter pack
            "n",  # Custom servers
            "y",  # Confirm
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("builtins.input", side_effect=inputs):
                with patch("cli.factory_cli.ProjectGenerator") as mock_gen:
                    mock_instance = MagicMock()
                    mock_instance.generate.return_value = {
                        "success": True,
                        "files_created": ["file1"],
                        "target_dir": tmpdir,
                    }
                    mock_gen.return_value = mock_instance

                    interactive_mode(tmpdir)

                    captured = capsys.readouterr()
                    assert "Project Context" in captured.out

    def test_interactive_mode_cancel(self, capsys):
        """Test cancelling interactive mode."""
        inputs = [
            "test-project",
            "Description",
            "web",
            "",
            "python",
            "",
            "",
            "",
            "",
            "n",
            "1",
            "n",
            "n",  # Don't confirm
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("builtins.input", side_effect=inputs):
                interactive_mode(tmpdir)

                captured = capsys.readouterr()
                assert "Cancelled" in captured.out

    def test_interactive_mode_with_pm_enabled(self, capsys):
        """Test interactive mode with PM system enabled."""
        inputs = [
            "test-project",
            "Description",
            "web",
            "",
            "python",
            "fastapi",
            "jira",
            "code-reviewer",
            "tdd",
            "y",  # Enable PM
            "github",  # PM backend
            "github-wiki",  # Doc backend
            "scrum",  # Methodology
            "1",  # MCP pack
            "n",  # No custom
            "y",  # Confirm
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("builtins.input", side_effect=inputs):
                with patch("cli.factory_cli.ProjectGenerator") as mock_gen:
                    mock_instance = MagicMock()
                    mock_instance.generate.return_value = {
                        "success": True,
                        "files_created": [],
                        "target_dir": tmpdir,
                    }
                    mock_gen.return_value = mock_instance

                    interactive_mode(tmpdir)


class TestGenerateFromBlueprint:
    """Tests for generate_from_blueprint function."""

    def test_generate_from_valid_blueprint(self, capsys):
        """Test generating from a valid blueprint."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("cli.factory_cli.ProjectGenerator") as mock_gen:
                mock_instance = MagicMock()
                mock_instance.generate.return_value = {
                    "success": True,
                    "files_created": ["file1", "file2"],
                    "target_dir": tmpdir,
                }
                mock_gen.return_value = mock_instance

                generate_from_blueprint("python-fastapi", tmpdir)

                captured = capsys.readouterr()
                assert "SUCCESS" in captured.out

    def test_generate_from_invalid_blueprint(self, capsys):
        """Test generating from non-existent blueprint."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(SystemExit) as exc_info:
                generate_from_blueprint("nonexistent-blueprint", tmpdir)

            assert exc_info.value.code == 1
            captured = capsys.readouterr()
            assert "ERROR" in captured.out

    def test_generate_with_project_name(self, capsys):
        """Test generating with custom project name."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("cli.factory_cli.ProjectGenerator") as mock_gen:
                mock_instance = MagicMock()
                mock_instance.generate.return_value = {
                    "success": True,
                    "files_created": [],
                    "target_dir": tmpdir,
                }
                mock_gen.return_value = mock_instance

                generate_from_blueprint(
                    "python-fastapi", tmpdir, project_name="my-custom-name"
                )

    def test_generate_with_pm_enabled(self, capsys):
        """Test generating with PM system enabled."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("cli.factory_cli.ProjectGenerator") as mock_gen:
                mock_instance = MagicMock()
                mock_instance.generate.return_value = {
                    "success": True,
                    "files_created": [],
                    "target_dir": tmpdir,
                }
                mock_gen.return_value = mock_instance

                generate_from_blueprint(
                    "python-fastapi",
                    tmpdir,
                    pm_enabled=True,
                    pm_backend="github",
                    pm_methodology="scrum",
                )

                captured = capsys.readouterr()
                assert "PM system enabled" in captured.out


class TestGenerateFromConfigFile:
    """Tests for generate_from_config_file function."""

    def test_generate_from_json_config(self, capsys):
        """Test generating from JSON config file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.json"
            config_data = {
                "project_name": "test-project",
                "project_description": "Test",
                "domain": "web",
                "primary_language": "python",
                "frameworks": [],
                "triggers": [],
                "agents": [],
                "skills": [],
                "mcp_servers": [],
            }
            config_path.write_text(json.dumps(config_data))

            output_dir = Path(tmpdir) / "output"

            with patch("cli.factory_cli.ProjectGenerator") as mock_gen:
                mock_instance = MagicMock()
                mock_instance.generate.return_value = {
                    "success": True,
                    "files_created": [],
                    "target_dir": str(output_dir),
                }
                mock_gen.return_value = mock_instance

                generate_from_config_file(str(config_path), str(output_dir))

                captured = capsys.readouterr()
                assert "SUCCESS" in captured.out

    def test_generate_from_nonexistent_config(self, capsys):
        """Test generating from non-existent config file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(SystemExit) as exc_info:
                generate_from_config_file("/nonexistent/config.json", tmpdir)

            assert exc_info.value.code == 1


class TestAnalyzeRepository:
    """Tests for analyze_repository function."""

    def test_analyze_valid_repository(self, capsys):
        """Test analyzing a valid repository."""
        with tempfile.TemporaryDirectory() as tmpdir:
            analyze_repository(tmpdir)

            captured = capsys.readouterr()
            assert "Analyzing repository" in captured.out

    def test_analyze_with_artifacts(self, capsys):
        """Test analyzing repository with existing artifacts."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            (repo_path / ".agentrules").write_text("# Rules")

            analyze_repository(tmpdir)

            captured = capsys.readouterr()
            assert "Analyzing" in captured.out


class TestOnboardRepository:
    """Tests for onboard_repository function."""

    def test_onboard_fresh_repository(self, capsys):
        """Test onboarding a fresh repository."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("cli.factory_cli.ProjectGenerator") as mock_gen:
                mock_instance = MagicMock()
                mock_instance.generate.return_value = {
                    "success": True,
                    "files_created": ["file1"],
                    "scenario": "fresh",
                    "skipped": [],
                    "merged": [],
                }
                mock_gen.return_value = mock_instance

                onboard_repository(tmpdir)

                captured = capsys.readouterr()
                assert "Onboarding" in captured.out

    def test_onboard_with_blueprint(self, capsys):
        """Test onboarding with specific blueprint."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("cli.factory_cli.ProjectGenerator") as mock_gen:
                mock_instance = MagicMock()
                mock_instance.generate.return_value = {
                    "success": True,
                    "files_created": [],
                    "scenario": "fresh",
                    "skipped": [],
                    "merged": [],
                }
                mock_gen.return_value = mock_instance

                onboard_repository(tmpdir, blueprint_id="python-fastapi")

    def test_onboard_dry_run(self, capsys):
        """Test onboarding in dry run mode."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("cli.factory_cli.ProjectGenerator") as mock_gen:
                mock_instance = MagicMock()
                mock_instance.generate.return_value = {
                    "success": True,
                    "files_created": [],
                    "scenario": "fresh",
                    "skipped": [],
                    "merged": [],
                }
                mock_gen.return_value = mock_instance

                onboard_repository(tmpdir, dry_run=True)

                captured = capsys.readouterr()
                assert "DRY RUN" in captured.out


class TestRollbackSession:
    """Tests for rollback_session function."""

    def test_rollback_no_sessions(self, capsys):
        """Test rollback when no sessions exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            rollback_session(tmpdir)

            captured = capsys.readouterr()
            assert "No backup sessions" in captured.out

    def test_rollback_with_sessions_quit(self, capsys):
        """Test rollback session list and quit."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a backup session
            from scripts.git.backup_manager import BackupManager

            manager = BackupManager(Path(tmpdir))
            session = manager.create_session("Test session")
            session.complete()

            with patch("builtins.input", return_value="q"):
                rollback_session(tmpdir)


class TestCreateDefaultConfig:
    """Tests for _create_default_config function."""

    def test_creates_config_from_inventory(self):
        """Test creating config from inventory."""
        from scripts.analysis.repo_analyzer import RepoInventory, TechStackDetection

        inventory = RepoInventory(path=Path("/test"))
        inventory.tech_stack = TechStackDetection(
            languages=["python"],
            frameworks=["fastapi"],
        )

        config = _create_default_config("/test", inventory)

        assert config.project_name == "test"
        assert config.primary_language == "python"
        assert "code-reviewer" in config.agents


class TestInteractiveConflictResolver:
    """Tests for _interactive_conflict_resolver function."""

    def test_resolver_returns_recommendation_on_empty_input(self):
        """Test resolver returns recommendation on empty input."""
        from scripts.git.merge_strategy import (
            Conflict,
            ConflictPrompt,
            ConflictResolution,
            ArtifactType,
        )

        conflict = Conflict(
            artifact_type=ArtifactType.AGENT,
            artifact_name="test",
            existing_path=Path("/test"),
            new_content="New",
        )

        prompt = ConflictPrompt(
            conflict=conflict,
            options=[ConflictResolution.KEEP_EXISTING, ConflictResolution.REPLACE],
            recommendation=ConflictResolution.KEEP_EXISTING,
            reason="Test reason",
        )

        with patch("builtins.input", return_value=""):
            result = _interactive_conflict_resolver(prompt)
            assert result == ConflictResolution.KEEP_EXISTING

    def test_resolver_returns_selected_option(self):
        """Test resolver returns selected option."""
        from scripts.git.merge_strategy import (
            Conflict,
            ConflictPrompt,
            ConflictResolution,
            ArtifactType,
        )

        conflict = Conflict(
            artifact_type=ArtifactType.AGENT,
            artifact_name="test",
            existing_path=Path("/test"),
            new_content="New",
        )

        prompt = ConflictPrompt(
            conflict=conflict,
            options=[ConflictResolution.KEEP_EXISTING, ConflictResolution.REPLACE],
            recommendation=ConflictResolution.KEEP_EXISTING,
            reason="Test reason",
        )

        with patch("builtins.input", return_value="2"):
            result = _interactive_conflict_resolver(prompt)
            assert result == ConflictResolution.REPLACE


class TestMain:
    """Tests for main function."""

    def test_main_no_args_shows_help(self, capsys):
        """Test main with no arguments shows help."""
        with patch("sys.argv", ["factory_cli.py"]):
            main()

            captured = capsys.readouterr()
            assert (
                "usage" in captured.out.lower()
                or "help" in captured.out.lower()
                or "Examples" in captured.out
            )

    def test_main_list_blueprints(self, capsys):
        """Test main with --list-blueprints."""
        with patch("sys.argv", ["factory_cli.py", "--list-blueprints"]):
            main()

            captured = capsys.readouterr()
            assert "Available Blueprints" in captured.out

    def test_main_list_patterns(self, capsys):
        """Test main with --list-patterns."""
        with patch("sys.argv", ["factory_cli.py", "--list-patterns"]):
            main()

            captured = capsys.readouterr()
            assert "Available Patterns" in captured.out

    def test_main_analyze(self, capsys):
        """Test main with --analyze."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("sys.argv", ["factory_cli.py", "--analyze", tmpdir]):
                main()

                captured = capsys.readouterr()
                assert "Analyzing" in captured.out

    def test_main_quickstart(self, capsys):
        """Test main with --quickstart."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch(
                "sys.argv",
                ["factory_cli.py", "--quickstart", "--quickstart-output", tmpdir],
            ):
                with patch("cli.factory_cli.ProjectGenerator") as mock_gen:
                    mock_instance = MagicMock()
                    mock_instance.generate.return_value = {
                        "success": True,
                        "files_created": ["file1"],
                    }
                    mock_gen.return_value = mock_instance

                    main()

    def test_main_blueprint_without_output_fails(self, capsys):
        """Test main with --blueprint but no --output fails."""
        with patch("sys.argv", ["factory_cli.py", "--blueprint", "python-fastapi"]):
            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 1

    def test_main_blueprint_with_output(self, capsys):
        """Test main with --blueprint and --output."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch(
                "sys.argv",
                ["factory_cli.py", "--blueprint", "python-fastapi", "--output", tmpdir],
            ):
                with patch("cli.factory_cli.ProjectGenerator") as mock_gen:
                    mock_instance = MagicMock()
                    mock_instance.generate.return_value = {
                        "success": True,
                        "files_created": [],
                        "target_dir": tmpdir,
                    }
                    mock_gen.return_value = mock_instance

                    main()

    def test_main_version(self, capsys):
        """Test main with --version."""
        with patch("sys.argv", ["factory_cli.py", "--version"]):
            with pytest.raises(SystemExit) as exc_info:
                main()

            # argparse exits with 0 for --version
            assert exc_info.value.code == 0
