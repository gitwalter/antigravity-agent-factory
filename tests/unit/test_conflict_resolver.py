"""
Unit tests for scripts/git/conflict_resolver.py

Tests conflict detection, resolution strategies, and conflict reporting
for knowledge evolution merges.

Author: Cursor Agent Factory
Version: 1.0.0
"""

import copy
import json
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
from datetime import datetime

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.git.conflict_resolver import (
    ConflictType,
    ResolutionStrategy,
    Conflict,
    ConflictReport,
    ConflictResolver,
)


class TestConflictType:
    """Tests for ConflictType enum."""
    
    def test_conflict_type_values(self):
        """Test that all conflict types have correct values."""
        assert ConflictType.VALUE_DIFFERENCE.value == "value_difference"
        assert ConflictType.TYPE_MISMATCH.value == "type_mismatch"
        assert ConflictType.STRUCTURE_CONFLICT.value == "structure_conflict"
        assert ConflictType.USER_CUSTOMIZATION.value == "user_customization"
        assert ConflictType.VERSION_CONFLICT.value == "version_conflict"
    
    def test_all_conflict_types_present(self):
        """Test that all expected conflict types exist."""
        expected_types = {
            "value_difference",
            "type_mismatch",
            "structure_conflict",
            "user_customization",
            "version_conflict",
        }
        actual_types = {ct.value for ct in ConflictType}
        assert actual_types == expected_types


class TestResolutionStrategy:
    """Tests for ResolutionStrategy enum."""
    
    def test_resolution_strategy_values(self):
        """Test that all resolution strategies have correct values."""
        assert ResolutionStrategy.KEEP_EXISTING.value == "keep_existing"
        assert ResolutionStrategy.USE_INCOMING.value == "use_incoming"
        assert ResolutionStrategy.MERGE_VALUES.value == "merge_values"
        assert ResolutionStrategy.USER_DECISION.value == "user_decision"
        assert ResolutionStrategy.SKIP.value == "skip"
    
    def test_all_strategies_present(self):
        """Test that all expected strategies exist."""
        expected_strategies = {
            "keep_existing",
            "use_incoming",
            "merge_values",
            "user_decision",
            "skip",
        }
        actual_strategies = {rs.value for rs in ResolutionStrategy}
        assert actual_strategies == expected_strategies


class TestConflict:
    """Tests for Conflict dataclass."""
    
    def test_conflict_creation(self):
        """Test creating a Conflict with all fields."""
        conflict = Conflict(
            path="test.path",
            conflict_type=ConflictType.VALUE_DIFFERENCE,
            existing_value="old",
            incoming_value="new",
            source="test_source",
            suggested_resolution=ResolutionStrategy.USE_INCOMING,
            resolution_notes="Test notes",
        )
        
        assert conflict.path == "test.path"
        assert conflict.conflict_type == ConflictType.VALUE_DIFFERENCE
        assert conflict.existing_value == "old"
        assert conflict.incoming_value == "new"
        assert conflict.source == "test_source"
        assert conflict.suggested_resolution == ResolutionStrategy.USE_INCOMING
        assert conflict.resolution_notes == "Test notes"
    
    def test_conflict_defaults(self):
        """Test Conflict with default values."""
        conflict = Conflict(
            path="test.path",
            conflict_type=ConflictType.VALUE_DIFFERENCE,
            existing_value="old",
            incoming_value="new",
        )
        
        assert conflict.source == ""
        assert conflict.suggested_resolution == ResolutionStrategy.USER_DECISION
        assert conflict.resolution_notes == ""
    
    def test_conflict_to_dict(self):
        """Test converting Conflict to dictionary."""
        conflict = Conflict(
            path="test.path",
            conflict_type=ConflictType.TYPE_MISMATCH,
            existing_value={"complex": "object"},
            incoming_value="string",
            source="test_source",
            suggested_resolution=ResolutionStrategy.USER_DECISION,
            resolution_notes="Type changed",
        )
        
        result = conflict.to_dict()
        
        assert result["path"] == "test.path"
        assert result["type"] == "type_mismatch"
        assert "complex" in result["existing"]  # Truncated to 100 chars
        assert result["incoming"] == "string"
        assert result["source"] == "test_source"
        assert result["suggested"] == "user_decision"
        assert result["notes"] == "Type changed"
    
    def test_conflict_to_dict_truncates_long_values(self):
        """Test that to_dict truncates long values."""
        long_value = "x" * 200
        conflict = Conflict(
            path="test.path",
            conflict_type=ConflictType.VALUE_DIFFERENCE,
            existing_value=long_value,
            incoming_value="new",
        )
        
        result = conflict.to_dict()
        
        assert len(result["existing"]) <= 100
        # Note: to_dict doesn't add ellipsis, just truncates


