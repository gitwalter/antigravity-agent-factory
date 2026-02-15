#!/usr/bin/env python3
"""
Tests for scripts/validation/sync_artifacts.py

Comprehensive tests for the unified artifact sync system including:
- Configuration loading from sync_config.json
- Artifact scanning with inclusion/exclusion logic
- Sync strategies (count, json_field, category_counts, tree_annotation)
- Directory-based triggers for CI optimization
- Integration with actual project files

### Why This Matters
Artifact synchronization ensures that the factory's documentation (README, guides, catalogs)
stays perfectly in sync with the actual code and data (agents, skills, tests).
This prevents documentation rot, provides accurate metrics to users, and ensures
that generated catalogs always reflect the current capabilities of the factory.
In CI, these tests prevent pushing changes that would leave documentation in an
inconsistent state.
"""

import json
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

# Import the module under test
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.validation.sync_artifacts import (
    SyncTarget,
    ArtifactConfig,
    ArtifactScanner,
    CountSyncStrategy,
    JsonFieldSyncStrategy,
    CategoryTestCounts,
    get_python_path,
    collect_test_count,
    extract_documented_counts,
    update_testing_md,
    SyncEngine,
)


# =============================================================================
# ARTIFACT SCANNER TESTS
# =============================================================================


class TestArtifactScanner:
    """Tests for the ArtifactScanner class."""

    def test_scan_finds_matching_files(self, tmp_path):
        """
        Verify that the scanner correctly identifies files matching a glob pattern.

        How: Creates a dummy directory structure with matching and non-matching files,
        then runs the scanner with a specific glob pattern.
        Why: Ensures the core scanning logic can distinguish between artifacts and
        other files in the source directory.
        """
        # Create test directory structure
        agents_dir = tmp_path / ".agent" / "agents"
        agents_dir.mkdir(parents=True)
        (agents_dir / "agent1.md").write_text("# Agent 1", encoding="utf-8")
        (agents_dir / "agent2.md").write_text("# Agent 2", encoding="utf-8")
        (agents_dir / "readme.txt").write_text("Not an agent", encoding="utf-8")

        scanner = ArtifactScanner(tmp_path)
        config = ArtifactConfig(
            name="agents",
            description="Test agents",
            source_dir=".agent/agents",
            pattern="*.md",
            recursive=False,
        )

        artifacts = scanner.scan(config)

        assert len(artifacts) == 2
        assert {a.id for a in artifacts} == {"agent1", "agent2"}

    def test_scan_respects_exclusions(self, tmp_path):
        """
        Verify that the scanner respects the exclusion list in the configuration.

        How: Creates a directory structure with a subdirectory that should be excluded,
        then runs the scanner with an exclusion pattern.
        Why: Allows users to skip certain files or directories (like templates or
        internal metadata) when scanning for artifacts.
        """
        agents_dir = tmp_path / ".agent" / "agents"
        pm_dir = agents_dir / "pm"
        agents_dir.mkdir(parents=True)
        pm_dir.mkdir()

        (agents_dir / "agent1.md").write_text("# Agent 1", encoding="utf-8")
        (pm_dir / "pm-agent.md").write_text("# PM Agent", encoding="utf-8")

        scanner = ArtifactScanner(tmp_path)
        config = ArtifactConfig(
            name="agents",
            description="Test agents",
            source_dir=".agent/agents",
            pattern="*.md",
            recursive=True,
            exclude=["pm/"],
        )

        artifacts = scanner.scan(config)

        assert len(artifacts) == 1
        assert artifacts[0].id == "agent1"

    def test_scan_recursive(self, tmp_path):
        """
        Verify that the scanner can perform recursive searches when configured.

        How: Creates separate levels of directories and files, then runs the scanner
        with recursive=True and a broad pattern.
        Why: Essential for artifacts that may be nested deep within a directory
        structure, such as workflow definitions or multi-level skills.
        """
        patterns_dir = tmp_path / "patterns"
        subdir = patterns_dir / "skills"
        patterns_dir.mkdir()
        subdir.mkdir()

        (patterns_dir / "pattern1.json").write_text("{}", encoding="utf-8")
        (subdir / "pattern2.json").write_text("{}", encoding="utf-8")

        scanner = ArtifactScanner(tmp_path)
        config = ArtifactConfig(
            name="patterns",
            description="Test patterns",
            source_dir="patterns",
            pattern="**/*.json",
            recursive=True,
        )

        artifacts = scanner.scan(config)

        assert len(artifacts) == 2

    def test_scan_parent_dir_id_extractor(self, tmp_path):
        """
        Verify that artifact IDs can be extracted from their parent directory names.

        How: Places a file in a named subdirectory and runs the scanner with
        id_extractor='parent_dir_name'.
        Why: Supports artifacts where the folder name is the primary identifier
        (e.g., skill or blueprint folders containing a standardized SKILL.md file).
        """
        skills_dir = tmp_path / ".agent" / "skills"
        skill1_dir = skills_dir / "my-skill"
        skills_dir.mkdir(parents=True)
        skill1_dir.mkdir()

        (skill1_dir / "SKILL.md").write_text("# Skill", encoding="utf-8")

        scanner = ArtifactScanner(tmp_path)
        config = ArtifactConfig(
            name="skills",
            description="Test skills",
            source_dir=".agent/skills",
            pattern="*/SKILL.md",
            id_extractor="parent_dir_name",
        )

        artifacts = scanner.scan(config)

        assert len(artifacts) == 1
        assert artifacts[0].id == "my-skill"

    def test_scan_returns_empty_for_missing_dir(self, tmp_path):
        """
        Verify that the scanner handles non-existent source directories gracefully.

        How: Configures a scan for a directory that does not exist in the filesystem.
        Why: Prevents the sync engine from crashing if a configured directory is
        missing or has been renamed, returning an empty set of artifacts instead.
        """
        scanner = ArtifactScanner(tmp_path)
        config = ArtifactConfig(
            name="missing",
            description="Missing dir",
            source_dir="nonexistent",
            pattern="*.md",
        )

        artifacts = scanner.scan(config)

        assert len(artifacts) == 0


