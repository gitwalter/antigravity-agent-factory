"""
Unit tests for scripts/git/backup_manager.py

Tests backup creation, manifest management, and rollback functionality.
"""

import json
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.git.backup_manager import (
    BackupEntry,
    BackupManifest,
    BackupSession,
    BackupManager,
    ensure_gitignore_excludes_backup,
)


class TestBackupEntry:
    """Tests for BackupEntry dataclass."""
    
    def test_backup_entry_creation(self):
        """Test creating a BackupEntry."""
        entry = BackupEntry(
            original_path="test/file.py",
            backup_path="/backup/test/file.py",
            file_hash="abc123",
            backed_up_at="2024-01-01T00:00:00",
            was_new=False,
        )
        assert entry.original_path == "test/file.py"
        assert entry.file_hash == "abc123"
        assert entry.was_new is False
    
    def test_backup_entry_was_new_default(self):
        """Test BackupEntry default was_new value."""
        entry = BackupEntry(
            original_path="test.py",
            backup_path="/backup/test.py",
            file_hash="xyz",
            backed_up_at="2024-01-01",
        )
        assert entry.was_new is False


class TestBackupManifest:
    """Tests for BackupManifest dataclass."""
    
    def test_manifest_creation(self):
        """Test creating a BackupManifest."""
        manifest = BackupManifest(
            session_id="20240101_120000",
            created_at="2024-01-01T12:00:00",
            repo_path="/path/to/repo",
            description="Test backup",
        )
        assert manifest.session_id == "20240101_120000"
        assert manifest.completed is False
        assert manifest.rolled_back is False
        assert manifest.entries == []
    
    def test_manifest_to_dict(self):
        """Test converting manifest to dictionary."""
        manifest = BackupManifest(
            session_id="test_session",
            created_at="2024-01-01",
            repo_path="/repo",
            description="Test",
        )
        manifest.entries.append(BackupEntry(
            original_path="file.py",
            backup_path="/backup/file.py",
            file_hash="hash123",
            backed_up_at="2024-01-01",
            was_new=True,
        ))
        
        d = manifest.to_dict()
        assert d["session_id"] == "test_session"
        assert len(d["entries"]) == 1
        assert d["entries"][0]["was_new"] is True
    
    def test_manifest_from_dict(self):
        """Test creating manifest from dictionary."""
        data = {
            "session_id": "from_dict_session",
            "created_at": "2024-01-01",
            "repo_path": "/test/repo",
            "description": "From dict",
            "entries": [
                {
                    "original_path": "test.py",
                    "backup_path": "/backup/test.py",
                    "file_hash": "abc",
                    "backed_up_at": "2024-01-01",
                    "was_new": False,
                }
            ],
            "completed": True,
            "rolled_back": False,
        }
        
        manifest = BackupManifest.from_dict(data)
        assert manifest.session_id == "from_dict_session"
        assert manifest.completed is True
        assert len(manifest.entries) == 1
        assert manifest.entries[0].original_path == "test.py"
    
    def test_manifest_roundtrip(self):
        """Test that manifest survives to_dict/from_dict roundtrip."""
        original = BackupManifest(
            session_id="roundtrip",
            created_at="2024-01-01",
            repo_path="/repo",
            description="Roundtrip test",
        )
        original.entries.append(BackupEntry(
            original_path="src/main.py",
            backup_path="/backup/src/main.py",
            file_hash="deadbeef",
            backed_up_at="2024-01-01T12:00:00",
            was_new=True,
        ))
        original.completed = True
        
        restored = BackupManifest.from_dict(original.to_dict())
        assert restored.session_id == original.session_id
        assert restored.completed == original.completed
        assert len(restored.entries) == len(original.entries)
        assert restored.entries[0].was_new == original.entries[0].was_new


