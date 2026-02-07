#!/usr/bin/env python3
"""
Tests for scripts/validation/sync_knowledge_counts.py

Ensures the knowledge count sync script correctly:
- Counts knowledge files in knowledge/ directory
- Extracts counts from manifest.json and KNOWLEDGE_FILES.md
- Updates files when counts differ
"""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch
import pytest

# Import the module under test
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.validation.sync_knowledge_counts import (
    count_knowledge_files,
    get_manifest_count,
    get_docs_count,
    update_manifest,
    update_docs,
    sync_knowledge_counts,
)


class TestCountKnowledgeFiles:
    """Tests for counting knowledge files."""
    
    def test_counts_json_files(self, tmp_path, monkeypatch):
        """Should count all .json files in knowledge/."""
        monkeypatch.chdir(tmp_path)
        
        knowledge_dir = tmp_path / "knowledge"
        knowledge_dir.mkdir()
        
        # Create some JSON files
        (knowledge_dir / "file1.json").write_text("{}", encoding='utf-8')
        (knowledge_dir / "file2.json").write_text("{}", encoding='utf-8')
        (knowledge_dir / "file3.json").write_text("{}", encoding='utf-8')
        
        count = count_knowledge_files()
        assert count == 3
    
    def test_excludes_underscore_prefixed(self, tmp_path, monkeypatch):
        """Should exclude files starting with underscore."""
        monkeypatch.chdir(tmp_path)
        
        knowledge_dir = tmp_path / "knowledge"
        knowledge_dir.mkdir()
        
        (knowledge_dir / "file1.json").write_text("{}", encoding='utf-8')
        (knowledge_dir / "_schema.json").write_text("{}", encoding='utf-8')
        
        count = count_knowledge_files()
        assert count == 1
    
    def test_excludes_subdirectories(self, tmp_path, monkeypatch):
        """Should not count files in subdirectories."""
        monkeypatch.chdir(tmp_path)
        
        knowledge_dir = tmp_path / "knowledge"
        knowledge_dir.mkdir()
        subdir = knowledge_dir / "schemas"
        subdir.mkdir()
        
        (knowledge_dir / "file1.json").write_text("{}", encoding='utf-8')
        (subdir / "file2.json").write_text("{}", encoding='utf-8')
        
        count = count_knowledge_files()
        assert count == 1
    
    def test_returns_zero_for_missing_dir(self, tmp_path, monkeypatch):
        """Should return 0 if knowledge/ doesn't exist."""
        monkeypatch.chdir(tmp_path)
        
        count = count_knowledge_files()
        assert count == 0


class TestGetManifestCount:
    """Tests for extracting count from manifest.json."""
    
    def test_extracts_total_files(self, tmp_path, monkeypatch):
        """Should extract statistics.total_files from manifest."""
        monkeypatch.chdir(tmp_path)
        
        knowledge_dir = tmp_path / "knowledge"
        knowledge_dir.mkdir()
        
        manifest = knowledge_dir / "manifest.json"
        manifest.write_text(json.dumps({
            "statistics": {"total_files": 42}
        }), encoding='utf-8')
        
        count = get_manifest_count()
        assert count == 42
    
    def test_returns_zero_for_missing_manifest(self, tmp_path, monkeypatch):
        """Should return 0 if manifest doesn't exist."""
        monkeypatch.chdir(tmp_path)
        
        count = get_manifest_count()
        assert count == 0
    
    def test_returns_zero_for_missing_statistics(self, tmp_path, monkeypatch):
        """Should return 0 if statistics key is missing."""
        monkeypatch.chdir(tmp_path)
        
        knowledge_dir = tmp_path / "knowledge"
        knowledge_dir.mkdir()
        
        manifest = knowledge_dir / "manifest.json"
        manifest.write_text('{"files": {}}', encoding='utf-8')
        
        count = get_manifest_count()
        assert count == 0


