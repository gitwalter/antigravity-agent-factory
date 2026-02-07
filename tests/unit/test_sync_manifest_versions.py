#!/usr/bin/env python3
"""
Tests for scripts/validation/sync_manifest_versions.py

Ensures the version sync script correctly:
- Extracts version from CHANGELOG.md
- Identifies out-of-sync versions in various files
- Updates files when --sync is used
"""

import json
import re
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

# Import the module under test
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.validation.sync_manifest_versions import (
    get_changelog_version,
    get_file_version_generic,
    sync_file_version,
    get_file_version,
    sync_manifest,
    VERSION_LOCATIONS,
)


class TestGetChangelogVersion:
    """Tests for extracting version from CHANGELOG.md."""
    
    def test_extracts_version_from_valid_changelog(self, tmp_path, monkeypatch):
        """Should extract the first version header from CHANGELOG.md."""
        changelog = tmp_path / "CHANGELOG.md"
        changelog.write_text("# Changelog\n\n## [3.4.0] - 2026-01-31\n\n### Added\n- Feature\n\n## [3.3.0]\n", encoding='utf-8')
        
        monkeypatch.chdir(tmp_path)
        version = get_changelog_version()
        assert version == "3.4.0"
    
    def test_handles_missing_changelog(self, tmp_path, monkeypatch):
        """Should return 0.0.0 if CHANGELOG.md doesn't exist."""
        monkeypatch.chdir(tmp_path)
        # No CHANGELOG.md file
        version = get_changelog_version()
        assert version == "0.0.0"
    
    def test_handles_changelog_without_version(self, tmp_path, monkeypatch):
        """Should return 0.0.0 if no version header found."""
        changelog = tmp_path / "CHANGELOG.md"
        changelog.write_text("# Changelog\n\nNo versions yet.\n", encoding='utf-8')
        
        monkeypatch.chdir(tmp_path)
        version = get_changelog_version()
        assert version == "0.0.0"


class TestGetFileVersionGeneric:
    """Tests for extracting version from files using regex."""
    
    def test_extracts_version_with_valid_pattern(self, tmp_path):
        """Should extract version matching the pattern."""
        test_file = tmp_path / "test.md"
        test_file.write_text("*Antigravity Agent Factory v3.4.0*\n", encoding='utf-8')
        
        version = get_file_version_generic(
            test_file,
            r'\*Antigravity Agent Factory v(\d+\.\d+\.\d+)\*'
        )
        assert version == "3.4.0"
    
    def test_returns_none_for_missing_file(self, tmp_path):
        """Should return None if file doesn't exist."""
        missing_file = tmp_path / "missing.md"
        
        version = get_file_version_generic(
            missing_file,
            r'v(\d+\.\d+\.\d+)'
        )
        assert version is None
    
    def test_returns_none_for_no_match(self, tmp_path):
        """Should return None if pattern doesn't match."""
        test_file = tmp_path / "test.md"
        test_file.write_text("No version here\n", encoding='utf-8')
        
        version = get_file_version_generic(
            test_file,
            r'v(\d+\.\d+\.\d+)'
        )
        assert version is None


class TestSyncFileVersion:
    """Tests for syncing version in a file."""
    
    def test_dry_run_does_not_modify_file(self, tmp_path):
        """Should not modify file when dry_run=True."""
        test_file = tmp_path / "test.md"
        original_content = "*Antigravity Agent Factory v1.0.0*\n"
        test_file.write_text(original_content, encoding='utf-8')
        
        result = sync_file_version(
            test_file,
            r'\*Antigravity Agent Factory v[\d.]+\*',
            lambda v: f'*Antigravity Agent Factory v{v}*',
            "2.0.0",
            dry_run=True
        )
        
        assert result is True
        assert test_file.read_text(encoding='utf-8') == original_content
    
    def test_sync_updates_file(self, tmp_path):
        """Should update file when dry_run=False."""
        test_file = tmp_path / "test.md"
        test_file.write_text("*Antigravity Agent Factory v1.0.0*\n", encoding='utf-8')
        
        result = sync_file_version(
            test_file,
            r'\*Antigravity Agent Factory v[\d.]+\*',
            lambda v: f'*Antigravity Agent Factory v{v}*',
            "2.0.0",
            dry_run=False
        )
        
        assert result is True
        assert "*Antigravity Agent Factory v2.0.0*" in test_file.read_text(encoding='utf-8')
    
    def test_returns_false_for_missing_file(self, tmp_path):
        """Should return False if file doesn't exist."""
        missing_file = tmp_path / "missing.md"
        
        result = sync_file_version(
            missing_file,
            r'v[\d.]+',
            lambda v: f'v{v}',
            "2.0.0",
            dry_run=True
        )
        
        assert result is False
    
    def test_returns_false_for_no_pattern_match(self, tmp_path):
        """Should return False if pattern doesn't match."""
        test_file = tmp_path / "test.md"
        test_file.write_text("No version here\n", encoding='utf-8')
        
        result = sync_file_version(
            test_file,
            r'v[\d.]+',
            lambda v: f'v{v}',
            "2.0.0",
            dry_run=True
        )
        
        assert result is False