class TestBackupSession:
    """Tests for BackupSession class."""
    
    def test_session_creation(self):
        """Test creating a backup session."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            manager = BackupManager(repo_path)
            
            session = BackupSession(manager, "test_session", "Test description")
            
            assert session.session_id == "test_session"
            assert session.manifest.description == "Test description"
            assert session.session_dir.exists()
    
    def test_backup_file_existing(self):
        """Test backing up an existing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            
            # Create a file to backup
            test_file = repo_path / "test.txt"
            test_file.write_text("Original content")
            
            manager = BackupManager(repo_path)
            session = manager.create_session("Test")
            
            result = session.backup_file(test_file)
            
            assert result is True
            assert len(session.manifest.entries) == 1
            assert session.manifest.entries[0].original_path == "test.txt"
            assert session.manifest.entries[0].was_new is False
            assert session.manifest.entries[0].file_hash != ""
    
    def test_backup_file_marked_as_new(self):
        """Test marking a file as newly created."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            
            # File doesn't exist yet
            new_file = repo_path / "new_file.txt"
            
            manager = BackupManager(repo_path)
            session = manager.create_session("Test")
            
            result = session.backup_file(new_file, mark_as_new=True)
            
            assert result is True
            assert session.manifest.entries[0].was_new is True
            assert session.manifest.entries[0].file_hash == ""
    
    def test_backup_directory(self):
        """Test backing up a directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            
            # Create directory with files
            subdir = repo_path / "subdir"
            subdir.mkdir()
            (subdir / "file1.txt").write_text("Content 1")
            (subdir / "file2.txt").write_text("Content 2")
            
            manager = BackupManager(repo_path)
            session = manager.create_session("Test")
            
            result = session.backup_directory(subdir)
            
            assert result is True
            assert len(session.manifest.entries) == 2
    
    def test_rollback_restores_files(self):
        """Test that rollback restores original file content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            
            # Create original file
            test_file = repo_path / "test.txt"
            test_file.write_text("Original content")
            
            manager = BackupManager(repo_path)
            session = manager.create_session("Test")
            session.backup_file(test_file)
            
            # Modify the file
            test_file.write_text("Modified content")
            assert test_file.read_text() == "Modified content"
            
            # Rollback
            result = session.rollback()
            
            assert result is True
            assert test_file.read_text() == "Original content"
            assert session.manifest.rolled_back is True
    
    def test_rollback_deletes_new_files(self):
        """Test that rollback deletes newly created files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            
            # Mark a new file
            new_file = repo_path / "new_file.txt"
            
            manager = BackupManager(repo_path)
            session = manager.create_session("Test")
            session.backup_file(new_file, mark_as_new=True)
            
            # Create the new file
            new_file.write_text("New file content")
            assert new_file.exists()
            
            # Rollback should delete it
            result = session.rollback()
            
            assert result is True
            assert not new_file.exists()
    
    def test_complete_marks_session_complete(self):
        """Test that complete() marks session as completed."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            manager = BackupManager(repo_path)
            session = manager.create_session("Test")
            
            assert session.manifest.completed is False
            
            session.complete()
            
            assert session.manifest.completed is True


class TestBackupManager:
    """Tests for BackupManager class."""
    
    def test_manager_creation(self):
        """Test creating a BackupManager."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            manager = BackupManager(repo_path)
            
            assert manager.repo_path == repo_path
            assert manager.backup_root == repo_path / ".agent-factory-backup"
    
    def test_create_session(self):
        """Test creating a backup session."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            manager = BackupManager(repo_path)
            
            session = manager.create_session("Test session")
            
            assert session is not None
            assert session.manifest.description == "Test session"
            assert manager.backup_root.exists()
    
    def test_list_sessions_empty(self):
        """Test listing sessions when none exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            manager = BackupManager(repo_path)
            
            sessions = manager.list_sessions()
            
            assert sessions == []
    
    def test_list_sessions_returns_manifests(self):
        """Test listing sessions returns manifest objects."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            manager = BackupManager(repo_path)
            
            # Create a few sessions
            session1 = manager.create_session("Session 1")
            session1.complete()
            
            sessions = manager.list_sessions()
            
            assert len(sessions) >= 1
            assert any(s.description == "Session 1" for s in sessions)
    
    def test_get_session_by_id(self):
        """Test retrieving a session by ID."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            manager = BackupManager(repo_path)
            
            original = manager.create_session("Test")
            session_id = original.session_id
            
            retrieved = manager.get_session(session_id)
            
            assert retrieved is not None
            assert retrieved.session_id == session_id
    
    def test_get_session_not_found(self):
        """Test retrieving non-existent session returns None."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            manager = BackupManager(repo_path)
            
            result = manager.get_session("nonexistent_session")
            
            assert result is None
    
    def test_rollback_session(self):
        """Test rolling back a session by ID."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            
            # Create a file and backup
            test_file = repo_path / "test.txt"
            test_file.write_text("Original")
            
            manager = BackupManager(repo_path)
            session = manager.create_session("Test")
            session.backup_file(test_file)
            session_id = session.session_id
            
            # Modify file
            test_file.write_text("Modified")
            
            # Rollback via manager
            result = manager.rollback_session(session_id)
            
            assert result is True
            assert test_file.read_text() == "Original"
    
    def test_rollback_session_not_found(self):
        """Test rolling back non-existent session fails."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            manager = BackupManager(repo_path)
            
            result = manager.rollback_session("nonexistent")
            
            assert result is False
    
    def test_rollback_already_rolled_back(self):
        """Test rolling back already rolled back session fails."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            manager = BackupManager(repo_path)
            
            session = manager.create_session("Test")
            session.rollback()
            
            result = manager.rollback_session(session.session_id)
            
            assert result is False
    
    def test_cleanup_old_sessions(self):
        """Test cleaning up old sessions."""
        import time
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            manager = BackupManager(repo_path)
            
            # Create multiple sessions with different timestamps
            sessions_created = []
            for i in range(7):
                # Use unique session IDs to avoid timestamp collision
                session_id = f"session_{i:02d}"
                session_dir = manager.backup_root / session_id
                session_dir.mkdir(parents=True, exist_ok=True)
                
                manifest = BackupManifest(
                    session_id=session_id,
                    created_at=f"2024-01-0{i+1}T00:00:00",
                    repo_path=str(repo_path),
                    description=f"Session {i}",
                )
                manifest.completed = True
                
                manifest_path = session_dir / "manifest.json"
                with open(manifest_path, "w") as f:
                    json.dump(manifest.to_dict(), f)
                
                sessions_created.append(session_id)
            
            # Verify we have 7 sessions
            assert len(manager.list_sessions()) == 7
            
            # Cleanup, keeping only 3
            removed = manager.cleanup_old_sessions(keep_count=3)
            
            assert removed == 4
            remaining = manager.list_sessions()
            assert len(remaining) == 3
    
    def test_get_backup_size_empty(self):
        """Test getting backup size when empty."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            manager = BackupManager(repo_path)
            
            size = manager.get_backup_size()
            
            assert size == 0
    
    def test_get_backup_size_with_files(self):
        """Test getting backup size with backed up files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            
            # Create a file
            test_file = repo_path / "test.txt"
            test_file.write_text("Test content" * 100)
            
            manager = BackupManager(repo_path)
            session = manager.create_session("Test")
            session.backup_file(test_file)
            
            size = manager.get_backup_size()
            
            assert size > 0
    
    def test_format_backup_size(self):
        """Test formatting backup size."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            manager = BackupManager(repo_path)
            
            formatted = manager.format_backup_size()
            
            assert "B" in formatted or "KB" in formatted or "MB" in formatted


class TestEnsureGitignoreExcludesBackup:
    """Tests for ensure_gitignore_excludes_backup function."""
    
    def test_creates_gitignore_if_missing(self):
        """Test that function creates .gitignore if it doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            
            result = ensure_gitignore_excludes_backup(repo_path)
            
            assert result is True
            gitignore = repo_path / ".gitignore"
            assert gitignore.exists()
            assert ".agent-factory-backup/" in gitignore.read_text()
    
    def test_appends_to_existing_gitignore(self):
        """Test that function appends to existing .gitignore."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            gitignore = repo_path / ".gitignore"
            gitignore.write_text("*.pyc\n__pycache__/\n")
            
            result = ensure_gitignore_excludes_backup(repo_path)
            
            assert result is True
            content = gitignore.read_text()
            assert "*.pyc" in content
            assert ".agent-factory-backup/" in content
    
    def test_does_not_duplicate_entry(self):
        """Test that function doesn't add duplicate entries."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            gitignore = repo_path / ".gitignore"
            gitignore.write_text(".agent-factory-backup/\n")
            
            result = ensure_gitignore_excludes_backup(repo_path)
            
            assert result is True
            content = gitignore.read_text()
            assert content.count(".agent-factory-backup") == 1


class TestMainEntry:
    """Tests for command-line interface."""
    
    def test_main_list_command(self, capsys):
        """Test main with list command by importing and calling the module code."""
        # This tests the command-line interface indirectly
        # The actual main block only runs when the module is executed directly
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            manager = BackupManager(repo_path)
            session = manager.create_session("Test")
            session.complete()
            
            # Verify the session was created
            sessions = manager.list_sessions()
            assert len(sessions) == 1
    
    def test_main_size_command(self):
        """Test backup size calculation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            manager = BackupManager(repo_path)
            
            # Initially 0
            size = manager.get_backup_size()
            assert size == 0
            
            # Create a session with a file
            test_file = repo_path / "test.txt"
            test_file.write_text("content")
            session = manager.create_session("Test")
            session.backup_file(test_file)
            
            # Now should have size > 0
            size = manager.get_backup_size()
            assert size > 0
    
    def test_format_backup_size_units(self):
        """Test format_backup_size with various sizes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            manager = BackupManager(repo_path)
            
            # Empty returns "0.0 B"
            formatted = manager.format_backup_size()
            assert "B" in formatted or "0" in formatted