class TestGetDocsCount:
    """Tests for extracting count from KNOWLEDGE_FILES.md."""
    
    def test_extracts_count_from_docs(self, tmp_path, monkeypatch):
        """Should extract count from KNOWLEDGE_FILES.md."""
        monkeypatch.chdir(tmp_path)
        
        docs_dir = tmp_path / "docs" / "reference"
        docs_dir.mkdir(parents=True)
        
        knowledge_md = docs_dir / "KNOWLEDGE_FILES.md"
        knowledge_md.write_text(
            "The factory currently includes **72 knowledge files** covering...",
            encoding='utf-8'
        )
        
        count = get_docs_count()
        assert count == 72
    
    def test_returns_zero_for_missing_file(self, tmp_path, monkeypatch):
        """Should return 0 if file doesn't exist."""
        monkeypatch.chdir(tmp_path)
        
        count = get_docs_count()
        assert count == 0
    
    def test_returns_zero_for_no_match(self, tmp_path, monkeypatch):
        """Should return 0 if pattern doesn't match."""
        monkeypatch.chdir(tmp_path)
        
        docs_dir = tmp_path / "docs" / "reference"
        docs_dir.mkdir(parents=True)
        
        knowledge_md = docs_dir / "KNOWLEDGE_FILES.md"
        knowledge_md.write_text("No count here", encoding='utf-8')
        
        count = get_docs_count()
        assert count == 0


class TestUpdateManifest:
    """Tests for updating manifest.json."""
    
    def test_dry_run_does_not_modify(self, tmp_path, monkeypatch):
        """Should not modify file when dry_run=True."""
        monkeypatch.chdir(tmp_path)
        
        knowledge_dir = tmp_path / "knowledge"
        knowledge_dir.mkdir()
        
        manifest = knowledge_dir / "manifest.json"
        original = json.dumps({"statistics": {"total_files": 10}})
        manifest.write_text(original, encoding='utf-8')
        
        result = update_manifest(20, dry_run=True)
        
        assert result is True
        assert manifest.read_text(encoding='utf-8') == original
    
    def test_updates_count(self, tmp_path, monkeypatch):
        """Should update count when dry_run=False."""
        monkeypatch.chdir(tmp_path)
        
        knowledge_dir = tmp_path / "knowledge"
        knowledge_dir.mkdir()
        
        manifest = knowledge_dir / "manifest.json"
        manifest.write_text(json.dumps({"statistics": {"total_files": 10}}), encoding='utf-8')
        
        result = update_manifest(20, dry_run=False)
        
        assert result is True
        data = json.loads(manifest.read_text(encoding='utf-8'))
        assert data["statistics"]["total_files"] == 20
    
    def test_returns_false_when_synced(self, tmp_path, monkeypatch):
        """Should return False when counts match."""
        monkeypatch.chdir(tmp_path)
        
        knowledge_dir = tmp_path / "knowledge"
        knowledge_dir.mkdir()
        
        manifest = knowledge_dir / "manifest.json"
        manifest.write_text(json.dumps({"statistics": {"total_files": 10}}), encoding='utf-8')
        
        result = update_manifest(10, dry_run=True)
        
        assert result is False


class TestUpdateDocs:
    """Tests for updating KNOWLEDGE_FILES.md."""
    
    def test_dry_run_does_not_modify(self, tmp_path, monkeypatch):
        """Should not modify file when dry_run=True."""
        monkeypatch.chdir(tmp_path)
        
        docs_dir = tmp_path / "docs" / "reference"
        docs_dir.mkdir(parents=True)
        
        knowledge_md = docs_dir / "KNOWLEDGE_FILES.md"
        original = "The factory includes **10 knowledge files**."
        knowledge_md.write_text(original, encoding='utf-8')
        
        result = update_docs(20, dry_run=True)
        
        assert result is True
        assert knowledge_md.read_text(encoding='utf-8') == original
    
    def test_updates_count(self, tmp_path, monkeypatch):
        """Should update count when dry_run=False."""
        monkeypatch.chdir(tmp_path)
        
        docs_dir = tmp_path / "docs" / "reference"
        docs_dir.mkdir(parents=True)
        
        knowledge_md = docs_dir / "KNOWLEDGE_FILES.md"
        knowledge_md.write_text("The factory includes **10 knowledge files**.", encoding='utf-8')
        
        result = update_docs(20, dry_run=False)
        
        assert result is True
        assert "**20 knowledge files**" in knowledge_md.read_text(encoding='utf-8')