# =============================================================================
# COUNT SYNC STRATEGY TESTS
# =============================================================================


class TestCountSyncStrategy:
    """Tests for the CountSyncStrategy class."""

    def test_detects_out_of_sync_count(self, tmp_path):
        """
        Verify that the count strategy correctly identifies a mismatch in numbers.

        How: Provides a file with a specific count and compares it against a
        different actual count.
        Why: The primary mechanism for ensuring that README footers or guide
        summaries accurately reflect the current file counts in the repo.
        """
        readme = tmp_path / "README.md"
        readme.write_text("# Project\n\nagents/ (10 agents)\n", encoding="utf-8")

        strategy = CountSyncStrategy(tmp_path)
        target = SyncTarget(
            type="count",
            file="README.md",
            pattern=r"agents/\s*\((\d+) agents?\)",
            replacement="agents/ ({count} agents)",
        )

        result = strategy.sync(target, 15, [], dry_run=True)

        assert result.changed is True
        assert result.old_value == 10
        assert result.new_value == 15

    def test_reports_in_sync_when_matched(self, tmp_path):
        """
        Verify that the count strategy reports no changes when the numbers match.

        How: Provides a file with a count that perfectly matches the actual count.
        Why: Ensures that the sync process is idempotent and doesn't perform
        unnecessary file writes when the state is already correct.
        """
        readme = tmp_path / "README.md"
        readme.write_text("# Project\n\nagents/ (10 agents)\n", encoding="utf-8")

        strategy = CountSyncStrategy(tmp_path)
        target = SyncTarget(
            type="count",
            file="README.md",
            pattern=r"agents/\s*\((\d+) agents?\)",
            replacement="agents/ ({count} agents)",
        )

        result = strategy.sync(target, 10, [], dry_run=True)

        assert result.changed is False

    def test_dry_run_does_not_modify_file(self, tmp_path):
        """
        Verify that dry-run mode correctly avoids any filesystem modifications.

        How: Runs the sync logic with dry_run=True and then checks the file content
        remains identical to the original.
        Why: Critical for CI validation where we want to detect drift without
        actually changing the files in the checkout.
        """
        readme = tmp_path / "README.md"
        original = "# Project\n\nagents/ (10 agents)\n"
        readme.write_text(original, encoding="utf-8")

        strategy = CountSyncStrategy(tmp_path)
        target = SyncTarget(
            type="count",
            file="README.md",
            pattern=r"agents/\s*\((\d+) agents?\)",
            replacement="agents/ ({count} agents)",
        )

        strategy.sync(target, 15, [], dry_run=True)

        assert readme.read_text(encoding="utf-8") == original

    def test_updates_file_when_sync(self, tmp_path):
        """
        Verify that the strategy correctly updates the file content when syncing.

        How: Runs the sync logic with dry_run=False and then checks the file content
        has been updated with the new count.
        Why: Ensures the auto-fix capability of the sync script actually works
        and correctly applies the regex-based replacement.
        """
        readme = tmp_path / "README.md"
        readme.write_text("# Project\n\nagents/ (10 agents)\n", encoding="utf-8")

        strategy = CountSyncStrategy(tmp_path)
        target = SyncTarget(
            type="count",
            file="README.md",
            pattern=r"agents/\s*\((\d+) agents?\)",
            replacement="agents/ ({count} agents)",
        )

        strategy.sync(target, 15, [], dry_run=False)

        content = readme.read_text(encoding="utf-8")
        assert "(15 agents)" in content