class TestGetFileVersion:
    """Tests for extracting version from JSON knowledge files."""
    
    def test_extracts_version_from_valid_json(self, tmp_path):
        """Should extract version from JSON file."""
        json_file = tmp_path / "test.json"
        json_file.write_text('{"version": "1.2.3", "data": {}}', encoding='utf-8')
        
        version = get_file_version(json_file)
        assert version == "1.2.3"
    
    def test_returns_none_for_missing_version(self, tmp_path):
        """Should return None if no version field."""
        json_file = tmp_path / "test.json"
        json_file.write_text('{"data": {}}', encoding='utf-8')
        
        version = get_file_version(json_file)
        assert version is None
    
    def test_returns_none_for_invalid_json(self, tmp_path):
        """Should return None for invalid JSON."""
        json_file = tmp_path / "test.json"
        json_file.write_text('not valid json', encoding='utf-8')
        
        version = get_file_version(json_file)
        assert version is None
    
    def test_returns_none_for_missing_file(self, tmp_path):
        """Should return None if file doesn't exist."""
        missing_file = tmp_path / "missing.json"
        
        version = get_file_version(missing_file)
        assert version is None


class TestVersionLocations:
    """Tests for VERSION_LOCATIONS configuration."""
    
    def test_all_locations_have_required_keys(self):
        """All VERSION_LOCATIONS entries should have required keys."""
        required_keys = {"file", "name", "pattern", "replacement"}
        
        for loc in VERSION_LOCATIONS:
            missing = required_keys - set(loc.keys())
            assert not missing, f"Location {loc.get('name', 'unknown')} missing keys: {missing}"
    
    def test_all_patterns_are_valid_regex(self):
        """All patterns should be valid regex."""
        for loc in VERSION_LOCATIONS:
            try:
                re.compile(loc["pattern"])
            except re.error as e:
                pytest.fail(f"Invalid regex in {loc['name']}: {e}")
    
    def test_replacement_functions_are_callable(self):
        """All replacement functions should be callable."""
        for loc in VERSION_LOCATIONS:
            assert callable(loc["replacement"]), f"Replacement in {loc['name']} is not callable"
    
    def test_replacement_functions_produce_valid_strings(self):
        """Replacement functions should return strings with version."""
        test_version = "9.9.9"
        for loc in VERSION_LOCATIONS:
            result = loc["replacement"](test_version)
            assert isinstance(result, str), f"Replacement in {loc['name']} didn't return string"
            assert test_version in result, f"Replacement in {loc['name']} doesn't include version"


class TestSyncManifest:
    """Tests for the main sync_manifest function."""
    
    def test_detects_out_of_sync_factory_version(self, tmp_path, monkeypatch):
        """Should detect when factory_version is out of sync."""
        # Setup temp directory with required files
        monkeypatch.chdir(tmp_path)
        
        # Create CHANGELOG.md
        changelog = tmp_path / "CHANGELOG.md"
        changelog.write_text("## [3.5.0] - 2026-01-31\n", encoding='utf-8')
        
        # Create knowledge directory and manifest
        knowledge_dir = tmp_path / "knowledge"
        knowledge_dir.mkdir()
        manifest = knowledge_dir / "manifest.json"
        manifest.write_text(json.dumps({
            "factory_version": "3.4.0",
            "files": {}
        }), encoding='utf-8')
        
        all_synced, changes = sync_manifest(dry_run=True)
        
        assert not all_synced
        assert any("factory_version" in c for c in changes)
    
    def test_reports_synced_when_all_match(self, tmp_path, monkeypatch):
        """Should report all synced when versions match."""
        monkeypatch.chdir(tmp_path)
        
        # Create CHANGELOG.md
        changelog = tmp_path / "CHANGELOG.md"
        changelog.write_text("## [3.4.0] - 2026-01-31\n", encoding='utf-8')
        
        # Create knowledge directory and manifest with matching version
        knowledge_dir = tmp_path / "knowledge"
        knowledge_dir.mkdir()
        manifest = knowledge_dir / "manifest.json"
        manifest.write_text(json.dumps({
            "factory_version": "3.4.0",
            "files": {}
        }), encoding='utf-8')
        
        all_synced, changes = sync_manifest(dry_run=True)
        
        # Only manifest.json matters in isolated test
        assert all_synced or all("factory_version" not in c for c in changes)


class TestIntegration:
    """Integration tests using actual project files."""
    
    @pytest.fixture
    def factory_root(self):
        """Get the factory root directory."""
        return Path(__file__).parent.parent.parent
    
    def test_changelog_exists_and_has_version(self, factory_root):
        """CHANGELOG.md should exist and have a valid version."""
        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(factory_root)
            version = get_changelog_version()
            assert version != "0.0.0", "CHANGELOG.md should have a version"
            assert re.match(r'\d+\.\d+\.\d+', version), f"Invalid version format: {version}"
        finally:
            os.chdir(original_cwd)
    
    def test_version_locations_files_exist(self, factory_root):
        """All files in VERSION_LOCATIONS should exist."""
        for loc in VERSION_LOCATIONS:
            filepath = factory_root / loc["file"]
            assert filepath.exists(), f"File {loc['file']} not found (expected by {loc['name']})"
    
    def test_current_state_is_synced(self, factory_root):
        """Current factory state should be version-synced."""
        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(factory_root)
            all_synced, changes = sync_manifest(dry_run=True)
            assert all_synced, f"Factory versions out of sync: {changes}"
        finally:
            os.chdir(original_cwd)
