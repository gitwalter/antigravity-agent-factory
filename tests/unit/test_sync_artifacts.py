#!/usr/bin/env python3
"""
Tests for scripts/validation/sync_artifacts.py

Comprehensive tests for the unified artifact sync system including:
- Configuration loading
- Artifact scanning
- Sync strategies (count, json_field, category_counts, tree_annotation)
- Directory-based triggers
- Integration with actual project files
"""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

# Import the module under test
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.validation.sync_artifacts import (
    ArtifactInfo,
    SyncTarget,
    ArtifactConfig,
    SyncResult,
    ArtifactScanner,
    CountSyncStrategy,
    JsonFieldSyncStrategy,
    TreeAnnotationSyncStrategy,
    SyncEngine,
)


# =============================================================================
# ARTIFACT SCANNER TESTS
# =============================================================================

class TestArtifactScanner:
    """Tests for the ArtifactScanner class."""
    
    def test_scan_finds_matching_files(self, tmp_path):
        """Should find files matching the pattern."""
        # Create test directory structure
        agents_dir = tmp_path / ".agent" / "agents"
        agents_dir.mkdir(parents=True)
        (agents_dir / "agent1.md").write_text("# Agent 1", encoding='utf-8')
        (agents_dir / "agent2.md").write_text("# Agent 2", encoding='utf-8')
        (agents_dir / "readme.txt").write_text("Not an agent", encoding='utf-8')
        
        scanner = ArtifactScanner(tmp_path)
        config = ArtifactConfig(
            name="agents",
            description="Test agents",
            source_dir=".agent/agents",
            pattern="*.md",
            recursive=False
        )
        
        artifacts = scanner.scan(config)
        
        assert len(artifacts) == 2
        assert {a.id for a in artifacts} == {"agent1", "agent2"}
    
    def test_scan_respects_exclusions(self, tmp_path):
        """Should exclude specified patterns."""
        agents_dir = tmp_path / ".agent" / "agents"
        pm_dir = agents_dir / "pm"
        agents_dir.mkdir(parents=True)
        pm_dir.mkdir()
        
        (agents_dir / "agent1.md").write_text("# Agent 1", encoding='utf-8')
        (pm_dir / "pm-agent.md").write_text("# PM Agent", encoding='utf-8')
        
        scanner = ArtifactScanner(tmp_path)
        config = ArtifactConfig(
            name="agents",
            description="Test agents",
            source_dir=".agent/agents",
            pattern="*.md",
            recursive=True,
            exclude=["pm/"]
        )
        
        artifacts = scanner.scan(config)
        
        assert len(artifacts) == 1
        assert artifacts[0].id == "agent1"
    
    def test_scan_recursive(self, tmp_path):
        """Should scan recursively when configured."""
        patterns_dir = tmp_path / "patterns"
        subdir = patterns_dir / "skills"
        patterns_dir.mkdir()
        subdir.mkdir()
        
        (patterns_dir / "pattern1.json").write_text("{}", encoding='utf-8')
        (subdir / "pattern2.json").write_text("{}", encoding='utf-8')
        
        scanner = ArtifactScanner(tmp_path)
        config = ArtifactConfig(
            name="patterns",
            description="Test patterns",
            source_dir="patterns",
            pattern="**/*.json",
            recursive=True
        )
        
        artifacts = scanner.scan(config)
        
        assert len(artifacts) == 2
    
    def test_scan_parent_dir_id_extractor(self, tmp_path):
        """Should extract ID from parent directory name."""
        skills_dir = tmp_path / ".agent" / "skills"
        skill1_dir = skills_dir / "my-skill"
        skills_dir.mkdir(parents=True)
        skill1_dir.mkdir()
        
        (skill1_dir / "SKILL.md").write_text("# Skill", encoding='utf-8')
        
        scanner = ArtifactScanner(tmp_path)
        config = ArtifactConfig(
            name="skills",
            description="Test skills",
            source_dir=".agent/skills",
            pattern="*/SKILL.md",
            id_extractor="parent_dir_name"
        )
        
        artifacts = scanner.scan(config)
        
        assert len(artifacts) == 1
        assert artifacts[0].id == "my-skill"
    
    def test_scan_returns_empty_for_missing_dir(self, tmp_path):
        """Should return empty list for non-existent directory."""
        scanner = ArtifactScanner(tmp_path)
        config = ArtifactConfig(
            name="missing",
            description="Missing dir",
            source_dir="nonexistent",
            pattern="*.md"
        )
        
        artifacts = scanner.scan(config)
        
        assert len(artifacts) == 0


# =============================================================================
# COUNT SYNC STRATEGY TESTS
# =============================================================================