# =============================================================================
# JSON FIELD SYNC STRATEGY TESTS
# =============================================================================


class TestJsonFieldSyncStrategy:
    """Tests for the JsonFieldSyncStrategy class."""

    def test_updates_nested_json_field(self, tmp_path):
        """
        Verify that the JSON strategy can update values deep within a nested structure.

        How: Creates a JSON file with nested property and runs sync with dot-walk path.
        Why: Many project meta-files (like manifest.json) use nested objects for
        organization, and we must be able to target them precisely.
        """
        manifest = tmp_path / "manifest.json"
        manifest.write_text(
            json.dumps({"statistics": {"total_files": 50}}), encoding="utf-8"
        )

        strategy = JsonFieldSyncStrategy(tmp_path)
        target = SyncTarget(
            type="json_field", file="manifest.json", json_path="statistics.total_files"
        )

        result = strategy.sync(target, 72, [], dry_run=False)

        assert result.changed is True
        assert result.old_value == 50
        assert result.new_value == 72

        data = json.loads(manifest.read_text(encoding="utf-8"))
        assert data["statistics"]["total_files"] == 72

    def test_creates_missing_nested_structure(self, tmp_path):
        """
        Verify that the JSON strategy creates missing parent objects if they don't exist.

        How: Targets a nested path in an empty JSON object.
        Why: Simplifies configuration by allowing the sync process to initialize
        statistics or metadata structures if they are missing from a new file.
        """
        manifest = tmp_path / "manifest.json"
        manifest.write_text(json.dumps({}), encoding="utf-8")

        strategy = JsonFieldSyncStrategy(tmp_path)
        target = SyncTarget(
            type="json_field", file="manifest.json", json_path="statistics.total_files"
        )

        result = strategy.sync(target, 72, [], dry_run=False)

        data = json.loads(manifest.read_text(encoding="utf-8"))
        assert data["statistics"]["total_files"] == 72


# =============================================================================
# SYNC ENGINE TESTS
# =============================================================================