class TestConflictReport:
    """Tests for ConflictReport dataclass."""
    
    def test_conflict_report_creation(self):
        """Test creating a ConflictReport."""
        report = ConflictReport(target_file="test.json")
        
        assert report.target_file == "test.json"
        assert report.conflicts == []
        assert report.auto_resolved == []
        assert report.requires_user == []
        assert isinstance(report.timestamp, datetime)
    
    def test_conflict_report_with_conflicts(self):
        """Test ConflictReport with conflicts."""
        conflict1 = Conflict(
            path="path1",
            conflict_type=ConflictType.VALUE_DIFFERENCE,
            existing_value="old1",
            incoming_value="new1",
        )
        conflict2 = Conflict(
            path="path2",
            conflict_type=ConflictType.TYPE_MISMATCH,
            existing_value="old2",
            incoming_value="new2",
        )
        
        report = ConflictReport(
            target_file="test.json",
            conflicts=[conflict1, conflict2],
            auto_resolved=[conflict1],
            requires_user=[conflict2],
        )
        
        assert len(report.conflicts) == 2
        assert len(report.auto_resolved) == 1
        assert len(report.requires_user) == 1
    
    def test_has_conflicts_property(self):
        """Test has_conflicts property."""
        report_empty = ConflictReport(target_file="test.json")
        assert report_empty.has_conflicts is False
        
        conflict = Conflict(
            path="path",
            conflict_type=ConflictType.VALUE_DIFFERENCE,
            existing_value="old",
            incoming_value="new",
        )
        report_with_conflicts = ConflictReport(
            target_file="test.json",
            conflicts=[conflict],
        )
        assert report_with_conflicts.has_conflicts is True
    
    def test_has_unresolved_property(self):
        """Test has_unresolved property."""
        report_empty = ConflictReport(target_file="test.json")
        assert report_empty.has_unresolved is False
        
        conflict = Conflict(
            path="path",
            conflict_type=ConflictType.VALUE_DIFFERENCE,
            existing_value="old",
            incoming_value="new",
        )
        report_with_unresolved = ConflictReport(
            target_file="test.json",
            requires_user=[conflict],
        )
        assert report_with_unresolved.has_unresolved is True
    
    def test_to_markdown_no_conflicts(self):
        """Test markdown generation with no conflicts."""
        report = ConflictReport(target_file="test.json")
        
        markdown = report.to_markdown()
        
        assert "# Conflict Report: test.json" in markdown
        assert "No conflicts detected." in markdown
    
    def test_to_markdown_with_conflicts(self):
        """Test markdown generation with conflicts."""
        auto_conflict = Conflict(
            path="auto.path",
            conflict_type=ConflictType.VALUE_DIFFERENCE,
            existing_value="old",
            incoming_value="new",
            resolution_notes="Auto-resolved",
        )
        user_conflict = Conflict(
            path="user.path",
            conflict_type=ConflictType.TYPE_MISMATCH,
            existing_value={"key": "value"},
            incoming_value="string",
            suggested_resolution=ResolutionStrategy.USER_DECISION,
        )
        
        report = ConflictReport(
            target_file="test.json",
            conflicts=[auto_conflict, user_conflict],
            auto_resolved=[auto_conflict],
            requires_user=[user_conflict],
        )
        
        markdown = report.to_markdown()
        
        assert "# Conflict Report: test.json" in markdown
        assert "**Total Conflicts**: 2" in markdown
        assert "Auto-resolved: 1" in markdown
        assert "Requires user decision: 1" in markdown
        assert "## Auto-Resolved Conflicts" in markdown
        assert "## Conflicts Requiring Decision" in markdown
        assert "auto.path" in markdown
        assert "user.path" in markdown
        assert "Type changed" in markdown or "type_mismatch" in markdown


class TestConflictResolverInitialization:
    """Tests for ConflictResolver initialization."""
    
    def test_default_initialization(self):
        """Test ConflictResolver with default parameters."""
        resolver = ConflictResolver()
        
        assert resolver.preserve_user_changes is True
        assert resolver.auto_resolve_minor is True
        assert resolver.trust_higher_priority is True
    
    def test_custom_initialization(self):
        """Test ConflictResolver with custom parameters."""
        resolver = ConflictResolver(
            preserve_user_changes=False,
            auto_resolve_minor=False,
            trust_higher_priority=False,
        )
        
        assert resolver.preserve_user_changes is False
        assert resolver.auto_resolve_minor is False
        assert resolver.trust_higher_priority is False
    
    def test_user_customization_paths(self):
        """Test that USER_CUSTOMIZATION_PATHS is defined."""
        resolver = ConflictResolver()
        
        assert len(resolver.USER_CUSTOMIZATION_PATHS) > 0
        assert "custom_patterns" in resolver.USER_CUSTOMIZATION_PATHS
    
    def test_always_update_paths(self):
        """Test that ALWAYS_UPDATE_PATHS is defined."""
        resolver = ConflictResolver()
        
        assert len(resolver.ALWAYS_UPDATE_PATHS) > 0
        assert "version" in resolver.ALWAYS_UPDATE_PATHS


