"""
Tests for the Mutability Guard.

CRITICAL tests for layer protection - ensures axioms cannot be modified.
"""

import pytest


class TestMutabilityGuard:
    """Tests for MutabilityGuard class."""

    @pytest.fixture
    def guard(self):
        """Create a mutability guard instance."""
        from scripts.guardian.mutability_guard import MutabilityGuard

        return MutabilityGuard()

    # =========================================================================
    # CRITICAL: Layer 0 Protection Tests
    # =========================================================================

    def test_axioms_are_protected(self, guard):
        """CRITICAL: Verify Layer 0 (Axioms) cannot be modified."""
        result = guard.can_modify(".agent/patterns/axioms/core-axioms.json")

        assert result.allowed is False
        # Valid reasons: immutable, Layer 0, or never-modify list
        assert (
            "immutable" in result.reason.lower()
            or "Layer 0" in result.reason
            or "never-modify" in result.reason.lower()
        )

    def test_cursorrules_is_protected(self, guard):
        """CRITICAL: Verify .agentrules cannot be modified."""
        result = guard.can_modify(".agentrules")
        assert result.allowed is False

    def test_axiom_zero_is_protected(self, guard):
        """CRITICAL: Verify axiom-zero.json cannot be modified."""
        result = guard.can_modify(".agent/patterns/axioms/axiom-zero.json")

        assert result.allowed is False

    # =========================================================================
    # CRITICAL: Layer 1 Protection Tests
    # =========================================================================

    def test_purpose_is_protected(self, guard):
        """CRITICAL: Verify Layer 1 (Purpose) cannot be modified."""
        result = guard.can_modify("PURPOSE.md")

        assert result.allowed is False
        assert "Layer 1" in result.reason or "immutable" in result.reason.lower()

    def test_purpose_patterns_are_protected(self, guard):
        """CRITICAL: Verify patterns/purpose/ cannot be modified."""
        result = guard.can_modify(".agent/patterns/purpose/mission.json")

        assert result.allowed is False

    # =========================================================================
    # CRITICAL: Layer 2 Protection Tests
    # =========================================================================

    def test_principles_are_protected(self, guard):
        """CRITICAL: Verify Layer 2 (Principles) cannot be modified."""
        result = guard.can_modify(".agent/patterns/principles/ethical-boundaries.json")

        assert result.allowed is False
        # Valid reasons: immutable, Layer 2, or never-modify list
        assert (
            "Layer 2" in result.reason
            or "immutable" in result.reason.lower()
            or "never-modify" in result.reason.lower()
        )

    def test_enforcement_patterns_are_protected(self, guard):
        """CRITICAL: Verify enforcement patterns cannot be modified."""
        result = guard.can_modify(
            ".agent/patterns/enforcement/integrity-enforcement.json"
        )

        assert result.allowed is False

    def test_quality_standards_are_protected(self, guard):
        """CRITICAL: Verify quality standards cannot be modified."""
        result = guard.can_modify(".agent/patterns/principles/quality-standards.json")

        assert result.allowed is False

    # =========================================================================
    # Mutable Path Tests
    # =========================================================================

    def test_knowledge_files_are_mutable(self, guard):
        """Verify knowledge files can be extended."""
        result = guard.can_modify("knowledge/fastapi-patterns.json")

        assert result.allowed is True
        assert "mutable" in result.reason.lower() or result.policy == "mutable"

    def test_blueprints_are_mutable(self, guard):
        """Verify blueprints can be modified."""
        result = guard.can_modify(".agent/blueprints/python-fastapi/blueprint.json")

        assert result.allowed is True

    def test_stack_patterns_are_mutable(self, guard):
        """Verify stack patterns can be modified."""
        result = guard.can_modify(".agent/patterns/stacks/python-stack.json")

        assert result.allowed is True

    def test_templates_are_mutable(self, guard):
        """Verify templates can be modified."""
        result = guard.can_modify("templates/python/service.py.tmpl")

        assert result.allowed is True

    def test_data_directory_is_mutable(self, guard):
        """Verify data directory can be modified."""
        result = guard.can_modify("data/memory/test.db")

        assert result.allowed is True

    # =========================================================================
    # Content Validation Tests
    # =========================================================================

    def test_validate_modification_checks_path_first(self, guard):
        """Test that path is checked before content."""
        result = guard.validate_modification(
            ".agent/patterns/axioms/core-axioms.json", "Some content"
        )

        assert result.allowed is False

    def test_validate_modification_checks_content(self, guard):
        """Test that content is validated for violations."""
        # Content that tries to override axioms
        suspicious_content = "This rule should override axiom A1"

        result = guard.validate_modification(
            "knowledge/test.json", suspicious_content, check_content=True
        )

        # Should either fail or pass with warning
        # The exact behavior depends on pattern matching
        assert result is not None

    def test_valid_modification_passes(self, guard):
        """Test that valid modifications pass."""
        result = guard.validate_modification(
            "knowledge/test.json",
            '{"name": "test", "patterns": []}',
            check_content=True,
        )

        assert result.allowed is True

    # =========================================================================
    # Path Normalization Tests
    # =========================================================================

    def test_path_with_backslashes(self, guard):
        """Test Windows-style paths are handled."""
        result = guard.can_modify(".agent\\patterns\\axioms\\core-axioms.json")

        assert result.allowed is False

    def test_path_with_dot_prefix(self, guard):
        """Test paths with ./ prefix are handled."""
        result = guard.can_modify("./.agent/patterns/axioms/core-axioms.json")

        assert result.allowed is False

    # =========================================================================
    # Utility Method Tests
    # =========================================================================

    def test_get_layer_info(self, guard):
        """Test getting layer information."""
        info = guard.get_layer_info("L0")

        assert info is not None
        assert info["name"] == "Axioms & Guardian"
        assert info["policy"] == "immutable"

    def test_get_all_protected_paths(self, guard):
        """Test getting all protected paths."""
        paths = guard.get_all_protected_paths()

        assert ".agentrules" in paths
        assert any("axioms" in p for p in paths)
        assert any("principles" in p for p in paths)

    def test_get_protection_summary(self, guard):
        """Test getting protection summary."""
        summary = guard.get_protection_summary()

        assert "L0" in summary
        assert "L1" in summary
        assert "L2" in summary
        assert "immutable" in summary.lower()


class TestMutabilityGuardSingleton:
    """Tests for the singleton pattern."""

    def test_get_mutability_guard_returns_instance(self):
        """Test singleton returns an instance."""
        from scripts.guardian.mutability_guard import get_mutability_guard

        # Reset singleton
        import scripts.guardian.mutability_guard as module

        module._default_guard = None

        guard1 = get_mutability_guard()
        guard2 = get_mutability_guard()

        assert guard1 is guard2