class TestSyncEngine:
    """Tests for the SyncEngine class."""

    def test_loads_config_from_file(self, tmp_path):
        """
        Verify that the SyncEngine correctly parses the main sync_config.json file.

        How: Creates a valid mock config file and initializes the engine with it.
        Why: The entire sync system is drive by this configuration; failure to
        parse it correctly would break all synchronization tasks.
        """
        config_dir = tmp_path / "scripts" / "validation"
        config_dir.mkdir(parents=True)

        config_file = config_dir / "sync_config.json"
        config_file.write_text(
            json.dumps(
                {
                    "artifacts": {
                        "test_artifact": {
                            "description": "Test",
                            "source_dir": "test",
                            "pattern": "*.md",
                            "targets": [
                                {
                                    "type": "count",
                                    "file": "README.md",
                                    "pattern": "test",
                                }
                            ],
                        }
                    }
                }
            ),
            encoding="utf-8",
        )

        engine = SyncEngine(tmp_path, config_file)

        assert "test_artifact" in engine.config
        assert engine.config["test_artifact"].description == "Test"

    def test_get_directory_triggers(self, tmp_path):
        """
        Verify that the engine correctly maps source directories to artifact types.

        How: Configures directory triggers and checks the returned mapping.
        Why: Used by CI to determine which documentation files need re-syncing
        based on which code directories were modified in a pull request.
        """
        config_dir = tmp_path / "scripts" / "validation"
        config_dir.mkdir(parents=True)

        config_file = config_dir / "sync_config.json"
        config_file.write_text(
            json.dumps(
                {
                    "artifacts": {},
                    "directory_triggers": {
                        ".agent/agents": ["agents"],
                        "knowledge": ["knowledge"],
                    },
                }
            ),
            encoding="utf-8",
        )

        engine = SyncEngine(tmp_path, config_file)
        triggers = engine.get_directory_triggers()

        assert ".agent/agents" in triggers
        assert triggers[".agent/agents"] == ["agents"]

    def test_get_artifacts_for_dirs(self, tmp_path):
        """
        Verify that the engine identifies the correct artifacts impacted by changed dirs.

        How: Provided a list of changed paths and checks if the corresponding
        artifacts are returned.
        Why: Critical for 'smart sync' where we only run expensive validation and
        sync tasks for components that actually changed.
        """
        config_dir = tmp_path / "scripts" / "validation"
        config_dir.mkdir(parents=True)

        config_file = config_dir / "sync_config.json"
        config_file.write_text(
            json.dumps(
                {
                    "artifacts": {},
                    "directory_triggers": {
                        ".agent/agents": ["agents"],
                        "knowledge": ["knowledge"],
                    },
                }
            ),
            encoding="utf-8",
        )

        engine = SyncEngine(tmp_path, config_file)

        artifacts = engine.get_artifacts_for_dirs([".agent/agents", "knowledge"])

        assert set(artifacts) == {"agents", "knowledge"}

    def test_sync_artifact_unknown_returns_error(self, tmp_path):
        """
        Verify that requesting a sync for a non-existent artifact returns an error.

        How: Calls sync_artifact with an ID that is not in the configuration.
        Why: Ensures the API provides feedback when invalid artifact types are
        requested, rather than failing silently or with a generic error.
        """
        config_dir = tmp_path / "scripts" / "validation"
        config_dir.mkdir(parents=True)

        config_file = config_dir / "sync_config.json"
        config_file.write_text(json.dumps({"artifacts": {}}), encoding="utf-8")

        engine = SyncEngine(tmp_path, config_file)
        results = engine.sync_artifact("nonexistent", dry_run=True)

        assert len(results) == 1
        assert "Unknown artifact" in results[0].message


# =============================================================================
# INTEGRATION TESTS
# =============================================================================


