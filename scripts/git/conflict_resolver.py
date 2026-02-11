"""
Conflict Resolver for Knowledge Evolution

This module handles detecting and resolving conflicts when merging
knowledge updates, particularly when multiple sources propose changes
to the same knowledge file or when user customizations conflict with
incoming updates.

Features:
    - Conflict detection in knowledge merges
    - Multiple resolution strategies
    - User customization preservation
    - Conflict reporting
    - Resolution suggestions

Author: Antigravity Agent Factory
Version: 1.0.0
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
import copy


class ConflictType(Enum):
    """Types of conflicts that can occur."""
    VALUE_DIFFERENCE = "value_difference"       # Same path, different values
    TYPE_MISMATCH = "type_mismatch"             # Same path, different types
    STRUCTURE_CONFLICT = "structure_conflict"   # Incompatible structures
    USER_CUSTOMIZATION = "user_customization"   # Conflicts with user changes
    VERSION_CONFLICT = "version_conflict"       # Version incompatibility


class ResolutionStrategy(Enum):
    """Strategies for resolving conflicts."""
    KEEP_EXISTING = "keep_existing"     # Keep the existing value
    USE_INCOMING = "use_incoming"       # Use the new value
    MERGE_VALUES = "merge_values"       # Attempt to merge both
    USER_DECISION = "user_decision"     # Require user input
    SKIP = "skip"                       # Skip this change


@dataclass
class Conflict:
    """Represents a single conflict.
    
    Attributes:
        path: JSON path where conflict occurs
        conflict_type: Type of conflict
        existing_value: Current value at path
        incoming_value: Proposed new value
        source: Source of the incoming value
        suggested_resolution: Suggested way to resolve
        resolution_notes: Explanation of conflict
    """
    path: str
    conflict_type: ConflictType
    existing_value: Any
    incoming_value: Any
    source: str = ""
    suggested_resolution: ResolutionStrategy = ResolutionStrategy.USER_DECISION
    resolution_notes: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "path": self.path,
            "type": self.conflict_type.value,
            "existing": str(self.existing_value)[:100],
            "incoming": str(self.incoming_value)[:100],
            "source": self.source,
            "suggested": self.suggested_resolution.value,
            "notes": self.resolution_notes,
        }


@dataclass
class ConflictReport:
    """Report of all conflicts detected during a merge.
    
    Attributes:
        target_file: File being merged
        conflicts: List of detected conflicts
        auto_resolved: Conflicts that were automatically resolved
        requires_user: Conflicts requiring user decision
        timestamp: When report was generated
    """
    target_file: str
    conflicts: List[Conflict] = field(default_factory=list)
    auto_resolved: List[Conflict] = field(default_factory=list)
    requires_user: List[Conflict] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    @property
    def has_conflicts(self) -> bool:
        """Check if there are any conflicts."""
        return len(self.conflicts) > 0
    
    @property
    def has_unresolved(self) -> bool:
        """Check if there are unresolved conflicts."""
        return len(self.requires_user) > 0
    
    def to_markdown(self) -> str:
        """Generate a markdown report."""
        lines = [
            f"# Conflict Report: {self.target_file}",
            "",
            f"Generated: {self.timestamp.strftime('%Y-%m-%d %H:%M UTC')}",
            "",
        ]
        
        if not self.has_conflicts:
            lines.append("No conflicts detected.")
            return "\n".join(lines)
        
        lines.append(f"**Total Conflicts**: {len(self.conflicts)}")
        lines.append(f"- Auto-resolved: {len(self.auto_resolved)}")
        lines.append(f"- Requires user decision: {len(self.requires_user)}")
        lines.append("")
        
        if self.auto_resolved:
            lines.append("## Auto-Resolved Conflicts")
            lines.append("")
            for conflict in self.auto_resolved:
                lines.append(f"- **{conflict.path}**: {conflict.resolution_notes}")
            lines.append("")
        
        if self.requires_user:
            lines.append("## Conflicts Requiring Decision")
            lines.append("")
            for conflict in self.requires_user:
                lines.append(f"### {conflict.path}")
                lines.append(f"- **Type**: {conflict.conflict_type.value}")
                lines.append(f"- **Existing**: `{str(conflict.existing_value)[:50]}`")
                lines.append(f"- **Incoming**: `{str(conflict.incoming_value)[:50]}`")
                lines.append(f"- **Suggestion**: {conflict.suggested_resolution.value}")
                lines.append("")
        
        return "\n".join(lines)


class ConflictResolver:
    """Resolver for knowledge merge conflicts.
    
    This class detects conflicts when merging knowledge updates and
    provides resolution strategies based on configured preferences.
    
    Example:
        resolver = ConflictResolver(preserve_user_changes=True)
        report = resolver.detect_conflicts(existing, incoming, source)
        resolved = resolver.resolve_all(existing, incoming, report)
    """
    
    # Paths that are typically user-customized
    USER_CUSTOMIZATION_PATHS = [
        "custom_patterns",
        "local_overrides",
        "user_additions",
    ]
    
    # Paths that should always use incoming value
    ALWAYS_UPDATE_PATHS = [
        "version",
        "metadata.updated",
        "metadata.checksum",
    ]
    
    def __init__(
        self,
        preserve_user_changes: bool = True,
        auto_resolve_minor: bool = True,
        trust_higher_priority: bool = True
    ):
        """Initialize the conflict resolver.
        
        Args:
            preserve_user_changes: Whether to preserve user customizations
            auto_resolve_minor: Whether to auto-resolve minor conflicts
            trust_higher_priority: Whether to prefer higher trust sources
        """
        self.preserve_user_changes = preserve_user_changes
        self.auto_resolve_minor = auto_resolve_minor
        self.trust_higher_priority = trust_higher_priority
    
    def detect_conflicts(
        self,
        existing: Dict[str, Any],
        incoming: Dict[str, Any],
        source: str = ""
    ) -> ConflictReport:
        """Detect all conflicts between existing and incoming content.
        
        Args:
            existing: Current knowledge content
            incoming: Proposed new content
            source: Source identifier for the incoming content
            
        Returns:
            ConflictReport with all detected conflicts
        """
        report = ConflictReport(target_file=source)
        
        self._detect_recursive(existing, incoming, "", source, report)
        
        # Categorize conflicts
        for conflict in report.conflicts:
            if self._can_auto_resolve(conflict):
                report.auto_resolved.append(conflict)
            else:
                report.requires_user.append(conflict)
        
        return report
    
    def _detect_recursive(
        self,
        existing: Any,
        incoming: Any,
        path: str,
        source: str,
        report: ConflictReport
    ) -> None:
        """Recursively detect conflicts in nested structures.
        
        Args:
            existing: Current value
            incoming: New value
            path: Current JSON path
            source: Source identifier
            report: Report to add conflicts to
        """
        # Same value - no conflict
        if existing == incoming:
            return
        
        # Type mismatch
        if type(existing) != type(incoming):
            report.conflicts.append(Conflict(
                path=path,
                conflict_type=ConflictType.TYPE_MISMATCH,
                existing_value=existing,
                incoming_value=incoming,
                source=source,
                suggested_resolution=self._suggest_for_type_mismatch(path),
                resolution_notes=f"Type changed from {type(existing).__name__} to {type(incoming).__name__}",
            ))
            return
        
        # Both are dictionaries - recurse
        if isinstance(existing, dict) and isinstance(incoming, dict):
            all_keys = set(existing.keys()) | set(incoming.keys())
            for key in all_keys:
                child_path = f"{path}.{key}" if path else key
                
                if key in existing and key not in incoming:
                    # Key removed in incoming
                    if not self._is_metadata_path(child_path):
                        report.conflicts.append(Conflict(
                            path=child_path,
                            conflict_type=ConflictType.VALUE_DIFFERENCE,
                            existing_value=existing[key],
                            incoming_value=None,
                            source=source,
                            suggested_resolution=ResolutionStrategy.KEEP_EXISTING,
                            resolution_notes="Key would be removed by update",
                        ))
                elif key not in existing and key in incoming:
                    # New key - no conflict (additions are good)
                    pass
                else:
                    # Both have key - recurse
                    self._detect_recursive(
                        existing[key], incoming[key], child_path, source, report
                    )
            return
        
        # Both are lists - check if content differs
        if isinstance(existing, list) and isinstance(incoming, list):
            if set(map(str, existing)) != set(map(str, incoming)):
                report.conflicts.append(Conflict(
                    path=path,
                    conflict_type=ConflictType.VALUE_DIFFERENCE,
                    existing_value=existing,
                    incoming_value=incoming,
                    source=source,
                    suggested_resolution=ResolutionStrategy.MERGE_VALUES,
                    resolution_notes="List contents differ",
                ))
            return
        
        # Simple value difference
        report.conflicts.append(Conflict(
            path=path,
            conflict_type=ConflictType.VALUE_DIFFERENCE,
            existing_value=existing,
            incoming_value=incoming,
            source=source,
            suggested_resolution=self._suggest_for_path(path),
            resolution_notes="Values differ",
        ))
    
    def _is_metadata_path(self, path: str) -> bool:
        """Check if path is a metadata path."""
        return path.startswith("metadata.") or path in ["version", "$schema"]
    
    def _is_user_customization_path(self, path: str) -> bool:
        """Check if path is typically user-customized."""
        for custom_path in self.USER_CUSTOMIZATION_PATHS:
            if path.startswith(custom_path) or custom_path in path:
                return True
        return False
    
    def _suggest_for_path(self, path: str) -> ResolutionStrategy:
        """Suggest resolution strategy based on path."""
        # Always update certain paths
        for update_path in self.ALWAYS_UPDATE_PATHS:
            if path == update_path or path.endswith(update_path):
                return ResolutionStrategy.USE_INCOMING
        
        # Preserve user customizations
        if self.preserve_user_changes and self._is_user_customization_path(path):
            return ResolutionStrategy.KEEP_EXISTING
        
        # Default to incoming for most cases
        return ResolutionStrategy.USE_INCOMING
    
    def _suggest_for_type_mismatch(self, path: str) -> ResolutionStrategy:
        """Suggest resolution for type mismatch."""
        # Type mismatches are usually significant - require user decision
        return ResolutionStrategy.USER_DECISION
    
    def _can_auto_resolve(self, conflict: Conflict) -> bool:
        """Determine if conflict can be auto-resolved."""
        if not self.auto_resolve_minor:
            return False
        
        # Never auto-resolve user decision suggestions
        if conflict.suggested_resolution == ResolutionStrategy.USER_DECISION:
            return False
        
        # Can auto-resolve updates to metadata/version
        if self._is_metadata_path(conflict.path):
            return True
        
        # Can auto-resolve if preserving user customizations
        if (self.preserve_user_changes and 
            self._is_user_customization_path(conflict.path) and
            conflict.suggested_resolution == ResolutionStrategy.KEEP_EXISTING):
            return True
        
        return False
    
    def resolve_all(
        self,
        existing: Dict[str, Any],
        incoming: Dict[str, Any],
        report: ConflictReport,
        user_decisions: Optional[Dict[str, ResolutionStrategy]] = None
    ) -> Dict[str, Any]:
        """Resolve all conflicts and produce merged content.
        
        Args:
            existing: Current content
            incoming: Incoming content
            report: Conflict report from detect_conflicts
            user_decisions: User decisions for conflicts (path -> strategy)
            
        Returns:
            Merged content with conflicts resolved
        """
        user_decisions = user_decisions or {}
        result = copy.deepcopy(existing)
        
        # Apply incoming changes, resolving conflicts
        self._apply_recursive(result, incoming, "", report, user_decisions)
        
        return result
    
    def _apply_recursive(
        self,
        target: Dict[str, Any],
        source: Dict[str, Any],
        path: str,
        report: ConflictReport,
        user_decisions: Dict[str, ResolutionStrategy]
    ) -> None:
        """Recursively apply changes, respecting resolutions.
        
        Args:
            target: Target dictionary to modify
            source: Source of changes
            path: Current path
            report: Conflict report
            user_decisions: User decisions
        """
        for key, value in source.items():
            child_path = f"{path}.{key}" if path else key
            
            # Check if there's a conflict at this path
            conflict = self._find_conflict(report, child_path)
            
            if conflict:
                # Get resolution strategy
                strategy = user_decisions.get(
                    child_path,
                    conflict.suggested_resolution
                )
                
                if strategy == ResolutionStrategy.KEEP_EXISTING:
                    continue  # Skip this change
                elif strategy == ResolutionStrategy.USE_INCOMING:
                    target[key] = copy.deepcopy(value)
                elif strategy == ResolutionStrategy.MERGE_VALUES:
                    target[key] = self._merge_values(
                        target.get(key), value, conflict.conflict_type
                    )
                elif strategy == ResolutionStrategy.SKIP:
                    continue
                # USER_DECISION without user input - skip
                elif strategy == ResolutionStrategy.USER_DECISION:
                    continue
            else:
                # No conflict - apply change
                if key not in target:
                    target[key] = copy.deepcopy(value)
                elif isinstance(value, dict) and isinstance(target.get(key), dict):
                    self._apply_recursive(
                        target[key], value, child_path, report, user_decisions
                    )
                else:
                    target[key] = copy.deepcopy(value)
    
    def _find_conflict(self, report: ConflictReport, path: str) -> Optional[Conflict]:
        """Find conflict for a specific path."""
        for conflict in report.conflicts:
            if conflict.path == path:
                return conflict
        return None
    
    def _merge_values(
        self,
        existing: Any,
        incoming: Any,
        conflict_type: ConflictType
    ) -> Any:
        """Merge two values."""
        # For lists, combine unique values
        if isinstance(existing, list) and isinstance(incoming, list):
            result = list(existing)
            for item in incoming:
                if item not in result:
                    result.append(item)
            return result
        
        # For dicts, merge recursively
        if isinstance(existing, dict) and isinstance(incoming, dict):
            result = copy.deepcopy(existing)
            for key, value in incoming.items():
                if key not in result:
                    result[key] = value
            return result
        
        # Default to incoming
        return incoming