class TestCountSyncStrategy:
    """Tests for the CountSyncStrategy class."""
    
    def test_detects_out_of_sync_count(self, tmp_path):
        """Should detect when count differs from actual."""
        readme = tmp_path / "README.md"
        readme.write_text("# Project\n\nagents/ (10 agents)\n", encoding='utf-8')
        
        strategy = CountSyncStrategy(tmp_path)
        target = SyncTarget(
            type="count",
            file="README.md",
            pattern=r"agents/\s*\((\d+) agents?\)",
            replacement="agents/ ({count} agents)"
        )
        
        result = strategy.sync(target, 15, [], dry_run=True)
        
        assert result.changed is True
        assert result.old_value == 10
        assert result.new_value == 15
    
    def test_reports_in_sync_when_matched(self, tmp_path):
        """Should report in sync when counts match."""
        readme = tmp_path / "README.md"
        readme.write_text("# Project\n\nagents/ (10 agents)\n", encoding='utf-8')
        
        strategy = CountSyncStrategy(tmp_path)
        target = SyncTarget(
            type="count",
            file="README.md",
            pattern=r"agents/\s*\((\d+) agents?\)",
            replacement="agents/ ({count} agents)"
        )
        
        result = strategy.sync(target, 10, [], dry_run=True)
        
        assert result.changed is False
    
    def test_dry_run_does_not_modify_file(self, tmp_path):
        """Should not modify file when dry_run=True."""
        readme = tmp_path / "README.md"
        original = "# Project\n\nagents/ (10 agents)\n"
        readme.write_text(original, encoding='utf-8')
        
        strategy = CountSyncStrategy(tmp_path)
        target = SyncTarget(
            type="count",
            file="README.md",
            pattern=r"agents/\s*\((\d+) agents?\)",
            replacement="agents/ ({count} agents)"
        )
        
        strategy.sync(target, 15, [], dry_run=True)
        
        assert readme.read_text(encoding='utf-8') == original
    
    def test_updates_file_when_sync(self, tmp_path):
        """Should update file when dry_run=False."""
        readme = tmp_path / "README.md"
        readme.write_text("# Project\n\nagents/ (10 agents)\n", encoding='utf-8')
        
        strategy = CountSyncStrategy(tmp_path)
        target = SyncTarget(
            type="count",
            file="README.md",
            pattern=r"agents/\s*\((\d+) agents?\)",
            replacement="agents/ ({count} agents)"
        )
        
        strategy.sync(target, 15, [], dry_run=False)
        
        content = readme.read_text(encoding='utf-8')
        assert "(15 agents)" in content


# =============================================================================
# JSON FIELD SYNC STRATEGY TESTS
# =============================================================================

class TestJsonFieldSyncStrategy:
    """Tests for the JsonFieldSyncStrategy class."""
    
    def test_updates_nested_json_field(self, tmp_path):
        """Should update nested JSON field."""
        manifest = tmp_path / "manifest.json"
        manifest.write_text(json.dumps({
            "statistics": {"total_files": 50}
        }), encoding='utf-8')
        
        strategy = JsonFieldSyncStrategy(tmp_path)
        target = SyncTarget(
            type="json_field",
            file="manifest.json",
            json_path="statistics.total_files"
        )
        
        result = strategy.sync(target, 72, [], dry_run=False)
        
        assert result.changed is True
        assert result.old_value == 50
        assert result.new_value == 72
        
        data = json.loads(manifest.read_text(encoding='utf-8'))
        assert data["statistics"]["total_files"] == 72
    
    def test_creates_missing_nested_structure(self, tmp_path):
        """Should create missing nested structure."""
        manifest = tmp_path / "manifest.json"
        manifest.write_text(json.dumps({}), encoding='utf-8')
        
        strategy = JsonFieldSyncStrategy(tmp_path)
        target = SyncTarget(
            type="json_field",
            file="manifest.json",
            json_path="statistics.total_files"
        )
        
        result = strategy.sync(target, 72, [], dry_run=False)
        
        data = json.loads(manifest.read_text(encoding='utf-8'))
        assert data["statistics"]["total_files"] == 72


# =============================================================================
# SYNC ENGINE TESTS
# =============================================================================