class TestIntegration:
    """Integration tests using actual project files."""

    @pytest.fixture
    def factory_root(self):
        """Get the factory root directory."""
        # File is at tests/unit/sync/test_sync_artifacts.py
        # Root is 4 levels up
        return Path(__file__).parent.parent.parent.parent

    def test_config_file_exists(self, factory_root):
        """
        Sanity check that the actual production sync_config.json exists in the repo.

        How: Checks for the existence of the config file relative to factory root.
        Why: The entire validation suite relies on this file; its absence would
        be a critical repository misconfiguration.
        """
        config_path = factory_root / "scripts" / "validation" / "sync_config.json"
        assert config_path.exists(), "sync_config.json not found"

    def test_config_is_valid_json(self, factory_root):
        """
        Verify that the production sync_config.json is valid and readable JSON.

        How: Attempts to load the actual config file with the json library.
        Why: Prevents accidental syntax errors in the JSON config from breaking
        the CI pipeline.
        """
        config_path = factory_root / "scripts" / "validation" / "sync_config.json"
        content = config_path.read_text(encoding="utf-8")

        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            pytest.fail(f"Invalid JSON: {e}")

        assert "artifacts" in data

    def test_config_has_all_artifact_types(self, factory_root):
        """
        Verify that all core factory artifacts are defined in the sync configuration.

        How: Checks the artifact list against the expected set of factory types.
        Why: Ensures developers don't forget to add documentation sync rules
        when new artifact types are added to the system.
        """
        config_path = factory_root / "scripts" / "validation" / "sync_config.json"
        data = json.loads(config_path.read_text(encoding="utf-8"))

        expected_artifacts = {
            "agents",
            "skills",
            "blueprints",
            "patterns",
            "knowledge",
            "templates",
            "tests",
        }
        actual_artifacts = set(data.get("artifacts", {}).keys())

        missing = expected_artifacts - actual_artifacts
        assert not missing, f"Missing artifact definitions: {missing}"

    def test_engine_loads_successfully(self, factory_root):
        """
        Verify that the SyncEngine can initialize with the real production config.

        How: Initializes a new SyncEngine instance pointing to the repo root.
        Why: Validates that the production config is not only valid JSON but
        also logically correct for the defined SyncEngine schema.
        """
        engine = SyncEngine(factory_root)

        assert len(engine.config) > 0
        assert "agents" in engine.config

    def test_sync_all_dry_run_succeeds(self, factory_root):
        """
        Perform a full dry-run sync across all artifacts in the actual repository.

        How: Runs engine.sync_all(dry_run=True) and checks for errors in the results.
        Why: This is the definitive integration test for the Entire Repo's
        documentation state. It ensures every sync target is valid and reachable.
        """
        import os

        original_cwd = os.getcwd()
        try:
            os.chdir(factory_root)

            engine = SyncEngine(factory_root)
            results = engine.sync_all(dry_run=True)

            # Should have results for each artifact
            assert len(results) > 0

            # No errors should have occurred
            errors = [r for r in results if "error" in r.message.lower()]
            assert len(errors) == 0, f"Errors occurred: {errors}"
        finally:
            os.chdir(original_cwd)

    def test_artifacts_are_currently_synced(self, factory_root):
        """
        Verify that the repository documentation is currently in a perfectly synced state.

        How: Runs sync_all and asserts that zero 'changed' status items are returned.
        Why: Used as a CI gate to ensure PRs don't introduce documentation drift.
        If this fails, the developer must run 'sync_artifacts.py --sync' locally.
        """
        import os

        original_cwd = os.getcwd()
        try:
            os.chdir(factory_root)

            engine = SyncEngine(factory_root)
            results = engine.sync_all(dry_run=True)

            # Filter out "No strategy" messages (for unimplemented features)
            real_changes = [
                r for r in results if r.changed and "No strategy" not in r.message
            ]

            assert (
                len(real_changes) == 0
            ), f"Out of sync: {[r.message for r in real_changes]}"
        finally:
            os.chdir(original_cwd)