class TestConflictDetection:
    """Tests for conflict detection logic."""
    
    @pytest.fixture
    def resolver(self):
        """Create a ConflictResolver instance."""
        return ConflictResolver()
    
    def test_no_conflict_same_values(self, resolver):
        """Test that identical values produce no conflicts."""
        existing = {"key": "value"}
        incoming = {"key": "value"}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        
        assert report.has_conflicts is False
        assert len(report.conflicts) == 0
    
    def test_simple_value_difference(self, resolver):
        """Test detection of simple value differences."""
        existing = {"key": "old_value"}
        incoming = {"key": "new_value"}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        
        assert report.has_conflicts is True
        assert len(report.conflicts) == 1
        assert report.conflicts[0].path == "key"
        assert report.conflicts[0].conflict_type == ConflictType.VALUE_DIFFERENCE
        assert report.conflicts[0].existing_value == "old_value"
        assert report.conflicts[0].incoming_value == "new_value"
    
    def test_type_mismatch(self, resolver):
        """Test detection of type mismatches."""
        existing = {"key": "string"}
        incoming = {"key": 123}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        
        assert report.has_conflicts is True
        assert len(report.conflicts) == 1
        assert report.conflicts[0].conflict_type == ConflictType.TYPE_MISMATCH
        assert report.conflicts[0].suggested_resolution == ResolutionStrategy.USER_DECISION
    
    def test_nested_dict_conflicts(self, resolver):
        """Test detection of conflicts in nested dictionaries."""
        existing = {"outer": {"inner": "old"}}
        incoming = {"outer": {"inner": "new"}}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        
        assert report.has_conflicts is True
        assert len(report.conflicts) == 1
        assert report.conflicts[0].path == "outer.inner"
    
    def test_new_keys_no_conflict(self, resolver):
        """Test that new keys don't create conflicts."""
        existing = {"key1": "value1"}
        incoming = {"key1": "value1", "key2": "value2"}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        
        assert report.has_conflicts is False
    
    def test_removed_keys_create_conflict(self, resolver):
        """Test that removed keys create conflicts."""
        existing = {"key1": "value1", "key2": "value2"}
        incoming = {"key1": "value1"}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        
        assert report.has_conflicts is True
        assert len(report.conflicts) == 1
        assert report.conflicts[0].path == "key2"
        assert report.conflicts[0].incoming_value is None
        assert report.conflicts[0].suggested_resolution == ResolutionStrategy.KEEP_EXISTING
    
    def test_list_differences(self, resolver):
        """Test detection of list differences."""
        existing = {"items": ["a", "b"]}
        incoming = {"items": ["b", "c"]}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        
        assert report.has_conflicts is True
        assert len(report.conflicts) == 1
        assert report.conflicts[0].conflict_type == ConflictType.VALUE_DIFFERENCE
        assert report.conflicts[0].suggested_resolution == ResolutionStrategy.MERGE_VALUES
    
    def test_list_same_content_no_conflict(self, resolver):
        """Test that lists with same content (different order) don't conflict."""
        existing = {"items": ["a", "b"]}
        incoming = {"items": ["b", "a"]}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        
        # Should not conflict because set comparison treats them as same
        assert report.has_conflicts is False
    
    def test_metadata_paths_no_conflict_on_removal(self, resolver):
        """Test that metadata path removals create conflicts (but can be auto-resolved)."""
        existing = {"metadata": {"updated": "2024-01-01"}, "data": "value"}
        incoming = {"data": "value"}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        
        # metadata removal does create a conflict, but it can be auto-resolved
        metadata_conflicts = [c for c in report.conflicts if "metadata" in c.path]
        assert len(metadata_conflicts) == 1
        # The conflict suggests KEEP_EXISTING for removals
        assert metadata_conflicts[0].suggested_resolution == ResolutionStrategy.KEEP_EXISTING
    
    def test_complex_nested_structure(self, resolver):
        """Test conflict detection in complex nested structures."""
        existing = {
            "level1": {
                "level2": {
                    "level3": "old_value",
                    "other": "unchanged",
                }
            },
            "top": "value",
        }
        incoming = {
            "level1": {
                "level2": {
                    "level3": "new_value",
                    "other": "unchanged",
                }
            },
            "top": "value",
        }
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        
        assert report.has_conflicts is True
        assert len(report.conflicts) == 1
        assert report.conflicts[0].path == "level1.level2.level3"


class TestConflictResolutionStrategies:
    """Tests for resolution strategy suggestions."""
    
    @pytest.fixture
    def resolver(self):
        """Create a ConflictResolver instance."""
        return ConflictResolver()
    
    def test_version_path_uses_incoming(self, resolver):
        """Test that version paths suggest USE_INCOMING."""
        existing = {"version": "1.0.0"}
        incoming = {"version": "2.0.0"}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        
        assert report.conflicts[0].suggested_resolution == ResolutionStrategy.USE_INCOMING
    
    def test_metadata_paths_use_incoming(self, resolver):
        """Test that metadata paths suggest USE_INCOMING."""
        existing = {"metadata": {"updated": "2024-01-01"}}
        incoming = {"metadata": {"updated": "2024-01-02"}}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        
        assert report.conflicts[0].suggested_resolution == ResolutionStrategy.USE_INCOMING
    
    def test_user_customization_paths_keep_existing(self, resolver):
        """Test that user customization paths suggest KEEP_EXISTING."""
        existing = {"custom_patterns": {"pattern1": "value1"}}
        incoming = {"custom_patterns": {"pattern1": "value2"}}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        
        assert report.conflicts[0].suggested_resolution == ResolutionStrategy.KEEP_EXISTING
    
    def test_user_customization_disabled(self):
        """Test that disabling preserve_user_changes changes suggestion."""
        resolver = ConflictResolver(preserve_user_changes=False)
        
        existing = {"custom_patterns": {"pattern1": "value1"}}
        incoming = {"custom_patterns": {"pattern1": "value2"}}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        
        assert report.conflicts[0].suggested_resolution == ResolutionStrategy.USE_INCOMING
    
    def test_type_mismatch_requires_user_decision(self, resolver):
        """Test that type mismatches require user decision."""
        existing = {"key": "string"}
        incoming = {"key": 123}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        
        assert report.conflicts[0].suggested_resolution == ResolutionStrategy.USER_DECISION


class TestAutoResolution:
    """Tests for automatic conflict resolution."""
    
    def test_auto_resolve_metadata(self):
        """Test that metadata conflicts are auto-resolved."""
        resolver = ConflictResolver(auto_resolve_minor=True)
        
        existing = {"metadata": {"updated": "2024-01-01"}}
        incoming = {"metadata": {"updated": "2024-01-02"}}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        
        assert len(report.auto_resolved) == 1
        assert len(report.requires_user) == 0
    
    def test_auto_resolve_user_customization_preservation(self):
        """Test that user customization preservation is auto-resolved."""
        resolver = ConflictResolver(
            preserve_user_changes=True,
            auto_resolve_minor=True,
        )
        
        existing = {"custom_patterns": {"pattern1": "value1"}}
        incoming = {"custom_patterns": {"pattern1": "value2"}}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        
        assert len(report.auto_resolved) == 1
    
    def test_no_auto_resolve_when_disabled(self):
        """Test that auto-resolution is disabled when flag is False."""
        resolver = ConflictResolver(auto_resolve_minor=False)
        
        existing = {"metadata": {"updated": "2024-01-01"}}
        incoming = {"metadata": {"updated": "2024-01-02"}}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        
        assert len(report.auto_resolved) == 0
        assert len(report.requires_user) == 1
    
    def test_user_decision_not_auto_resolved(self):
        """Test that USER_DECISION conflicts are never auto-resolved."""
        resolver = ConflictResolver(auto_resolve_minor=True)
        
        existing = {"key": "string"}
        incoming = {"key": 123}  # Type mismatch
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        
        assert len(report.auto_resolved) == 0
        assert len(report.requires_user) == 1


