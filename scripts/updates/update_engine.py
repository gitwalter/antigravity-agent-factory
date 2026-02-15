"""
Update Engine for Knowledge Evolution

This module provides the core logic for processing and applying knowledge updates.
It handles merging updates into existing knowledge files, managing backups,
validating changes, and coordinating the update workflow.

Features:
    - Backup creation and management
    - Merge strategies (conservative, balanced, aggressive)
    - Schema validation
    - Conflict detection and resolution
    - Rollback support
    - Update history tracking

Design Patterns:
    - Strategy: Different merge strategies
    - Command: Reversible update operations
    - Template Method: Update workflow with customizable steps

Author: Antigravity Agent Factory
Version: 1.0.0
"""

import json
import shutil
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import copy


class MergeStrategy(Enum):
    """Strategies for merging knowledge updates.

    Each strategy defines how conflicts between existing and new content
    are resolved.
    """

    CONSERVATIVE = "conservative"  # Only add new, never modify existing
    BALANCED = "balanced"  # Add and update, preserve user customizations
    AGGRESSIVE = "aggressive"  # Full replacement with new content


@dataclass
class UpdateOperation:
    """Represents a single update operation.

    Attributes:
        target_file: Knowledge file being updated
        operation_type: Type of operation (add, modify, remove)
        path: JSON path to the affected element
        old_value: Previous value (for modify/remove)
        new_value: New value (for add/modify)
        timestamp: When operation was performed
    """

    target_file: str
    operation_type: str  # "add", "modify", "remove"
    path: str
    old_value: Optional[Any] = None
    new_value: Optional[Any] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "target_file": self.target_file,
            "operation_type": self.operation_type,
            "path": self.path,
            "old_value": self.old_value,
            "new_value": self.new_value,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class UpdateResult:
    """Result of applying an update.

    Attributes:
        success: Whether update was successful
        target_file: File that was updated
        old_version: Previous version
        new_version: New version
        operations: List of operations performed
        backup_path: Path to backup file
        errors: Any errors encountered
    """

    success: bool
    target_file: str
    old_version: Optional[str] = None
    new_version: Optional[str] = None
    operations: List[UpdateOperation] = field(default_factory=list)
    backup_path: Optional[Path] = None
    errors: List[str] = field(default_factory=list)


@dataclass
class BatchUpdateResult:
    """Result of applying multiple updates.

    Attributes:
        success: Whether all updates succeeded
        results: Individual update results
        total_applied: Number of updates applied
        total_failed: Number of updates that failed
        batch_id: Unique identifier for this batch
        timestamp: When batch was processed
    """

    success: bool
    results: List[UpdateResult]
    total_applied: int = 0
    total_failed: int = 0
    batch_id: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self):
        if not self.batch_id:
            self.batch_id = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        self.total_applied = sum(1 for r in self.results if r.success)
        self.total_failed = sum(1 for r in self.results if not r.success)