class TestDirectoryDetection:
    """Tests for directory-based sync triggering."""

    def test_detects_agents_dir(self, tmp_path):
        """
        Verify that changes to the agents directory trigger a sync for that artifact.

        How: Simulates a change to an agent file and checks if the 'agents'
        artifact type is correctly identified.
        Why: Documentation for agents (like README counts) must be updated
        whenever an agent is added, removed, or changed.
        """
        config_dir = tmp_path / "scripts" / "validation"
        config_dir.mkdir(parents=True)

        config_file = config_dir / "sync_config.json"
        config_file.write_text(
            json.dumps(
                {"artifacts": {}, "directory_triggers": {".agent/agents": ["agents"]}}
            ),
            encoding="utf-8",
        )

        engine = SyncEngine(tmp_path, config_file)
        artifacts = engine.get_artifacts_for_dirs([".agent/agents/new-agent.md"])

        assert "agents" in artifacts

    def test_detects_nested_path(self, tmp_path):
        """
        Verify that nested file changes correctly trigger parent artifact syncs.

        How: Simulates a change to a deeply nested file within a trigger directory.
        Why: Ensures that changes to sub-components (like a specific skill's
        internal logic) still trigger the high-level artifact sync.
        """
        config_dir = tmp_path / "scripts" / "validation"
        config_dir.mkdir(parents=True)

        config_file = config_dir / "sync_config.json"
        config_file.write_text(
            json.dumps(
                {"artifacts": {}, "directory_triggers": {"patterns": ["patterns"]}}
            ),
            encoding="utf-8",
        )

        engine = SyncEngine(tmp_path, config_file)
        artifacts = engine.get_artifacts_for_dirs(["patterns/skills/new-pattern.json"])

        assert "patterns" in artifacts


# =============================================================================
# HELPER FUNCTION TESTS
# =============================================================================


class TestCategoryTestCounts:
    """Tests for the CategoryTestCounts NamedTuple."""

    def test_creates_valid_namedtuple(self):
        """Should create a valid CategoryTestCounts instance."""
        counts = CategoryTestCounts(
            total=100, unit=50, integration=30, validation=10, guardian=5, memory=5
        )

        assert counts.total == 100
        assert counts.unit == 50
        assert counts.integration == 30
        assert counts.validation == 10
        assert counts.guardian == 5
        assert counts.memory == 5

    def test_counts_are_immutable(self):
        """CategoryTestCounts should be immutable."""
        counts = CategoryTestCounts(100, 50, 30, 10, 5, 5)

        with pytest.raises(AttributeError):
            counts.total = 200


class TestGetPythonPath:
    """Tests for Python path detection."""

    def test_returns_current_interpreter(self, monkeypatch):
        """
        Verify that get_python_path returns the current active Python interpreter.

        How: Compares the function result against sys.executable.
        Why: Ensures that sync scripts run by the factory use the same
        environment/interpreter as the factory itself, avoiding dependency issues.
        """
        path = get_python_path()
        assert path == sys.executable