class TestSyncEngine:
    """Tests for the SyncEngine class."""
    
    def test_loads_config_from_file(self, tmp_path):
        """Should load configuration from JSON file."""
        config_dir = tmp_path / "scripts" / "validation"
        config_dir.mkdir(parents=True)
        
        config_file = config_dir / "sync_config.json"
        config_file.write_text(json.dumps({
            "artifacts": {
                "test_artifact": {
                    "description": "Test",
                    "source_dir": "test",
                    "pattern": "*.md",
                    "targets": [
                        {"type": "count", "file": "README.md", "pattern": "test"}
                    ]
                }
            }
        }), encoding='utf-8')
        
        engine = SyncEngine(tmp_path, config_file)
        
        assert "test_artifact" in engine.config
        assert engine.config["test_artifact"].description == "Test"
    
    def test_get_directory_triggers(self, tmp_path):
        """Should return directory trigger mapping."""
        config_dir = tmp_path / "scripts" / "validation"
        config_dir.mkdir(parents=True)
        
        config_file = config_dir / "sync_config.json"
        config_file.write_text(json.dumps({
            "artifacts": {},
            "directory_triggers": {
                ".agent/agents": ["agents"],
                "knowledge": ["knowledge"]
            }
        }), encoding='utf-8')
        
        engine = SyncEngine(tmp_path, config_file)
        triggers = engine.get_directory_triggers()
        
        assert ".agent/agents" in triggers
        assert triggers[".agent/agents"] == ["agents"]
    
    def test_get_artifacts_for_dirs(self, tmp_path):
        """Should return artifacts triggered by directories."""
        config_dir = tmp_path / "scripts" / "validation"
        config_dir.mkdir(parents=True)
        
        config_file = config_dir / "sync_config.json"
        config_file.write_text(json.dumps({
            "artifacts": {},
            "directory_triggers": {
                ".agent/agents": ["agents"],
                "knowledge": ["knowledge"]
            }
        }), encoding='utf-8')
        
        engine = SyncEngine(tmp_path, config_file)
        
        artifacts = engine.get_artifacts_for_dirs([".agent/agents", "knowledge"])
        
        assert set(artifacts) == {"agents", "knowledge"}
    
    def test_sync_artifact_unknown_returns_error(self, tmp_path):
        """Should return error for unknown artifact."""
        config_dir = tmp_path / "scripts" / "validation"
        config_dir.mkdir(parents=True)
        
        config_file = config_dir / "sync_config.json"
        config_file.write_text(json.dumps({"artifacts": {}}), encoding='utf-8')
        
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
        return Path(__file__).parent.parent.parent
    
    def test_config_file_exists(self, factory_root):
        """sync_config.json should exist."""
        config_path = factory_root / "scripts" / "validation" / "sync_config.json"
        assert config_path.exists(), "sync_config.json not found"
    
    def test_config_is_valid_json(self, factory_root):
        """sync_config.json should be valid JSON."""
        config_path = factory_root / "scripts" / "validation" / "sync_config.json"
        content = config_path.read_text(encoding='utf-8')
        
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            pytest.fail(f"Invalid JSON: {e}")
        
        assert "artifacts" in data
    
    def test_config_has_all_artifact_types(self, factory_root):
        """Config should define all expected artifact types."""
        config_path = factory_root / "scripts" / "validation" / "sync_config.json"
        data = json.loads(config_path.read_text(encoding='utf-8'))
        
        expected_artifacts = {"agents", "skills", "blueprints", "patterns", "knowledge", "templates", "tests"}
        actual_artifacts = set(data.get("artifacts", {}).keys())
        
        missing = expected_artifacts - actual_artifacts
        assert not missing, f"Missing artifact definitions: {missing}"
    
    def test_engine_loads_successfully(self, factory_root):
        """SyncEngine should load without errors."""
        engine = SyncEngine(factory_root)
        
        assert len(engine.config) > 0
        assert "agents" in engine.config
    
    def test_sync_all_dry_run_succeeds(self, factory_root):
        """Dry run sync should complete without errors."""
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
        """All artifacts should be in sync after previous sync."""
        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(factory_root)
            
            engine = SyncEngine(factory_root)
            results = engine.sync_all(dry_run=True)
            
            # Filter out "No strategy" messages (for unimplemented features)
            real_changes = [
                r for r in results 
                if r.changed and "No strategy" not in r.message
            ]
            
            assert len(real_changes) == 0, f"Out of sync: {[r.message for r in real_changes]}"
        finally:
            os.chdir(original_cwd)


class TestDirectoryDetection:
    """Tests for directory-based sync triggering."""
    
    def test_detects_agents_dir(self, tmp_path):
        """Should detect .agent/agents directory changes."""
        config_dir = tmp_path / "scripts" / "validation"
        config_dir.mkdir(parents=True)
        
        config_file = config_dir / "sync_config.json"
        config_file.write_text(json.dumps({
            "artifacts": {},
            "directory_triggers": {
                ".agent/agents": ["agents"]
            }
        }), encoding='utf-8')
        
        engine = SyncEngine(tmp_path, config_file)
        artifacts = engine.get_artifacts_for_dirs([".agent/agents/new-agent.md"])
        
        assert "agents" in artifacts
    
    def test_detects_nested_path(self, tmp_path):
        """Should detect nested paths within trigger directories."""
        config_dir = tmp_path / "scripts" / "validation"
        config_dir.mkdir(parents=True)
        
        config_file = config_dir / "sync_config.json"
        config_file.write_text(json.dumps({
            "artifacts": {},
            "directory_triggers": {
                "patterns": ["patterns"]
            }
        }), encoding='utf-8')
        
        engine = SyncEngine(tmp_path, config_file)
        artifacts = engine.get_artifacts_for_dirs(["patterns/skills/new-pattern.json"])
        
        assert "patterns" in artifacts