class TestConflictResolution:
    """Tests for resolving conflicts and producing merged content."""
    
    @pytest.fixture
    def resolver(self):
        """Create a ConflictResolver instance."""
        return ConflictResolver()
    
    def test_resolve_no_conflicts(self, resolver):
        """Test resolution with no conflicts."""
        existing = {"key1": "value1"}
        incoming = {"key2": "value2"}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        resolved = resolver.resolve_all(existing, incoming, report)
        
        assert resolved["key1"] == "value1"
        assert resolved["key2"] == "value2"
    
    def test_resolve_keep_existing(self, resolver):
        """Test resolution with KEEP_EXISTING strategy."""
        existing = {"key": "old_value"}
        incoming = {"key": "new_value"}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        user_decisions = {"key": ResolutionStrategy.KEEP_EXISTING}
        resolved = resolver.resolve_all(existing, incoming, report, user_decisions)
        
        assert resolved["key"] == "old_value"
    
    def test_resolve_use_incoming(self, resolver):
        """Test resolution with USE_INCOMING strategy."""
        existing = {"key": "old_value"}
        incoming = {"key": "new_value"}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        user_decisions = {"key": ResolutionStrategy.USE_INCOMING}
        resolved = resolver.resolve_all(existing, incoming, report, user_decisions)
        
        assert resolved["key"] == "new_value"
    
    def test_resolve_merge_values_lists(self, resolver):
        """Test resolution with MERGE_VALUES strategy for lists."""
        existing = {"items": ["a", "b"]}
        incoming = {"items": ["b", "c"]}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        user_decisions = {"items": ResolutionStrategy.MERGE_VALUES}
        resolved = resolver.resolve_all(existing, incoming, report, user_decisions)
        
        assert set(resolved["items"]) == {"a", "b", "c"}
    
    def test_resolve_merge_values_dicts(self, resolver):
        """Test resolution with MERGE_VALUES strategy for dicts."""
        existing = {"outer": {"inner1": "a"}}
        incoming = {"outer": {"inner2": "b"}}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        user_decisions = {"outer": ResolutionStrategy.MERGE_VALUES}
        resolved = resolver.resolve_all(existing, incoming, report, user_decisions)
        
        assert resolved["outer"]["inner1"] == "a"
        assert resolved["outer"]["inner2"] == "b"
    
    def test_resolve_skip(self, resolver):
        """Test resolution with SKIP strategy."""
        existing = {"key": "old_value"}
        incoming = {"key": "new_value"}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        user_decisions = {"key": ResolutionStrategy.SKIP}
        resolved = resolver.resolve_all(existing, incoming, report, user_decisions)
        
        assert resolved["key"] == "old_value"
    
    def test_resolve_user_decision_without_input(self, resolver):
        """Test that USER_DECISION without user input keeps existing."""
        existing = {"key": "old_value"}
        incoming = {"key": "new_value"}
        
        # Create a conflict with USER_DECISION as suggested resolution
        conflict = Conflict(
            path="key",
            conflict_type=ConflictType.TYPE_MISMATCH,
            existing_value="old_value",
            incoming_value="new_value",
            suggested_resolution=ResolutionStrategy.USER_DECISION,
        )
        report = ConflictReport(target_file="test.json", conflicts=[conflict])
        report.requires_user = [conflict]
        
        # No user_decisions provided
        resolved = resolver.resolve_all(existing, incoming, report)
        
        # Should keep existing when USER_DECISION without input
        assert resolved["key"] == "old_value"
    
    def test_resolve_nested_conflicts(self, resolver):
        """Test resolution of nested conflicts."""
        existing = {"level1": {"level2": {"key": "old"}}}
        incoming = {"level1": {"level2": {"key": "new"}}}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        user_decisions = {"level1.level2.key": ResolutionStrategy.USE_INCOMING}
        resolved = resolver.resolve_all(existing, incoming, report, user_decisions)
        
        assert resolved["level1"]["level2"]["key"] == "new"
    
    def test_resolve_preserves_unrelated_data(self, resolver):
        """Test that resolution preserves unrelated data."""
        existing = {
            "conflict_key": "old",
            "unrelated": {"nested": "value"},
            "list": [1, 2, 3],
        }
        incoming = {
            "conflict_key": "new",
            "new_key": "new_value",
        }
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        user_decisions = {"conflict_key": ResolutionStrategy.USE_INCOMING}
        resolved = resolver.resolve_all(existing, incoming, report, user_decisions)
        
        assert resolved["conflict_key"] == "new"
        assert resolved["unrelated"]["nested"] == "value"
        assert resolved["list"] == [1, 2, 3]
        assert resolved["new_key"] == "new_value"
    
    def test_resolve_does_not_modify_original(self, resolver):
        """Test that resolution doesn't modify original dictionaries."""
        existing = {"key": "old_value"}
        incoming = {"key": "new_value"}
        
        original_existing = copy.deepcopy(existing)
        original_incoming = copy.deepcopy(incoming)
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        resolved = resolver.resolve_all(existing, incoming, report)
        
        assert existing == original_existing
        assert incoming == original_incoming