class TestSyncKnowledgeCounts:
    """Tests for the main sync function."""
    
    def test_detects_out_of_sync(self, tmp_path, monkeypatch):
        """Should detect when counts are out of sync."""
        monkeypatch.chdir(tmp_path)
        
        # Create knowledge dir with files
        knowledge_dir = tmp_path / "knowledge"
        knowledge_dir.mkdir()
        (knowledge_dir / "file1.json").write_text("{}", encoding='utf-8')
        (knowledge_dir / "file2.json").write_text("{}", encoding='utf-8')
        
        # Create manifest with wrong count
        manifest = knowledge_dir / "manifest.json"
        manifest.write_text(json.dumps({"statistics": {"total_files": 10}}), encoding='utf-8')
        
        # Create docs with wrong count
        docs_dir = tmp_path / "docs" / "reference"
        docs_dir.mkdir(parents=True)
        knowledge_md = docs_dir / "KNOWLEDGE_FILES.md"
        knowledge_md.write_text("includes **10 knowledge files**", encoding='utf-8')
        
        all_synced, changes = sync_knowledge_counts(dry_run=True)
        
        assert not all_synced
        assert len(changes) == 2
    
    def test_reports_synced_when_matched(self, tmp_path, monkeypatch):
        """Should report synced when all counts match."""
        monkeypatch.chdir(tmp_path)
        
        # Create knowledge dir with files
        # Note: manifest.json is excluded from count (it's a meta-file)
        knowledge_dir = tmp_path / "knowledge"
        knowledge_dir.mkdir()
        (knowledge_dir / "file1.json").write_text("{}", encoding='utf-8')
        (knowledge_dir / "file2.json").write_text("{}", encoding='utf-8')
        
        # Create manifest with correct count (2 = file1.json + file2.json, NOT including manifest.json)
        manifest = knowledge_dir / "manifest.json"
        manifest.write_text(json.dumps({"statistics": {"total_files": 2}}), encoding='utf-8')
        
        # Create docs with correct count
        docs_dir = tmp_path / "docs" / "reference"
        docs_dir.mkdir(parents=True)
        knowledge_md = docs_dir / "KNOWLEDGE_FILES.md"
        knowledge_md.write_text("includes **2 knowledge files**", encoding='utf-8')
        
        all_synced, changes = sync_knowledge_counts(dry_run=True)
        
        assert all_synced
        assert len(changes) == 0


class TestIntegration:
    """Integration tests using actual project files."""
    
    @pytest.fixture
    def factory_root(self):
        """Get the factory root directory."""
        return Path(__file__).parent.parent.parent
    
    def test_knowledge_dir_exists(self, factory_root):
        """knowledge/ directory should exist."""
        assert (factory_root / "knowledge").exists()
    
    def test_manifest_exists(self, factory_root):
        """knowledge/manifest.json should exist."""
        assert (factory_root / "knowledge" / "manifest.json").exists()
    
    def test_knowledge_files_md_exists(self, factory_root):
        """docs/reference/KNOWLEDGE_FILES.md should exist."""
        assert (factory_root / "docs" / "reference" / "KNOWLEDGE_FILES.md").exists()
    
    def test_counts_are_currently_synced(self, factory_root):
        """Current knowledge counts should be in sync."""
        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(factory_root)
            
            all_synced, changes = sync_knowledge_counts(dry_run=True)
            
            assert all_synced, f"Knowledge counts out of sync: {changes}"
        finally:
            os.chdir(original_cwd)