class UpdateEngine:
    """Engine for processing and applying knowledge updates.

    This class handles the complete update workflow including:
    - Creating backups before updates
    - Merging new content with existing knowledge
    - Validating changes against schemas
    - Managing update history
    - Supporting rollbacks

    Example:
        engine = UpdateEngine(knowledge_dir, backup_dir)
        result = engine.apply_update(update, MergeStrategy.BALANCED)
        if not result.success:
            engine.rollback(result.backup_path)
    """

    def __init__(
        self,
        knowledge_dir: Path,
        backup_dir: Optional[Path] = None,
        max_backups: int = 10,
    ):
        """Initialize the update engine.

        Args:
            knowledge_dir: Directory containing knowledge files
            backup_dir: Directory for backups (defaults to knowledge_dir/backups)
            max_backups: Maximum number of backups to retain per file
        """
        self.knowledge_dir = Path(knowledge_dir)
        self.backup_dir = (
            Path(backup_dir) if backup_dir else self.knowledge_dir / "backups"
        )
        self.max_backups = max_backups
        self._history: List[BatchUpdateResult] = []

        # Ensure directories exist
        self.knowledge_dir.mkdir(parents=True, exist_ok=True)
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def apply_update(
        self,
        update: "KnowledgeUpdate",
        strategy: MergeStrategy = MergeStrategy.BALANCED,
        create_backup: bool = True,
    ) -> UpdateResult:
        """Apply a single knowledge update.

        Args:
            update: The update to apply
            strategy: Merge strategy to use
            create_backup: Whether to backup before updating

        Returns:
            UpdateResult with operation details
        """

        target_path = self.knowledge_dir / update.target_file
        result = UpdateResult(
            success=False,
            target_file=update.target_file,
            new_version=update.new_version,
        )

        try:
            # Load existing content
            existing_content = {}
            if target_path.exists():
                with open(target_path, "r", encoding="utf-8") as f:
                    existing_content = json.load(f)
                result.old_version = existing_content.get("version")

            # Create backup
            if create_backup and target_path.exists():
                result.backup_path = self._create_backup(target_path)

            # Merge content
            merged_content, operations = self._merge_content(
                existing_content, update, strategy
            )
            result.operations = operations

            # Validate merged content
            validation_errors = self._validate_content(merged_content)
            if validation_errors:
                result.errors = validation_errors
                return result

            # Write updated content
            with open(target_path, "w", encoding="utf-8") as f:
                json.dump(merged_content, f, indent=2, ensure_ascii=False)

            result.success = True

        except Exception as e:
            result.errors.append(str(e))
            # Attempt rollback if we have a backup
            if result.backup_path:
                self._restore_backup(result.backup_path, target_path)

        return result

    def apply_batch(
        self,
        updates: List["KnowledgeUpdate"],
        strategy: MergeStrategy = MergeStrategy.BALANCED,
    ) -> BatchUpdateResult:
        """Apply multiple updates as a batch.

        Args:
            updates: List of updates to apply
            strategy: Merge strategy to use

        Returns:
            BatchUpdateResult with all operation details
        """
        results: List[UpdateResult] = []

        for update in updates:
            result = self.apply_update(update, strategy)
            results.append(result)

        batch_result = BatchUpdateResult(
            success=all(r.success for r in results),
            results=results,
        )

        self._history.append(batch_result)
        return batch_result

    def _create_backup(self, file_path: Path) -> Path:
        """Create a backup of a knowledge file.

        Args:
            file_path: Path to the file to backup

        Returns:
            Path to the backup file
        """
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.stem}.{timestamp}{file_path.suffix}"
        backup_path = self.backup_dir / backup_name

        shutil.copy2(file_path, backup_path)

        # Rotate old backups
        self._rotate_backups(file_path.stem)

        return backup_path

    def _rotate_backups(self, file_stem: str) -> None:
        """Remove old backups exceeding max_backups limit.

        Args:
            file_stem: Base name of the file (without extension)
        """
        # Find all backups for this file
        backups = list(self.backup_dir.glob(f"{file_stem}.*"))
        backups.sort(key=lambda p: p.stat().st_mtime, reverse=True)

        # Remove old backups
        for old_backup in backups[self.max_backups :]:
            old_backup.unlink()

    def _restore_backup(self, backup_path: Path, target_path: Path) -> bool:
        """Restore a file from backup.

        Args:
            backup_path: Path to the backup file
            target_path: Path to restore to

        Returns:
            True if restore was successful
        """
        try:
            shutil.copy2(backup_path, target_path)
            return True
        except Exception:
            return False

    def _merge_content(
        self,
        existing: Dict[str, Any],
        update: "KnowledgeUpdate",
        strategy: MergeStrategy,
    ) -> Tuple[Dict[str, Any], List[UpdateOperation]]:
        """Merge update content with existing content.

        Args:
            existing: Existing knowledge content
            update: Update to apply
            strategy: Merge strategy

        Returns:
            Tuple of (merged_content, operations)
        """

        operations: List[UpdateOperation] = []
        merged = copy.deepcopy(existing)

        # Update version
        if "version" in merged:
            operations.append(
                UpdateOperation(
                    target_file=update.target_file,
                    operation_type="modify",
                    path="version",
                    old_value=merged.get("version"),
                    new_value=update.new_version,
                )
            )
        merged["version"] = update.new_version

        # Update metadata
        if "metadata" not in merged:
            merged["metadata"] = {}
        merged["metadata"]["updated"] = datetime.now(timezone.utc).isoformat()
        merged["metadata"]["checksum"] = update.checksum

        # Add source information
        if "sources" not in merged:
            merged["sources"] = []
        merged["sources"].append(
            {
                "type": update.source.adapter_type,
                "identifier": update.source.identifier,
                "version": update.source.version,
                "url": update.source.url,
                "fetched_at": update.source.fetched_at.isoformat(),
            }
        )

        # Apply changes based on strategy
        if update.proposed_content:
            if strategy == MergeStrategy.AGGRESSIVE:
                # Full replacement
                for key, value in update.proposed_content.items():
                    if key not in ["$schema", "version", "metadata"]:
                        merged[key] = value
                        operations.append(
                            UpdateOperation(
                                target_file=update.target_file,
                                operation_type="modify",
                                path=key,
                                new_value=value,
                            )
                        )

            elif strategy in [MergeStrategy.BALANCED, MergeStrategy.CONSERVATIVE]:
                # Add and update (Balanced) or only add (Conservative)
                merged = self._deep_merge(
                    merged,
                    update.proposed_content,
                    operations,
                    update.target_file,
                    strategy=strategy,
                )

        # Add changelog entry
        if "changelog" not in merged:
            merged["changelog"] = []

        changelog_entry = {
            "version": update.new_version,
            "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "changes": [
                {
                    "type": c.change_type.value,
                    "description": c.description,
                }
                for c in update.changes
            ],
            "source": update.source.identifier,
        }
        merged["changelog"].insert(0, changelog_entry)

        return merged, operations

    def _deep_merge(
        self,
        base: Dict[str, Any],
        updates: Dict[str, Any],
        operations: List[UpdateOperation],
        target_file: str,
        path: str = "",
        strategy: MergeStrategy = MergeStrategy.BALANCED,
    ) -> Dict[str, Any]:
        """Deep merge two dictionaries.

        Args:
            base: Base dictionary
            updates: Updates to merge
            operations: List to append operations to
            target_file: Target file name for operations
            path: Current path in the structure

        Returns:
            Merged dictionary
        """
        result = copy.deepcopy(base)

        for key, value in updates.items():
            current_path = f"{path}.{key}" if path else key

            if key not in result:
                # New key - add it
                result[key] = value
                operations.append(
                    UpdateOperation(
                        target_file=target_file,
                        operation_type="add",
                        path=current_path,
                        new_value=value,
                    )
                )
            elif isinstance(value, dict) and isinstance(result[key], dict):
                # Both are dicts - recurse
                result[key] = self._deep_merge(
                    result[key], value, operations, target_file, current_path, strategy
                )
            elif result[key] != value:
                # Different value
                if strategy == MergeStrategy.CONSERVATIVE:
                    continue  # Skip update in conservative mode

                # Update value
                old_value = result[key]
                result[key] = value
                operations.append(
                    UpdateOperation(
                        target_file=target_file,
                        operation_type="modify",
                        path=current_path,
                        old_value=old_value,
                        new_value=value,
                    )
                )

        return result

    def _validate_content(self, content: Dict[str, Any]) -> List[str]:
        """Validate merged content against schema.

        Args:
            content: Content to validate

        Returns:
            List of validation errors (empty if valid)
        """
        errors: List[str] = []

        # Basic validation
        if not isinstance(content, dict):
            errors.append("Content must be a JSON object")
            return errors

        # Check required fields
        if "version" not in content:
            errors.append("Missing required field: version")

        # Validate version format
        version = content.get("version", "")
        if version and not self._is_valid_version(version):
            errors.append(f"Invalid version format: {version}")

        return errors

    def _is_valid_version(self, version: str) -> bool:
        """Check if version string is valid semver.

        Args:
            version: Version string to check

        Returns:
            True if valid
        """
        import re

        pattern = r"^\d+\.\d+\.\d+$"
        return bool(re.match(pattern, version))

    def rollback(self, backup_path: Path) -> bool:
        """Rollback a file to a previous backup.

        Args:
            backup_path: Path to the backup file

        Returns:
            True if rollback was successful
        """
        if not backup_path.exists():
            return False

        # Extract original filename from backup name
        # Format: filename.YYYYMMDD_HHMMSS.json
        parts = backup_path.stem.rsplit(".", 1)
        if len(parts) < 2:
            return False

        original_stem = parts[0]
        target_path = self.knowledge_dir / f"{original_stem}.json"

        return self._restore_backup(backup_path, target_path)

    def rollback_batch(self, batch_id: str) -> bool:
        """Rollback all changes from a batch.

        Args:
            batch_id: ID of the batch to rollback

        Returns:
            True if all rollbacks succeeded
        """
        # Find the batch in history
        batch = None
        for b in self._history:
            if b.batch_id == batch_id:
                batch = b
                break

        if not batch:
            return False

        success = True
        for result in batch.results:
            if result.backup_path:
                if not self.rollback(result.backup_path):
                    success = False

        return success

    def list_backups(self, file_stem: Optional[str] = None) -> List[Path]:
        """List available backups.

        Args:
            file_stem: Optional filter by file name

        Returns:
            List of backup file paths
        """
        if file_stem:
            pattern = f"{file_stem}.*"
        else:
            pattern = "*.*"

        backups = list(self.backup_dir.glob(pattern))
        backups.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        return backups

    def get_history(self) -> List[BatchUpdateResult]:
        """Get update history.

        Returns:
            List of batch update results
        """
        return self._history.copy()
