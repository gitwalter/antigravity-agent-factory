"""
Notification System for Knowledge Evolution

This module provides a notification system for alerting users about
available knowledge updates, applied changes, and system events.

Features:
    - Multiple notification channels (console, file, callback)
    - Priority-based filtering
    - Quiet mode support
    - Update digest generation
    - Notification history

Author: Antigravity Agent FactoryVersion: 1.0.0
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
from pathlib import Path
import json


class NotificationLevel(Enum):
    """Notification importance levels."""

    CRITICAL = 1  # Security issues, breaking changes
    WARNING = 2  # Important updates, deprecations
    INFO = 3  # General information
    DEBUG = 4  # Detailed debugging info


class NotificationChannel(Enum):
    """Available notification channels."""

    CONSOLE = "console"  # Print to console
    FILE = "file"  # Write to file
    CALLBACK = "callback"  # Call registered functions


@dataclass
class Notification:
    """Represents a single notification.

    Attributes:
        title: Short title
        message: Full message content
        level: Importance level
        source: What generated this notification
        timestamp: When notification was created
        data: Additional data (e.g., update details)
        read: Whether notification has been read
    """

    title: str
    message: str
    level: NotificationLevel = NotificationLevel.INFO
    source: str = "knowledge-evolution"
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    data: Optional[Dict[str, Any]] = None
    read: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "title": self.title,
            "message": self.message,
            "level": self.level.name,
            "source": self.source,
            "timestamp": self.timestamp.isoformat(),
            "data": self.data,
            "read": self.read,
        }

    def format_console(self) -> str:
        """Format for console output."""
        level_icons = {
            NotificationLevel.CRITICAL: "[!]",
            NotificationLevel.WARNING: "[*]",
            NotificationLevel.INFO: "[i]",
            NotificationLevel.DEBUG: "[.]",
        }
        icon = level_icons.get(self.level, "[?]")
        return f"{icon} {self.title}: {self.message}"


@dataclass
class NotificationConfig:
    """Configuration for the notification system.

    Attributes:
        show_update_summary: Show summary of available updates
        show_changelog: Show changelog for updates
        quiet_mode: Suppress non-critical notifications
        min_level: Minimum level to show
        file_path: Path for file notifications
        max_history: Maximum notifications to keep in history
    """

    show_update_summary: bool = True
    show_changelog: bool = True
    quiet_mode: bool = False
    min_level: NotificationLevel = NotificationLevel.INFO
    file_path: Optional[Path] = None
    max_history: int = 100


class NotificationSystem:
    """System for managing and delivering notifications.

    This class handles creating, storing, and delivering notifications
    about knowledge updates and system events.

    Example:
        notifier = NotificationSystem(config)
        notifier.notify_updates_available(updates)
        notifier.notify_update_applied(result)
    """

    def __init__(self, config: Optional[NotificationConfig] = None):
        """Initialize the notification system.

        Args:
            config: Notification configuration
        """
        self.config = config or NotificationConfig()
        self._history: List[Notification] = []
        self._callbacks: List[Callable[[Notification], None]] = []

    def notify(
        self,
        title: str,
        message: str,
        level: NotificationLevel = NotificationLevel.INFO,
        source: str = "knowledge-evolution",
        data: Optional[Dict[str, Any]] = None,
    ) -> Notification:
        """Send a notification.

        Args:
            title: Short title
            message: Full message
            level: Importance level
            source: What generated this
            data: Additional data

        Returns:
            The created notification
        """
        notification = Notification(
            title=title,
            message=message,
            level=level,
            source=source,
            data=data,
        )

        # Check if should be shown
        if self._should_show(notification):
            self._deliver(notification)

        # Add to history
        self._add_to_history(notification)

        return notification

    def _should_show(self, notification: Notification) -> bool:
        """Check if notification should be shown.

        Args:
            notification: The notification to check

        Returns:
            True if should be shown
        """
        # Quiet mode - only critical
        if self.config.quiet_mode:
            return notification.level == NotificationLevel.CRITICAL

        # Check minimum level
        return notification.level.value <= self.config.min_level.value

    def _deliver(self, notification: Notification) -> None:
        """Deliver notification through all channels.

        Args:
            notification: Notification to deliver
        """
        # Console output
        print(notification.format_console())

        # File output
        if self.config.file_path:
            self._write_to_file(notification)

        # Callbacks
        for callback in self._callbacks:
            try:
                callback(notification)
            except Exception as e:
                print(f"Notification callback error: {e}")

    def _write_to_file(self, notification: Notification) -> None:
        """Write notification to file.

        Args:
            notification: Notification to write
        """
        if not self.config.file_path:
            return

        try:
            self.config.file_path.parent.mkdir(parents=True, exist_ok=True)

            # Append to file
            with open(self.config.file_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(notification.to_dict()) + "\n")
        except Exception as e:
            # Print error so it's visible in tests
            import sys

            error_msg = f"Failed to write notification to file: {e}"
            print(error_msg, file=sys.stderr)
            # Also print to stdout for compatibility with test capture
            print(f"Error: {error_msg}")

    def _add_to_history(self, notification: Notification) -> None:
        """Add notification to history.

        Args:
            notification: Notification to add
        """
        self._history.append(notification)

        # Trim history if needed
        if len(self._history) > self.config.max_history:
            self._history = self._history[-self.config.max_history :]

    def register_callback(self, callback: Callable[[Notification], None]) -> None:
        """Register a callback for notifications.

        Args:
            callback: Function to call with each notification
        """
        self._callbacks.append(callback)

    def unregister_callback(self, callback: Callable[[Notification], None]) -> None:
        """Unregister a notification callback.

        Args:
            callback: Callback to remove
        """
        if callback in self._callbacks:
            self._callbacks.remove(callback)

    def notify_updates_available(
        self,
        updates: List[Any],  # List[KnowledgeUpdate]
        show_details: bool = True,
    ) -> Notification:
        """Notify about available knowledge updates.

        Args:
            updates: List of available updates
            show_details: Whether to show update details

        Returns:
            The notification
        """
        if not updates:
            return self.notify(
                title="Knowledge Check Complete",
                message="No updates available",
                level=NotificationLevel.INFO,
            )

        # Count by priority
        priority_counts = {}
        for update in updates:
            priority_name = update.priority.name
            priority_counts[priority_name] = priority_counts.get(priority_name, 0) + 1

        # Build message
        message_parts = [f"{len(updates)} updates available"]
        for priority, count in sorted(priority_counts.items()):
            message_parts.append(f"  {priority}: {count}")

        # Determine notification level based on update priorities
        level = NotificationLevel.INFO
        if "CRITICAL" in priority_counts:
            level = NotificationLevel.CRITICAL
        elif "HIGH" in priority_counts:
            level = NotificationLevel.WARNING

        # Build details
        details = None
        if show_details and self.config.show_update_summary:
            details = {
                "total": len(updates),
                "by_priority": priority_counts,
                "files": [u.target_file for u in updates],
            }

        return self.notify(
            title="Knowledge Updates Available",
            message="\n".join(message_parts),
            level=level,
            data=details,
        )

    def notify_update_applied(
        self,
        result: Any,  # UpdateResult
        show_changelog: bool = True,
    ) -> Notification:
        """Notify about an applied update.

        Args:
            result: The update result
            show_changelog: Whether to show changelog

        Returns:
            The notification
        """
        if result.success:
            message = f"Updated {result.target_file}: {result.old_version} → {result.new_version}"
            level = NotificationLevel.INFO
        else:
            message = (
                f"Failed to update {result.target_file}: {', '.join(result.errors)}"
            )
            level = NotificationLevel.WARNING

        details = None
        if show_changelog and self.config.show_changelog:
            details = {
                "file": result.target_file,
                "old_version": result.old_version,
                "new_version": result.new_version,
                "operations": len(result.operations),
                "backup": str(result.backup_path) if result.backup_path else None,
            }

        return self.notify(
            title="Update Applied" if result.success else "Update Failed",
            message=message,
            level=level,
            data=details,
        )

    def notify_batch_complete(
        self,
        batch_result: Any,  # BatchUpdateResult
    ) -> Notification:
        """Notify about completed batch update.

        Args:
            batch_result: The batch result

        Returns:
            The notification
        """
        if batch_result.success:
            message = f"Applied {batch_result.total_applied} updates successfully"
            level = NotificationLevel.INFO
        else:
            message = f"Completed with issues: {batch_result.total_applied} applied, {batch_result.total_failed} failed"
            level = NotificationLevel.WARNING

        details = {
            "batch_id": batch_result.batch_id,
            "total_applied": batch_result.total_applied,
            "total_failed": batch_result.total_failed,
            "files": [r.target_file for r in batch_result.results],
        }

        return self.notify(
            title="Batch Update Complete",
            message=message,
            level=level,
            data=details,
        )

    def notify_rollback(
        self, file_name: str, backup_path: Path, success: bool
    ) -> Notification:
        """Notify about a rollback operation.

        Args:
            file_name: File that was rolled back
            backup_path: Backup that was restored
            success: Whether rollback succeeded

        Returns:
            The notification
        """
        if success:
            message = f"Rolled back {file_name} from backup"
            level = NotificationLevel.INFO
        else:
            message = f"Failed to rollback {file_name}"
            level = NotificationLevel.WARNING

        return self.notify(
            title="Rollback " + ("Complete" if success else "Failed"),
            message=message,
            level=level,
            data={"file": file_name, "backup": str(backup_path)},
        )

    def get_history(
        self, level: Optional[NotificationLevel] = None, unread_only: bool = False
    ) -> List[Notification]:
        """Get notification history.

        Args:
            level: Filter by level (optional)
            unread_only: Only return unread notifications

        Returns:
            List of notifications
        """
        result = self._history

        if level:
            result = [n for n in result if n.level == level]

        if unread_only:
            result = [n for n in result if not n.read]

        return result

    def mark_read(self, notification: Notification) -> None:
        """Mark a notification as read.

        Args:
            notification: Notification to mark
        """
        notification.read = True

    def mark_all_read(self) -> None:
        """Mark all notifications as read."""
        for notification in self._history:
            notification.read = True

    def clear_history(self) -> None:
        """Clear notification history."""
        self._history.clear()

    def generate_digest(self) -> str:
        """Generate a digest of unread notifications.

        Returns:
            Formatted digest string
        """
        unread = self.get_history(unread_only=True)

        if not unread:
            return "No unread notifications"

        lines = [f"=== {len(unread)} Unread Notifications ===", ""]

        # Group by level
        by_level: Dict[NotificationLevel, List[Notification]] = {}
        for n in unread:
            if n.level not in by_level:
                by_level[n.level] = []
            by_level[n.level].append(n)

        for level in sorted(by_level.keys(), key=lambda l: l.value):
            lines.append(f"## {level.name}")
            for n in by_level[level]:
                lines.append(f"  - {n.title}: {n.message}")
            lines.append("")

        return "\n".join(lines)