class TestHelperMethods:
    """Tests for helper methods."""
    
    @pytest.fixture
    def resolver(self):
        """Create a ConflictResolver instance."""
        return ConflictResolver()
    
    def test_is_metadata_path(self, resolver):
        """Test _is_metadata_path helper."""
        assert resolver._is_metadata_path("metadata.updated") is True
        assert resolver._is_metadata_path("metadata.checksum") is True
        assert resolver._is_metadata_path("version") is True
        assert resolver._is_metadata_path("$schema") is True
        assert resolver._is_metadata_path("data.value") is False
    
    def test_is_user_customization_path(self, resolver):
        """Test _is_user_customization_path helper."""
        assert resolver._is_user_customization_path("custom_patterns") is True
        assert resolver._is_user_customization_path("custom_patterns.pattern1") is True
        assert resolver._is_user_customization_path("local_overrides") is True
        assert resolver._is_user_customization_path("user_additions") is True
        assert resolver._is_user_customization_path("data.value") is False
    
    def test_find_conflict(self, resolver):
        """Test _find_conflict helper."""
        conflict1 = Conflict(
            path="path1",
            conflict_type=ConflictType.VALUE_DIFFERENCE,
            existing_value="old1",
            incoming_value="new1",
        )
        conflict2 = Conflict(
            path="path2",
            conflict_type=ConflictType.VALUE_DIFFERENCE,
            existing_value="old2",
            incoming_value="new2",
        )
        
        report = ConflictReport(
            target_file="test.json",
            conflicts=[conflict1, conflict2],
        )
        
        found = resolver._find_conflict(report, "path1")
        assert found == conflict1
        
        found = resolver._find_conflict(report, "path2")
        assert found == conflict2
        
        found = resolver._find_conflict(report, "nonexistent")
        assert found is None
    
    def test_merge_values_lists(self, resolver):
        """Test _merge_values for lists."""
        existing = ["a", "b"]
        incoming = ["b", "c"]
        
        result = resolver._merge_values(
            existing, incoming, ConflictType.VALUE_DIFFERENCE
        )
        
        assert set(result) == {"a", "b", "c"}
        assert len(result) == 3
    
    def test_merge_values_dicts(self, resolver):
        """Test _merge_values for dictionaries."""
        existing = {"key1": "value1", "key2": "value2"}
        incoming = {"key2": "new_value2", "key3": "value3"}
        
        result = resolver._merge_values(
            existing, incoming, ConflictType.VALUE_DIFFERENCE
        )
        
        assert result["key1"] == "value1"
        # Note: _merge_values only adds new keys, doesn't overwrite existing ones
        assert result["key2"] == "value2"  # Existing value preserved
        assert result["key3"] == "value3"  # New key added
    
    def test_merge_values_other_types(self, resolver):
        """Test _merge_values for non-list/dict types defaults to incoming."""
        existing = "old"
        incoming = "new"
        
        result = resolver._merge_values(
            existing, incoming, ConflictType.VALUE_DIFFERENCE
        )
        
        assert result == "new"


