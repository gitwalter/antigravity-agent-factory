"""
Changelog Generator for Knowledge Evolution

This module generates human-readable changelogs for knowledge file updates,
tracking what changed, when, and why.

Features:
    - Automatic changelog generation from updates
    - Multiple output formats (Markdown, JSON)
    - Version comparison
    - Breaking change highlighting
    - Source attribution

Author: Antigravity Agent Factory
Version: 1.0.0
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import json


@dataclass
class ChangelogEntry:
    """A single changelog entry.
    
    Attributes:
        version: Version number
        date: Release date
        changes: List of changes by category
        sources: Sources that contributed to changes
        breaking: Whether this version has breaking changes
        migration_notes: Notes for migrating from previous version
    """
    version: str
    date: str
    changes: Dict[str, List[str]]  # category -> list of changes
    sources: List[str] = field(default_factory=list)
    breaking: bool = False
    migration_notes: Optional[str] = None


class ChangelogGenerator:
    """Generator for knowledge update changelogs.
    
    This class creates and maintains changelogs for knowledge files,
    documenting all changes made by the knowledge evolution system.
    
    Example:
        generator = ChangelogGenerator(changelog_dir)
        entry = generator.create_entry(update_result)
        generator.append_entry("fastapi-patterns.json", entry)
        markdown = generator.generate_markdown("fastapi-patterns.json")
    """
    
    CHANGE_CATEGORIES = ["added", "changed", "deprecated", "removed", "fixed", "security"]
    
    def __init__(self, changelog_dir: Path):
        """Initialize the changelog generator.
        
        Args:
            changelog_dir: Directory to store changelog files
        """
        self.changelog_dir = Path(changelog_dir)
        self.changelog_dir.mkdir(parents=True, exist_ok=True)
    
    def get_changelog_path(self, knowledge_file: str) -> Path:
        """Get the changelog file path for a knowledge file.
        
        Args:
            knowledge_file: Name of the knowledge file
            
        Returns:
            Path to the changelog file
        """
        stem = Path(knowledge_file).stem
        return self.changelog_dir / f"{stem}-changelog.json"
    
    def load_changelog(self, knowledge_file: str) -> Dict[str, Any]:
        """Load existing changelog for a knowledge file.
        
        Args:
            knowledge_file: Name of the knowledge file
            
        Returns:
            Changelog data or empty structure
        """
        changelog_path = self.get_changelog_path(knowledge_file)
        
        if changelog_path.exists():
            with open(changelog_path, "r", encoding="utf-8") as f:
                return json.load(f)
        
        return {
            "$schema": "../schemas/changelog-schema.json",
            "knowledge_file": knowledge_file,
            "current_version": "1.0.0",
            "entries": [],
        }
    
    def save_changelog(self, knowledge_file: str, changelog: Dict[str, Any]) -> None:
        """Save changelog to file.
        
        Args:
            knowledge_file: Name of the knowledge file
            changelog: Changelog data to save
        """
        changelog_path = self.get_changelog_path(knowledge_file)
        
        with open(changelog_path, "w", encoding="utf-8") as f:
            json.dump(changelog, f, indent=2, ensure_ascii=False)
    
    def create_entry_from_update(
        self,
        update_result: Any  # UpdateResult
    ) -> ChangelogEntry:
        """Create a changelog entry from an update result.
        
        Args:
            update_result: Result from applying an update
            
        Returns:
            ChangelogEntry for this update
        """
        # Group changes by category
        changes: Dict[str, List[str]] = {cat: [] for cat in self.CHANGE_CATEGORIES}
        
        for op in update_result.operations:
            # Map operation type to changelog category
            if op.operation_type == "add":
                category = "added"
            elif op.operation_type == "modify":
                category = "changed"
            elif op.operation_type == "remove":
                category = "removed"
            else:
                category = "changed"
            
            # Create change description
            description = f"{op.path}"
            if op.new_value:
                description += f" (set to: {str(op.new_value)[:50]})"
            
            changes[category].append(description)
        
        # Remove empty categories
        changes = {k: v for k, v in changes.items() if v}
        
        return ChangelogEntry(
            version=update_result.new_version or "1.0.0",
            date=datetime.utcnow().strftime("%Y-%m-%d"),
            changes=changes,
            sources=[],  # Will be filled from update source
            breaking=False,
        )
    
    def create_entry_from_knowledge_update(
        self,
        update: Any  # KnowledgeUpdate
    ) -> ChangelogEntry:
        """Create a changelog entry from a KnowledgeUpdate.
        
        Args:
            update: The knowledge update
            
        Returns:
            ChangelogEntry for this update
        """
        # Group changes by category
        changes: Dict[str, List[str]] = {cat: [] for cat in self.CHANGE_CATEGORIES}
        
        for change in update.changes:
            category = change.change_type.value
            if category not in changes:
                category = "changed"
            changes[category].append(change.description)
        
        # Remove empty categories
        changes = {k: v for k, v in changes.items() if v}
        
        return ChangelogEntry(
            version=update.new_version,
            date=datetime.utcnow().strftime("%Y-%m-%d"),
            changes=changes,
            sources=[update.source.identifier] if update.source else [],
            breaking=update.breaking,
            migration_notes=None,
        )
    
    def append_entry(self, knowledge_file: str, entry: ChangelogEntry) -> None:
        """Append an entry to a knowledge file's changelog.
        
        Args:
            knowledge_file: Name of the knowledge file
            entry: Entry to append
        """
        changelog = self.load_changelog(knowledge_file)
        
        # Update current version
        changelog["current_version"] = entry.version
        
        # Create entry dict
        entry_dict = {
            "version": entry.version,
            "date": entry.date,
            "breaking": entry.breaking,
            "changes": entry.changes,
            "sources": [{"identifier": s} for s in entry.sources],
        }
        
        if entry.migration_notes:
            entry_dict["migration"] = {"instructions": entry.migration_notes}
        
        # Insert at beginning (newest first)
        changelog["entries"].insert(0, entry_dict)
        
        self.save_changelog(knowledge_file, changelog)
    
    def generate_markdown(
        self,
        knowledge_file: str,
        max_entries: Optional[int] = None
    ) -> str:
        """Generate a Markdown changelog.
        
        Args:
            knowledge_file: Name of the knowledge file
            max_entries: Maximum entries to include
            
        Returns:
            Markdown formatted changelog
        """
        changelog = self.load_changelog(knowledge_file)
        entries = changelog.get("entries", [])
        
        if max_entries:
            entries = entries[:max_entries]
        
        lines = [
            f"# Changelog for {knowledge_file}",
            "",
            f"Current Version: **{changelog.get('current_version', 'Unknown')}**",
            "",
        ]
        
        for entry in entries:
            version = entry.get("version", "Unknown")
            date = entry.get("date", "Unknown")
            breaking = entry.get("breaking", False)
            
            # Version header
            breaking_badge = " [BREAKING]" if breaking else ""
            lines.append(f"## [{version}]{breaking_badge} - {date}")
            lines.append("")
            
            # Changes by category
            changes = entry.get("changes", {})
            for category in self.CHANGE_CATEGORIES:
                if category in changes and changes[category]:
                    lines.append(f"### {category.capitalize()}")
                    for change in changes[category]:
                        lines.append(f"- {change}")
                    lines.append("")
            
            # Sources
            sources = entry.get("sources", [])
            if sources:
                source_names = [s.get("identifier", "Unknown") for s in sources]
                lines.append(f"*Sources: {', '.join(source_names)}*")
                lines.append("")
            
            # Migration notes
            migration = entry.get("migration", {})
            if migration.get("instructions"):
                lines.append("### Migration Notes")
                lines.append(migration["instructions"])
                lines.append("")
            
            lines.append("---")
            lines.append("")
        
        return "\n".join(lines)
    
    def generate_summary(
        self,
        knowledge_files: Optional[List[str]] = None
    ) -> str:
        """Generate a summary of recent changes across files.
        
        Args:
            knowledge_files: Optional list of files to include
            
        Returns:
            Summary markdown
        """
        lines = [
            "# Knowledge Evolution Summary",
            "",
            f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}",
            "",
        ]
        
        # Find all changelog files
        if knowledge_files:
            files = [self.get_changelog_path(kf) for kf in knowledge_files]
        else:
            files = list(self.changelog_dir.glob("*-changelog.json"))
        
        recent_changes: List[Dict[str, Any]] = []
        
        for changelog_path in files:
            if not changelog_path.exists():
                continue
            
            with open(changelog_path, "r", encoding="utf-8") as f:
                changelog = json.load(f)
            
            knowledge_file = changelog.get("knowledge_file", changelog_path.stem)
            entries = changelog.get("entries", [])
            
            if entries:
                latest = entries[0]
                recent_changes.append({
                    "file": knowledge_file,
                    "version": latest.get("version"),
                    "date": latest.get("date"),
                    "breaking": latest.get("breaking", False),
                    "change_count": sum(len(c) for c in latest.get("changes", {}).values()),
                })
        
        # Sort by date
        recent_changes.sort(key=lambda x: x.get("date", ""), reverse=True)
        
        lines.append("## Recent Updates")
        lines.append("")
        lines.append("| File | Version | Date | Changes | Breaking |")
        lines.append("|------|---------|------|---------|----------|")
        
        for change in recent_changes[:20]:  # Top 20
            breaking = "Yes" if change.get("breaking") else "No"
            lines.append(
                f"| {change['file']} | {change['version']} | {change['date']} | "
                f"{change['change_count']} | {breaking} |"
            )
        
        lines.append("")
        lines.append(f"Total files tracked: {len(recent_changes)}")
        
        return "\n".join(lines)
    
    def get_version_diff(
        self,
        knowledge_file: str,
        from_version: str,
        to_version: str
    ) -> List[ChangelogEntry]:
        """Get all changes between two versions.
        
        Args:
            knowledge_file: Name of the knowledge file
            from_version: Starting version (exclusive)
            to_version: Ending version (inclusive)
            
        Returns:
            List of changelog entries between versions
        """
        changelog = self.load_changelog(knowledge_file)
        entries = changelog.get("entries", [])
        
        result: List[ChangelogEntry] = []
        in_range = False
        
        for entry in entries:
            version = entry.get("version")
            
            if version == to_version:
                in_range = True
            
            if in_range:
                result.append(ChangelogEntry(
                    version=version,
                    date=entry.get("date"),
                    changes=entry.get("changes", {}),
                    sources=[s.get("identifier") for s in entry.get("sources", [])],
                    breaking=entry.get("breaking", False),
                ))
            
            if version == from_version:
                break
        
        return result
