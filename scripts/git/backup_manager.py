#!/usr/bin/env python3
"""
Antigravity Agent Factory - Backup Manager
Handles backup creation, manifest tracking, and rollback functionality
for the onboarding process.

Usage:
    from scripts.git.backup_manager import BackupManager
    
    manager = BackupManager(repo_path)
    session = manager.create_session()
    session.backup_file(file_path)
    # ... make changes ...
    session.rollback()  # If needed

Author: Antigravity Agent Factory
Version: 1.0.0
"""

import json
import shutil
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class BackupEntry:
    """Record of a single backed up file.
    
    Attributes:
        original_path: Original path of the file (relative to repo).
        backup_path: Path to the backup copy.
        file_hash: MD5 hash of the original content.
        backed_up_at: Timestamp when backup was created.
        was_new: Whether this was a new file (didn't exist before).
    """
    original_path: str
    backup_path: str
    file_hash: str
    backed_up_at: str
    was_new: bool = False


@dataclass
class BackupManifest:
    """Manifest for a backup session.
    
    Attributes:
        session_id: Unique identifier for this backup session.
        created_at: Timestamp when session was created.
        repo_path: Path to the repository.
        description: Human-readable description of the operation.
        entries: List of backed up files.
        completed: Whether the operation completed successfully.
        rolled_back: Whether the operation was rolled back.
    """
    session_id: str
    created_at: str
    repo_path: str
    description: str = ""
    entries: List[BackupEntry] = field(default_factory=list)
    completed: bool = False
    rolled_back: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert manifest to dictionary for JSON serialization.
        
        Returns:
            Dictionary representation of the manifest.
        """
        return {
            "session_id": self.session_id,
            "created_at": self.created_at,
            "repo_path": self.repo_path,
            "description": self.description,
            "entries": [
                {
                    "original_path": e.original_path,
                    "backup_path": e.backup_path,
                    "file_hash": e.file_hash,
                    "backed_up_at": e.backed_up_at,
                    "was_new": e.was_new,
                }
                for e in self.entries
            ],
            "completed": self.completed,
            "rolled_back": self.rolled_back,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BackupManifest':
        """Create manifest from dictionary.
        
        Args:
            data: Dictionary representation.
            
        Returns:
            BackupManifest instance.
        """
        manifest = cls(
            session_id=data["session_id"],
            created_at=data["created_at"],
            repo_path=data["repo_path"],
            description=data.get("description", ""),
            completed=data.get("completed", False),
            rolled_back=data.get("rolled_back", False),
        )
        
        for entry_data in data.get("entries", []):
            manifest.entries.append(BackupEntry(
                original_path=entry_data["original_path"],
                backup_path=entry_data["backup_path"],
                file_hash=entry_data["file_hash"],
                backed_up_at=entry_data["backed_up_at"],
                was_new=entry_data.get("was_new", False),
            ))
        
        return manifest


class BackupSession:
    """Active backup session for tracking file modifications.
    
    This class manages the backup of files during an onboarding operation,
    allowing for rollback if something goes wrong.
    
    Attributes:
        manager: Parent BackupManager.
        manifest: Session manifest tracking all backups.
        session_dir: Directory containing backups for this session.
    """
    
    def __init__(
        self,
        manager: 'BackupManager',
        session_id: str,
        description: str = ""
    ):
        """Initialize a backup session.
        
        Args:
            manager: Parent BackupManager.
            session_id: Unique session identifier.
            description: Human-readable description of the operation.
        """
        self.manager = manager
        self.session_id = session_id
        self.session_dir = manager.backup_root / session_id
        self.session_dir.mkdir(parents=True, exist_ok=True)
        
        self.manifest = BackupManifest(
            session_id=session_id,
            created_at=datetime.now().isoformat(),
            repo_path=str(manager.repo_path),
            description=description,
        )
        
        self._save_manifest()
    
    def backup_file(self, file_path: Path, mark_as_new: bool = False) -> bool:
        """Create a backup of a file before modifying it.
        
        Args:
            file_path: Path to the file to backup.
            mark_as_new: If True, marks file as newly created (for deletion on rollback).
            
        Returns:
            True if backup was successful, False otherwise.
        """
        # Calculate relative path
        try:
            relative_path = file_path.relative_to(self.manager.repo_path)
        except ValueError:
            relative_path = Path(file_path.name)
        
        # Create backup directory structure
        backup_path = self.session_dir / relative_path
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Calculate hash and copy if file exists
        file_hash = ""
        if file_path.exists() and not mark_as_new:
            try:
                import hashlib
                content = file_path.read_bytes()
                file_hash = hashlib.md5(content).hexdigest()
                shutil.copy2(file_path, backup_path)
            except Exception as e:
                print(f"Warning: Could not backup {file_path}: {e}")
                return False
        
        # Create entry
        entry = BackupEntry(
            original_path=str(relative_path),
            backup_path=str(backup_path),
            file_hash=file_hash,
            backed_up_at=datetime.now().isoformat(),
            was_new=mark_as_new,
        )
        
        self.manifest.entries.append(entry)
        self._save_manifest()
        
        return True
    
    def backup_directory(self, dir_path: Path, mark_as_new: bool = False) -> bool:
        """Backup all files in a directory.
        
        Args:
            dir_path: Path to the directory to backup.
            mark_as_new: If True, marks files as newly created.
            
        Returns:
            True if all backups were successful.
        """
        if not dir_path.exists():
            return True
        
        success = True
        for file_path in dir_path.rglob("*"):
            if file_path.is_file():
                if not self.backup_file(file_path, mark_as_new):
                    success = False
        
        return success
    
    def rollback(self) -> bool:
        """Rollback all changes made in this session.
        
        Returns:
            True if rollback was successful, False otherwise.
        """
        success = True
        
        for entry in reversed(self.manifest.entries):
            original_path = self.manager.repo_path / entry.original_path
            backup_path = Path(entry.backup_path)
            
            try:
                if entry.was_new:
                    # Delete newly created files
                    if original_path.exists():
                        original_path.unlink()
                        # Clean up empty parent directories
                        self._cleanup_empty_dirs(original_path.parent)
                else:
                    # Restore from backup
                    if backup_path.exists():
                        original_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(backup_path, original_path)
            except Exception as e:
                print(f"Warning: Could not rollback {entry.original_path}: {e}")
                success = False
        
        self.manifest.rolled_back = True
        self._save_manifest()
        
        return success
    
    def complete(self) -> None:
        """Mark the session as successfully completed."""
        self.manifest.completed = True
        self._save_manifest()
    
    def _save_manifest(self) -> None:
        """Save the manifest to disk."""
        manifest_path = self.session_dir / "manifest.json"
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(self.manifest.to_dict(), f, indent=2)
    
    def _cleanup_empty_dirs(self, dir_path: Path) -> None:
        """Remove empty directories up to the repo root.
        
        Args:
            dir_path: Starting directory to check.
        """
        try:
            while dir_path != self.manager.repo_path:
                if dir_path.exists() and not any(dir_path.iterdir()):
                    dir_path.rmdir()
                    dir_path = dir_path.parent
                else:
                    break
        except Exception:
            pass  # Ignore cleanup errors


class BackupManager:
    """Manager for backup operations during onboarding.
    
    This class handles the creation and management of backup sessions,
    allowing for safe modification of existing repository files with
    rollback capability.
    
    Attributes:
        repo_path: Path to the repository.
        backup_root: Root directory for all backups.
    
    Example:
        >>> manager = BackupManager(Path("C:/Projects/my-repo"))
        >>> session = manager.create_session("Onboarding with python-fastapi blueprint")
        >>> session.backup_file(Path("C:/Projects/my-repo/.agentrules"))        >>> # ... modify files ...
        >>> session.complete()  # Or session.rollback() if needed
    """
    
    BACKUP_DIR_NAME = ".agent-factory-backup"    
    def __init__(self, repo_path: Path):
        """Initialize the backup manager.
        
        Args:
            repo_path: Path to the repository.
        """
        self.repo_path = Path(repo_path)
        self.backup_root = self.repo_path / self.BACKUP_DIR_NAME
    
    def create_session(self, description: str = "") -> BackupSession:
        """Create a new backup session.
        
        Args:
            description: Human-readable description of the operation.
            
        Returns:
            New BackupSession instance.
        """
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        return BackupSession(self, session_id, description)
    
    def list_sessions(self) -> List[BackupManifest]:
        """List all backup sessions.
        
        Returns:
            List of BackupManifest for all sessions.
        """
        sessions = []
        
        if not self.backup_root.exists():
            return sessions
        
        for session_dir in sorted(self.backup_root.iterdir()):
            if session_dir.is_dir():
                manifest_path = session_dir / "manifest.json"
                if manifest_path.exists():
                    try:
                        with open(manifest_path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                        sessions.append(BackupManifest.from_dict(data))
                    except Exception as e:
                        print(f"Warning: Could not load manifest from {session_dir}: {e}")
        
        return sessions
    
    def get_session(self, session_id: str) -> Optional[BackupSession]:
        """Get an existing backup session by ID.
        
        Args:
            session_id: Session identifier.
            
        Returns:
            BackupSession if found, None otherwise.
        """
        session_dir = self.backup_root / session_id
        manifest_path = session_dir / "manifest.json"
        
        if not manifest_path.exists():
            return None
        
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            session = BackupSession(self, session_id)
            session.manifest = BackupManifest.from_dict(data)
            return session
        except Exception:
            return None
    
    def rollback_session(self, session_id: str) -> bool:
        """Rollback a specific backup session.
        
        Args:
            session_id: Session identifier to rollback.
            
        Returns:
            True if rollback was successful, False otherwise.
        """
        session = self.get_session(session_id)
        if session is None:
            print(f"Session not found: {session_id}")
            return False
        
        if session.manifest.rolled_back:
            print(f"Session already rolled back: {session_id}")
            return False
        
        return session.rollback()
    
    def cleanup_old_sessions(self, keep_count: int = 5) -> int:
        """Remove old backup sessions, keeping the most recent ones.
        
        Args:
            keep_count: Number of recent sessions to keep.
            
        Returns:
            Number of sessions removed.
        """
        sessions = self.list_sessions()
        
        # Sort by creation time (newest first)
        sessions.sort(key=lambda s: s.created_at, reverse=True)
        
        removed = 0
        for session in sessions[keep_count:]:
            session_dir = self.backup_root / session.session_id
            try:
                shutil.rmtree(session_dir)
                removed += 1
            except Exception as e:
                print(f"Warning: Could not remove session {session.session_id}: {e}")
        
        return removed
    
    def get_backup_size(self) -> int:
        """Calculate total size of all backups in bytes.
        
        Returns:
            Total size in bytes.
        """
        if not self.backup_root.exists():
            return 0
        
        total = 0
        for file_path in self.backup_root.rglob("*"):
            if file_path.is_file():
                total += file_path.stat().st_size
        
        return total
    
    def format_backup_size(self) -> str:
        """Get human-readable backup size.
        
        Returns:
            Formatted size string (e.g., "1.5 MB").
        """
        size = self.get_backup_size()
        
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        
        return f"{size:.1f} TB"


def ensure_gitignore_excludes_backup(repo_path: Path) -> bool:
    """Ensure .gitignore excludes the backup directory.
    
    Args:
        repo_path: Path to the repository.
        
    Returns:
        True if .gitignore was updated or already excludes backups.
    """
    gitignore_path = repo_path / ".gitignore"
    backup_pattern = BackupManager.BACKUP_DIR_NAME + "/"
    
    if gitignore_path.exists():
        content = gitignore_path.read_text(encoding="utf-8")
        if backup_pattern in content or BackupManager.BACKUP_DIR_NAME in content:
            return True
    else:
        content = ""
    
    # Add the pattern
    if not content.endswith("\n") and content:
        content += "\n"
    
    content += f"\n# Antigravity Agent Factory backup directory\n{backup_pattern}\n"    
    try:
        gitignore_path.write_text(content, encoding="utf-8")
        return True
    except Exception as e:
        print(f"Warning: Could not update .gitignore: {e}")
        return False


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python backup_manager.py <repository_path> [command]")
        print("Commands:")
        print("  list     - List all backup sessions")
        print("  size     - Show total backup size")
        print("  cleanup  - Remove old backup sessions")
        sys.exit(1)
    
    repo_path = Path(sys.argv[1])
    command = sys.argv[2] if len(sys.argv) > 2 else "list"
    
    manager = BackupManager(repo_path)
    
    if command == "list":
        sessions = manager.list_sessions()
        if not sessions:
            print("No backup sessions found.")
        else:
            print(f"Found {len(sessions)} backup session(s):\n")
            for session in sessions:
                status = "rolled back" if session.rolled_back else (
                    "completed" if session.completed else "incomplete"
                )
                print(f"  {session.session_id}")
                print(f"    Created: {session.created_at}")
                print(f"    Status: {status}")
                print(f"    Files: {len(session.entries)}")
                if session.description:
                    print(f"    Description: {session.description}")
                print()
    
    elif command == "size":
        print(f"Total backup size: {manager.format_backup_size()}")
    
    elif command == "cleanup":
        removed = manager.cleanup_old_sessions()
        print(f"Removed {removed} old backup session(s).")
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