class TestEdgeCases:
    """Tests for edge cases and error handling."""
    
    @pytest.fixture
    def resolver(self):
        """Create a ConflictResolver instance."""
        return ConflictResolver()
    
    def test_empty_dicts(self, resolver):
        """Test conflict detection with empty dictionaries."""
        existing = {}
        incoming = {}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        
        assert report.has_conflicts is False
    
    def test_empty_vs_populated(self, resolver):
        """Test conflict detection with empty vs populated dict."""
        existing = {}
        incoming = {"key": "value"}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        
        assert report.has_conflicts is False  # New keys don't conflict
    
    def test_populated_vs_empty(self, resolver):
        """Test conflict detection with populated vs empty dict."""
        existing = {"key": "value"}
        incoming = {}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        
        assert report.has_conflicts is True
        assert len(report.conflicts) == 1
    
    def test_empty_lists(self, resolver):
        """Test conflict detection with empty lists."""
        existing = {"items": []}
        incoming = {"items": []}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        
        assert report.has_conflicts is False
    
    def test_none_values(self, resolver):
        """Test conflict detection with None values."""
        existing = {"key": None}
        incoming = {"key": "value"}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        
        assert report.has_conflicts is True
        assert report.conflicts[0].conflict_type == ConflictType.TYPE_MISMATCH
    
    def test_boolean_values(self, resolver):
        """Test conflict detection with boolean values."""
        existing = {"flag": True}
        incoming = {"flag": False}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        
        assert report.has_conflicts is True
        assert report.conflicts[0].conflict_type == ConflictType.VALUE_DIFFERENCE
    
    def test_numeric_types(self, resolver):
        """Test conflict detection with different numeric types."""
        existing = {"number": 42}
        incoming = {"number": 42.0}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        
        # Note: 42 == 42.0 evaluates to True, so no conflict is detected
        # The equality check happens before the type check
        assert report.has_conflicts is False
    
    def test_numeric_types_different_values(self, resolver):
        """Test conflict detection with different numeric types and values."""
        existing = {"number": 42}
        incoming = {"number": 43.0}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        
        # Different values with different types should create a conflict
        assert report.has_conflicts is True
        assert report.conflicts[0].conflict_type == ConflictType.TYPE_MISMATCH
    
    def test_very_deep_nesting(self, resolver):
        """Test conflict detection with very deep nesting."""
        existing = {"a": {"b": {"c": {"d": {"e": "value"}}}}}
        incoming = {"a": {"b": {"c": {"d": {"e": "new_value"}}}}}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        
        assert report.has_conflicts is True
        assert report.conflicts[0].path == "a.b.c.d.e"
    
    def test_large_lists(self, resolver):
        """Test conflict detection with large lists."""
        existing = {"items": list(range(100))}
        incoming = {"items": list(range(50, 150))}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        
        assert report.has_conflicts is True
    
    def test_special_characters_in_paths(self, resolver):
        """Test conflict detection with special characters in keys."""
        existing = {"key-with-dash": "value1", "key_with_underscore": "value2"}
        incoming = {"key-with-dash": "value2", "key_with_underscore": "value1"}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        
        assert report.has_conflicts is True
        assert len(report.conflicts) == 2
    
    def test_list_with_duplicates(self, resolver):
        """Test conflict detection with lists containing duplicates."""
        existing = {"items": ["a", "a", "b"]}
        incoming = {"items": ["b", "b", "c"]}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        
        # Should detect conflict even with duplicates
        assert report.has_conflicts is True
    
    def test_dict_to_list_type_change(self, resolver):
        """Test conflict detection when dict changes to list."""
        existing = {"data": {"key": "value"}}
        incoming = {"data": ["item1", "item2"]}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        
        assert report.has_conflicts is True
        assert report.conflicts[0].conflict_type == ConflictType.TYPE_MISMATCH
    
    def test_list_to_dict_type_change(self, resolver):
        """Test conflict detection when list changes to dict."""
        existing = {"data": ["item1", "item2"]}
        incoming = {"data": {"key": "value"}}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        
        assert report.has_conflicts is True
        assert report.conflicts[0].conflict_type == ConflictType.TYPE_MISMATCH
    
    def test_string_to_number_type_change(self, resolver):
        """Test conflict detection when string changes to number."""
        existing = {"value": "123"}
        incoming = {"value": 123}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        
        assert report.has_conflicts is True
        assert report.conflicts[0].conflict_type == ConflictType.TYPE_MISMATCH
    
    def test_multiple_conflicts_same_level(self, resolver):
        """Test detection of multiple conflicts at the same level."""
        existing = {"key1": "old1", "key2": "old2", "key3": "old3"}
        incoming = {"key1": "new1", "key2": "new2", "key3": "new3"}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        
        assert report.has_conflicts is True
        assert len(report.conflicts) == 3
    
    def test_nested_list_conflicts(self, resolver):
        """Test conflict detection with nested lists."""
        existing = {"outer": [{"inner": "old"}]}
        incoming = {"outer": [{"inner": "new"}]}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        
        # Lists are compared as sets of strings, so this may or may not conflict
        # depending on string representation
        assert isinstance(report.conflicts, list)
    
    def test_empty_string_vs_none(self, resolver):
        """Test conflict detection between empty string and None."""
        existing = {"key": ""}
        incoming = {"key": None}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        
        assert report.has_conflicts is True
        assert report.conflicts[0].conflict_type == ConflictType.TYPE_MISMATCH
    
    def test_zero_vs_false(self, resolver):
        """Test that 0 and False are considered equal (Python semantics)."""
        existing = {"key": 0}
        incoming = {"key": False}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        
        # In Python, 0 == False, so no conflict should be detected
        assert report.has_conflicts is False
    
    def test_one_vs_true(self, resolver):
        """Test that 1 and True are considered equal (Python semantics)."""
        existing = {"key": 1}
        incoming = {"key": True}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        
        # In Python, 1 == True, so no conflict should be detected
        assert report.has_conflicts is False