class TestCollectTestCount:
    """Tests for test count collection."""

    def test_returns_integer(self):
        """
        Verify that collect_test_count returns the number of tests as an integer.

        How: Mocks the subprocess call to return a standard pytest collection
        output and checks if the correct number is parsed.
        Why: Core helper for the 'tests' artifact count target.
        """
        # Mock subprocess to avoid actually running pytest
        with patch("scripts.validation.sync_artifacts.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                stdout="======================== 42 tests collected in 1.00s ========================\n",
                returncode=0,
            )

            count = collect_test_count("unit")
            assert isinstance(count, int)
            assert count == 42

    def test_handles_subprocess_timeout(self):
        """
        Verify that the collector handles subprocess timeouts gracefully by returning 0.

        How: Simulates a TimeoutExpired exception in the mocked subprocess.run call.
        Why: Prevents the entire sync process from hanging if pytest takes too long
        to collect tests (e.g., due to extreme recursion in test generators).
        """
        import subprocess

        with patch("scripts.validation.sync_artifacts.subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired(cmd="pytest", timeout=120)

            count = collect_test_count("unit")
            assert count == 0

    def test_handles_missing_directory(self, tmp_path):
        """
        Verify that the collector returns 0 when the target test directory is missing.

        How: Attempts to collect tests from a non-existent path.
        Why: Ensures that if a test category is renamed or deleted, the sync
        script doesn't crash, but instead reports 0 tests.
        """
        count = collect_test_count("nonexistent", root_path=tmp_path)
        assert count == 0

    def test_parses_plural_tests(self):
        """
        Verify that the parser correctly extracts counts when multiple tests are found.

        How: Provides '100 tests collected' string to the parser.
        Why: Pytest uses plural 'tests' when count > 1.
        """
        with patch("scripts.validation.sync_artifacts.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                stdout="======================== 100 tests collected in 5.00s ========================\n",
                returncode=0,
            )

            count = collect_test_count(None)
            assert count == 100

    def test_parses_singular_test(self):
        """
        Verify that the parser correctly extracts counts when exactly one test is found.

        How: Provides '1 test collected' string to the parser.
        Why: Ensure the regex handles the singular 'test' case which has different
        output formatting in pytest.
        """
        with patch("scripts.validation.sync_artifacts.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                stdout="======================== 1 test collected in 0.50s ========================\n",
                returncode=0,
            )

            count = collect_test_count(None)
            assert count == 1


class TestExtractDocumentedCounts:
    """Tests for extracting counts from TESTING.md content."""

    def test_extracts_total_count(self):
        """Should extract total test count."""
        content = """
## Overview

The test suite uses **pytest** and consists of **942 tests** organized into five categories:

| Category | Tests | Purpose |
|----------|-------|---------|
| Unit Tests | ~589 | Test individual components |
| Integration Tests | ~142 | Test component interactions |
| Validation Tests | ~135 | Validate JSON schemas |
| Guardian Tests | ~31 | Test integrity protection |
| Memory Tests | ~45 | Test memory system |
"""
        counts = extract_documented_counts(content)

        assert counts.total == 942

    def test_extracts_category_counts(self):
        """Should extract all category counts."""
        content = """
| Category | Tests | Purpose |
|----------|-------|---------|
| Unit Tests | ~589 | Test individual components |
| Integration Tests | ~142 | Test component interactions |
| Validation Tests | ~135 | Validate JSON schemas |
| Guardian Tests | ~31 | Test integrity protection |
| Memory Tests | ~45 | Test memory system |
"""
        counts = extract_documented_counts(content)

        assert counts.unit == 589
        assert counts.integration == 142
        assert counts.validation == 135
        assert counts.guardian == 31
        assert counts.memory == 45

    def test_handles_missing_total(self):
        """
        Verify that the extractor returns 0 for the total if it's not found in content.

        How: Provides a string that does not match the 'consists of **X tests**' pattern.
        Why: Robustness against malformed or missing documentation sections.
        """
        content = "No test counts here"
        counts = extract_documented_counts(content)

        assert counts.total == 0

    def test_handles_missing_categories(self):
        """
        Verify that the extractor returns 0 for categories missing from the table.

        How: Provides a string with a total count but no category table.
        Why: Ensures the sync script doesn't crash if only the total count exists
        but the category breakdown is missing.
        """
        content = "The test suite consists of **100 tests**"
        counts = extract_documented_counts(content)

        assert counts.unit == 0
        assert counts.integration == 0


class TestUpdateTestingMd:
    """Tests for updating TESTING.md."""

    def test_detects_out_of_sync_total(self, tmp_path):
        """Should detect when total count is out of sync."""
        testing_dir = tmp_path / "docs" / "testing"
        testing_dir.mkdir(parents=True)
        testing_md = testing_dir / "testing.md"
        testing_md.write_text(
            """
## Overview

The test suite uses **pytest** and consists of **458 tests** organized into five categories:

| Category | Tests | Purpose |
|----------|-------|---------|
| Unit Tests | ~200 | Test individual components |
| Integration Tests | ~50 | Test component interactions |
| Validation Tests | ~208 | Validate JSON schemas |
| Guardian Tests | ~0 | Not documented |
| Memory Tests | ~0 | Not documented |
""",
            encoding="utf-8",
        )

        actual = CategoryTestCounts(
            total=942, unit=589, integration=142, validation=135, guardian=31, memory=45
        )

        changes = update_testing_md(actual, dry_run=True, root_path=tmp_path)

        assert len(changes) > 0
        assert any("Total tests" in c for c in changes)

    def test_dry_run_does_not_modify_file(self, tmp_path):
        """
        Verify that update_testing_md respects the dry_run flag.

        How: Calls the function with dry_run=True and checks that the file
        remains unchanged despite being out of sync.
        Why: Safety mechanism for validation-only runs.
        """
        testing_dir = tmp_path / "docs" / "testing"
        testing_dir.mkdir(parents=True)
        testing_md = testing_dir / "testing.md"
        original_content = "The test suite consists of **100 tests**"
        testing_md.write_text(original_content, encoding="utf-8")

        actual = CategoryTestCounts(200, 100, 50, 30, 10, 10)
        update_testing_md(actual, dry_run=True, root_path=tmp_path)

        assert testing_md.read_text(encoding="utf-8") == original_content

    def test_sync_updates_file(self, tmp_path):
        """Should update file when dry_run=False."""
        testing_dir = tmp_path / "docs" / "testing"
        testing_dir.mkdir(parents=True)
        testing_md = testing_dir / "testing.md"
        testing_md.write_text(
            """
The test suite uses **pytest** and consists of **100 tests** organized:

| Category | Tests | Purpose |
|----------|-------|---------|
| Unit Tests | ~50 | Test components |
| Integration Tests | ~20 | Test interactions |
| Validation Tests | ~15 | Validate schemas |
| Guardian Tests | ~10 | Test guardian |
| Memory Tests | ~5 | Test memory |
""",
            encoding="utf-8",
        )

        actual = CategoryTestCounts(200, 100, 50, 30, 10, 10)
        changes = update_testing_md(actual, dry_run=False, root_path=tmp_path)

        new_content = testing_md.read_text(encoding="utf-8")
        assert "**200 tests**" in new_content
        assert "| Unit Tests | ~100 |" in new_content

    def test_reports_missing_file(self, tmp_path):
        """
        Verify that update_testing_md handles the absence of the target file.

        How: Calls the function when TESTING.md hasn't been created yet.
        Why: Ensures the sync script provides helpful error messages instead of
        crashing if a target file is missing.
        """
        actual = CategoryTestCounts(100, 50, 30, 10, 5, 5)
        changes = update_testing_md(actual, dry_run=True, root_path=tmp_path)

        assert any("not found" in c for c in changes)

    def test_no_changes_when_synced(self, tmp_path):
        """
        Verify that update_testing_md returns zero changes when counts match EXACTLY.

        How: Provides a file with counts that match the 'actual' parameter.
        Why: Confirms idempotency of the high-level sync operation.
        """
        testing_dir = tmp_path / "docs" / "testing"
        testing_dir.mkdir(parents=True)
        testing_md = testing_dir / "testing.md"
        testing_md.write_text(
            """
The test suite consists of **100 tests**:

| Category | Tests | Purpose |
|----------|-------|---------|
| Unit Tests | ~50 | Test components |
| Integration Tests | ~20 | Test interactions |
| Validation Tests | ~15 | Validate schemas |
| Guardian Tests | ~10 | Test guardian |
| Memory Tests | ~5 | Test memory |
""",
            encoding="utf-8",
        )

        actual = CategoryTestCounts(100, 50, 20, 15, 10, 5)
        changes = update_testing_md(actual, dry_run=True, root_path=tmp_path)

        assert len(changes) == 0
