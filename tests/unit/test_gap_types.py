"""
Unit tests for gap types and enums in scripts/analysis/knowledge_gap_analyzer.py

Tests for GapType and GapPriority enumerations.
"""

import sys
from pathlib import Path

import pytest

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.analysis.knowledge_gap_analyzer import GapType, GapPriority


class TestGapType:
    """Tests for GapType enumeration."""

    def test_all_gap_types_defined(self):
        """Test that all expected gap types are defined."""
        expected_types = {"MISSING", "SHALLOW", "STALE", "CROSS_REF", "INCOMPLETE"}
        actual_types = {gt.name for gt in GapType}

        assert expected_types == actual_types

    def test_gap_type_values(self):
        """Test gap type string values."""
        assert GapType.MISSING.value == "missing"
        assert GapType.SHALLOW.value == "shallow"
        assert GapType.STALE.value == "stale"
        assert GapType.CROSS_REF.value == "cross_reference"
        assert GapType.INCOMPLETE.value == "incomplete"

    def test_gap_type_from_value(self):
        """Test creating GapType from value."""
        assert GapType("missing") == GapType.MISSING
        assert GapType("shallow") == GapType.SHALLOW

    def test_gap_type_invalid_value(self):
        """Test that invalid value raises error."""
        with pytest.raises(ValueError):
            GapType("invalid_type")

    def test_gap_type_iteration(self):
        """Test iterating over all gap types."""
        types = list(GapType)

        assert len(types) == 5
        assert GapType.MISSING in types


class TestGapPriority:
    """Tests for GapPriority enumeration."""

    def test_all_priorities_defined(self):
        """Test that all expected priorities are defined."""
        expected = {"CRITICAL", "HIGH", "MEDIUM", "LOW"}
        actual = {gp.name for gp in GapPriority}

        assert expected == actual

    def test_priority_values(self):
        """Test priority numeric values."""
        assert GapPriority.CRITICAL.value == 1
        assert GapPriority.HIGH.value == 2
        assert GapPriority.MEDIUM.value == 3
        assert GapPriority.LOW.value == 4

    def test_priority_ordering(self):
        """Test that priorities can be compared."""
        assert GapPriority.CRITICAL.value < GapPriority.HIGH.value
        assert GapPriority.HIGH.value < GapPriority.MEDIUM.value
        assert GapPriority.MEDIUM.value < GapPriority.LOW.value

    def test_priority_sorting(self):
        """Test sorting priorities by value."""
        priorities = [GapPriority.LOW, GapPriority.CRITICAL, GapPriority.HIGH]
        sorted_priorities = sorted(priorities, key=lambda p: p.value)

        assert sorted_priorities[0] == GapPriority.CRITICAL
        assert sorted_priorities[1] == GapPriority.HIGH
        assert sorted_priorities[2] == GapPriority.LOW

    def test_priority_from_value(self):
        """Test creating GapPriority from value."""
        assert GapPriority(1) == GapPriority.CRITICAL
        assert GapPriority(4) == GapPriority.LOW