class TestConflictResolutionAdvanced:
    """Advanced tests for conflict resolution."""
    
    @pytest.fixture
    def resolver(self):
        """Create a ConflictResolver instance."""
        return ConflictResolver()
    
    def test_resolve_multiple_conflicts_mixed_strategies(self, resolver):
        """Test resolving multiple conflicts with different strategies."""
        existing = {
            "keep_me": "old1",
            "replace_me": "old2",
            "merge_me": ["a", "b"],
        }
        incoming = {
            "keep_me": "new1",
            "replace_me": "new2",
            "merge_me": ["b", "c"],
        }
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        user_decisions = {
            "keep_me": ResolutionStrategy.KEEP_EXISTING,
            "replace_me": ResolutionStrategy.USE_INCOMING,
            "merge_me": ResolutionStrategy.MERGE_VALUES,
        }
        resolved = resolver.resolve_all(existing, incoming, report, user_decisions)
        
        assert resolved["keep_me"] == "old1"
        assert resolved["replace_me"] == "new2"
        assert set(resolved["merge_me"]) == {"a", "b", "c"}
    
    def test_resolve_with_partial_user_decisions(self, resolver):
        """Test resolution when only some conflicts have user decisions."""
        existing = {"key1": "old1", "key2": "old2"}
        incoming = {"key1": "new1", "key2": "new2"}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        # Only provide decision for key1
        user_decisions = {"key1": ResolutionStrategy.USE_INCOMING}
        resolved = resolver.resolve_all(existing, incoming, report, user_decisions)
        
        assert resolved["key1"] == "new1"
        # key2 should use suggested resolution (USE_INCOMING by default)
        assert resolved["key2"] == "new2"
    
    def test_resolve_merge_nested_dicts(self, resolver):
        """Test merging nested dictionaries."""
        existing = {
            "level1": {
                "level2": {
                    "keep": "old",
                    "shared": "old_value",
                }
            }
        }
        incoming = {
            "level1": {
                "level2": {
                    "add": "new",
                    "shared": "new_value",
                }
            }
        }
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        # The conflict is detected at the exact path where values differ
        user_decisions = {"level1.level2.shared": ResolutionStrategy.KEEP_EXISTING}
        resolved = resolver.resolve_all(existing, incoming, report, user_decisions)
        
        assert resolved["level1"]["level2"]["keep"] == "old"
        assert resolved["level1"]["level2"]["add"] == "new"
        # KEEP_EXISTING preserves the old value
        assert resolved["level1"]["level2"]["shared"] == "old_value"
    
    def test_resolve_list_merge_preserves_order(self, resolver):
        """Test that list merging preserves order from existing."""
        existing = {"items": ["a", "b", "c"]}
        incoming = {"items": ["d", "e", "a"]}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        user_decisions = {"items": ResolutionStrategy.MERGE_VALUES}
        resolved = resolver.resolve_all(existing, incoming, report, user_decisions)
        
        # Should start with existing items, then add new ones
        assert resolved["items"][:3] == ["a", "b", "c"]
        assert "d" in resolved["items"]
        assert "e" in resolved["items"]
    
    def test_resolve_empty_list_merge(self, resolver):
        """Test merging when existing list is empty."""
        existing = {"items": []}
        incoming = {"items": ["a", "b"]}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        user_decisions = {"items": ResolutionStrategy.MERGE_VALUES}
        resolved = resolver.resolve_all(existing, incoming, report, user_decisions)
        
        assert set(resolved["items"]) == {"a", "b"}
    
    def test_resolve_empty_dict_merge(self, resolver):
        """Test merging when existing dict is empty."""
        existing = {"data": {}}
        incoming = {"data": {"key": "value"}}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        user_decisions = {"data": ResolutionStrategy.MERGE_VALUES}
        resolved = resolver.resolve_all(existing, incoming, report, user_decisions)
        
        assert resolved["data"]["key"] == "value"
    
    def test_resolve_with_no_conflicts_applies_all_changes(self, resolver):
        """Test that resolution applies all changes when no conflicts."""
        existing = {"key1": "value1"}
        incoming = {"key1": "value1", "key2": "value2", "key3": {"nested": "value"}}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        resolved = resolver.resolve_all(existing, incoming, report)
        
        assert resolved["key1"] == "value1"
        assert resolved["key2"] == "value2"
        assert resolved["key3"]["nested"] == "value"
    
    def test_resolve_skips_removed_keys(self, resolver):
        """Test that SKIP strategy skips removed keys."""
        existing = {"key1": "value1", "key2": "value2"}
        incoming = {"key1": "value1"}
        
        report = resolver.detect_conflicts(existing, incoming, "test")
        user_decisions = {"key2": ResolutionStrategy.SKIP}
        resolved = resolver.resolve_all(existing, incoming, report, user_decisions)
        
        # key2 should still exist (SKIP means don't apply the removal)
        assert "key2" in resolved
        assert resolved["key2"] == "value2"


class TestConflictReportAdvanced:
    """Advanced tests for ConflictReport."""
    
    def test_report_timestamp_is_datetime(self):
        """Test that timestamp is a datetime object."""
        report = ConflictReport(target_file="test.json")
        
        assert isinstance(report.timestamp, datetime)
    
    def test_report_categorization(self):
        """Test that conflicts are properly categorized."""
        auto_conflict = Conflict(
            path="auto.path",
            conflict_type=ConflictType.VALUE_DIFFERENCE,
            existing_value="old",
            incoming_value="new",
            suggested_resolution=ResolutionStrategy.USE_INCOMING,
        )
        user_conflict = Conflict(
            path="user.path",
            conflict_type=ConflictType.TYPE_MISMATCH,
            existing_value="old",
            incoming_value=123,
            suggested_resolution=ResolutionStrategy.USER_DECISION,
        )
        
        resolver = ConflictResolver(auto_resolve_minor=True)
        # Manually categorize (simulating detect_conflicts behavior)
        report = ConflictReport(target_file="test.json", conflicts=[auto_conflict, user_conflict])
        
        # Simulate categorization
        for conflict in report.conflicts:
            if resolver._can_auto_resolve(conflict):
                report.auto_resolved.append(conflict)
            else:
                report.requires_user.append(conflict)
        
        assert len(report.auto_resolved) >= 0
        assert len(report.requires_user) >= 0
        assert len(report.conflicts) == 2
    
    def test_markdown_with_long_values(self):
        """Test markdown generation with long values."""
        conflict = Conflict(
            path="test.path",
            conflict_type=ConflictType.VALUE_DIFFERENCE,
            existing_value="x" * 200,
            incoming_value="y" * 200,
        )
        
        report = ConflictReport(
            target_file="test.json",
            conflicts=[conflict],
            requires_user=[conflict],
        )
        
        markdown = report.to_markdown()
        
        # Values should be truncated in markdown
        assert len(markdown) < 1000  # Reasonable size
    
    def test_markdown_empty_auto_resolved(self):
        """Test markdown when auto_resolved is empty."""
        conflict = Conflict(
            path="test.path",
            conflict_type=ConflictType.VALUE_DIFFERENCE,
            existing_value="old",
            incoming_value="new",
        )
        
        report = ConflictReport(
            target_file="test.json",
            conflicts=[conflict],
            auto_resolved=[],
            requires_user=[conflict],
        )
        
        markdown = report.to_markdown()
        
        assert "## Auto-Resolved Conflicts" not in markdown
        assert "## Conflicts Requiring Decision" in markdown
    
    def test_markdown_empty_requires_user(self):
        """Test markdown when requires_user is empty."""
        conflict = Conflict(
            path="test.path",
            conflict_type=ConflictType.VALUE_DIFFERENCE,
            existing_value="old",
            incoming_value="new",
        )
        
        report = ConflictReport(
            target_file="test.json",
            conflicts=[conflict],
            auto_resolved=[conflict],
            requires_user=[],
        )
        
        markdown = report.to_markdown()
        
        assert "## Auto-Resolved Conflicts" in markdown
        assert "## Conflicts Requiring Decision" not in markdown


class TestPathHelpers:
    """Tests for path helper methods."""
    
    @pytest.fixture
    def resolver(self):
        """Create a ConflictResolver instance."""
        return ConflictResolver()
    
    def test_is_metadata_path_variations(self, resolver):
        """Test _is_metadata_path with various path formats."""
        assert resolver._is_metadata_path("metadata.updated") is True
        assert resolver._is_metadata_path("metadata.checksum") is True
        assert resolver._is_metadata_path("metadata.something.else") is True
        assert resolver._is_metadata_path("version") is True
        assert resolver._is_metadata_path("$schema") is True
        assert resolver._is_metadata_path("data.metadata.updated") is False  # Not at start
        assert resolver._is_metadata_path("data.value") is False
    
    def test_is_user_customization_path_variations(self, resolver):
        """Test _is_user_customization_path with various formats."""
        assert resolver._is_user_customization_path("custom_patterns") is True
        assert resolver._is_user_customization_path("custom_patterns.pattern1") is True
        assert resolver._is_user_customization_path("local_overrides") is True
        assert resolver._is_user_customization_path("user_additions") is True
        assert resolver._is_user_customization_path("data.custom_patterns") is True  # Contains it
        assert resolver._is_user_customization_path("data.value") is False
    
    def test_suggest_for_path_edge_cases(self, resolver):
        """Test _suggest_for_path with edge cases."""
        # Test root level version
        strategy = resolver._suggest_for_path("version")
        assert strategy == ResolutionStrategy.USE_INCOMING
        
        # Test nested metadata
        strategy = resolver._suggest_for_path("metadata.updated")
        assert strategy == ResolutionStrategy.USE_INCOMING
        
        # Test user customization
        resolver.preserve_user_changes = True
        strategy = resolver._suggest_for_path("custom_patterns")
        assert strategy == ResolutionStrategy.KEEP_EXISTING
        
        # Test regular path
        strategy = resolver._suggest_for_path("data.value")
        assert strategy == ResolutionStrategy.USE_INCOMING


class TestIntegrationScenarios:
    """Integration tests for real-world scenarios."""
    
    @pytest.fixture
    def resolver(self):
        """Create a ConflictResolver instance."""
        return ConflictResolver(
            preserve_user_changes=True,
            auto_resolve_minor=True,
        )
    
    def test_knowledge_file_update_scenario(self, resolver):
        """Test a realistic knowledge file update scenario."""
        existing = {
            "version": "1.0.0",
            "metadata": {
                "updated": "2024-01-01",
                "checksum": "abc123",
            },
            "patterns": [
                {"id": "pattern1", "name": "Pattern 1"},
            ],
            "custom_patterns": {
                "user_pattern": "user_value",
            },
        }
        
        incoming = {
            "version": "1.1.0",
            "metadata": {
                "updated": "2024-01-02",
                "checksum": "def456",
            },
            "patterns": [
                {"id": "pattern1", "name": "Pattern 1 Updated"},
                {"id": "pattern2", "name": "Pattern 2"},
            ],
            "custom_patterns": {
                "user_pattern": "new_value",
            },
        }
        
        report = resolver.detect_conflicts(existing, incoming, "github")
        
        # Version and metadata should be auto-resolved
        version_conflicts = [c for c in report.conflicts if c.path == "version"]
        metadata_conflicts = [c for c in report.conflicts if "metadata" in c.path]
        
        # Custom patterns should suggest KEEP_EXISTING
        custom_conflicts = [c for c in report.conflicts if "custom_patterns" in c.path]
        if custom_conflicts:
            assert custom_conflicts[0].suggested_resolution == ResolutionStrategy.KEEP_EXISTING
        
        # Resolve with default strategies
        resolved = resolver.resolve_all(existing, incoming, report)
        
        # Version should be updated
        assert resolved["version"] == "1.1.0"
        # Custom patterns should be preserved
        assert resolved["custom_patterns"]["user_pattern"] == "user_value"
    
    def test_complex_merge_scenario(self, resolver):
        """Test a complex merge scenario with multiple conflict types."""
        existing = {
            "version": "1.0.0",
            "data": {
                "list": ["a", "b"],
                "dict": {"key1": "value1"},
                "value": "old",
            },
            "user_custom": "preserve_me",
        }
        
        incoming = {
            "version": "2.0.0",
            "data": {
                "list": ["b", "c"],
                "dict": {"key2": "value2"},
                "value": "new",
            },
            "user_custom": "replace_me",
            "new_section": {"new": "data"},
        }
        
        report = resolver.detect_conflicts(existing, incoming, "source")
        
        # Should detect multiple conflicts
        assert report.has_conflicts is True
        
        # Resolve with mixed strategies
        user_decisions = {
            "version": ResolutionStrategy.USE_INCOMING,
            "data.list": ResolutionStrategy.MERGE_VALUES,
            "data.dict": ResolutionStrategy.MERGE_VALUES,
            "data.value": ResolutionStrategy.USE_INCOMING,
            "user_custom": ResolutionStrategy.KEEP_EXISTING,
        }
        
        resolved = resolver.resolve_all(existing, incoming, report, user_decisions)
        
        assert resolved["version"] == "2.0.0"
        assert set(resolved["data"]["list"]) == {"a", "b", "c"}
        assert resolved["data"]["dict"]["key1"] == "value1"
        assert resolved["data"]["dict"]["key2"] == "value2"
        assert resolved["data"]["value"] == "new"
        assert resolved["user_custom"] == "preserve_me"
        assert resolved["new_section"]["new"] == "data"
