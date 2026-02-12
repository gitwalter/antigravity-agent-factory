"""
CRITICAL Regression Tests for Axiom Protection.

These tests ensure that axioms remain IDENTICAL after any number of
learning cycles. This is the most important test in the memory system.
"""

import pytest
import tempfile
import shutil
import json
from pathlib import Path

# Check if chromadb is available
try:
    import chromadb
    HAS_CHROMADB = True
except ImportError:
    HAS_CHROMADB = False


@pytest.mark.skipif(not HAS_CHROMADB, reason="chromadb not installed")
class TestNoAxiomDrift:
    """
    CRITICAL: Regression tests ensuring axioms never change.
    
    These tests verify that no matter how many observations are made
    and proposals are accepted, the core axioms remain unchanged.
    """
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for test data."""
        temp_path = tempfile.mkdtemp()
        yield temp_path
        shutil.rmtree(temp_path, ignore_errors=True)
    
    @pytest.fixture
    def engine(self, temp_dir):
        """Create an induction engine with temp storage."""
        from scripts.memory.memory_store import MemoryStore
        from scripts.memory.induction_engine import InductionEngine
        
        store = MemoryStore(persist_dir=temp_dir)
        return InductionEngine(memory_store=store)
    
    def _read_file_if_exists(self, path: str) -> str:
        """Read a file if it exists, return empty string otherwise."""
        file_path = Path(path)
        if file_path.exists():
            return file_path.read_text(encoding='utf-8')
        return ""
    
    def _get_protected_files_snapshot(self) -> dict:
        """Get a snapshot of all protected files."""
        protected_files = [
            ".agent/patterns/axioms/core-axioms.json",
            ".agent/patterns/axioms/axiom-zero.json",
            ".agent/patterns/principles/ethical-boundaries.json",
            ".agent/patterns/principles/quality-standards.json",
            ".agent/patterns/enforcement/integrity-enforcement.json",
            ".agent/patterns/enforcement/safety-enforcement.json",
            ".agentrules",        ]
        
        snapshot = {}
        for path in protected_files:
            snapshot[path] = self._read_file_if_exists(path)
        
        return snapshot
    
    def test_axioms_unchanged_after_learning(self, engine):
        """
        CRITICAL: Verify axioms remain identical after learning cycles.
        
        This test simulates many observation and acceptance cycles and
        verifies that no protected files have been modified.
        """
        # Take initial snapshot
        original_snapshot = self._get_protected_files_snapshot()
        
        # Run many learning cycles
        observations = [
            {"type": "user_correction", "content": "Use pytest for testing"},
            {"type": "explicit_teaching", "content": "Always add type hints"},
            {"type": "preference", "content": "Prefer black for formatting"},
            {"type": "error_resolution", "content": "Fix import errors by checking path"},
            {"type": "successful_pattern", "content": "FastAPI with SQLAlchemy works well"},
        ]
        
        for _ in range(20):  # 20 cycles
            for obs in observations:
                proposal = engine.observe(obs)
                if proposal:
                    # Accept all proposals
                    try:
                        engine.accept_proposal(proposal.id)
                    except Exception:
                        pass  # Some may fail if similar
        
        # Take final snapshot
        final_snapshot = self._get_protected_files_snapshot()
        
        # CRITICAL ASSERTION: All protected files must be identical
        for path, original_content in original_snapshot.items():
            final_content = final_snapshot[path]
            assert original_content == final_content, \
                f"CRITICAL: Protected file {path} was modified!"
    
    def test_axiom_files_not_in_mutable_paths(self):
        """
        Verify that axiom files are not accidentally in mutable paths.
        """
        from scripts.guardian.mutability_guard import MutabilityGuard, MUTABLE_PATHS
        
        guard = MutabilityGuard()
        
        axiom_files = [
            ".agent/patterns/axioms/core-axioms.json",
            ".agent/patterns/axioms/axiom-zero.json",
            ".agentrules",        ]
        
        for axiom_file in axiom_files:
            # Should not be in any mutable path
            for mutable_path in MUTABLE_PATHS:
                assert not axiom_file.startswith(mutable_path), \
                    f"Axiom file {axiom_file} is in mutable path {mutable_path}!"
            
            # Should be explicitly protected
            result = guard.can_modify(axiom_file)
            assert not result.allowed, \
                f"Axiom file {axiom_file} is not protected!"
    
    def test_guard_blocks_all_layer0_modifications(self):
        """
        Verify that ALL Layer 0 paths are blocked.
        """
        from scripts.guardian.mutability_guard import MutabilityGuard, PROTECTED_LAYERS
        
        guard = MutabilityGuard()
        
        for path in PROTECTED_LAYERS["L0"]["paths"]:
            result = guard.can_modify(path)
            assert not result.allowed, \
                f"Layer 0 path {path} is not protected!"
    
    def test_guard_blocks_all_layer1_modifications(self):
        """
        Verify that ALL Layer 1 paths are blocked.
        """
        from scripts.guardian.mutability_guard import MutabilityGuard, PROTECTED_LAYERS
        
        guard = MutabilityGuard()
        
        for path in PROTECTED_LAYERS["L1"]["paths"]:
            result = guard.can_modify(path)
            assert not result.allowed, \
                f"Layer 1 path {path} is not protected!"
    
    def test_guard_blocks_all_layer2_modifications(self):
        """
        Verify that ALL Layer 2 paths are blocked.
        """
        from scripts.guardian.mutability_guard import MutabilityGuard, PROTECTED_LAYERS
        
        guard = MutabilityGuard()
        
        for path in PROTECTED_LAYERS["L2"]["paths"]:
            result = guard.can_modify(path)
            assert not result.allowed, \
                f"Layer 2 path {path} is not protected!"
    
    def test_induction_engine_respects_guard(self, engine):
        """
        Verify that InductionEngine uses the guard correctly.
        """
        assert engine.guard is not None
        
        # Guard should block axiom modifications
        result = engine.guard.can_modify(".agent/patterns/axioms/core-axioms.json")
        assert not result.allowed
    
    def test_memory_store_does_not_touch_protected_files(self, temp_dir):
        """
        Verify MemoryStore only writes to its own directory.
        """
        from scripts.memory.memory_store import MemoryStore
        
        store = MemoryStore(persist_dir=temp_dir)
        
        # Add memories
        for i in range(10):
            store.add_memory(
                f"Test memory {i}",
                {"source": "test"},
                "semantic"
            )
        
        # Verify no protected files were created in temp_dir
        protected_patterns = ["axiom", "principle", "enforcement", "cursorrules"]        
        for pattern in protected_patterns:
            matches = list(Path(temp_dir).rglob(f"*{pattern}*"))
            assert len(matches) == 0, \
                f"Protected file pattern '{pattern}' found in memory directory!"


class TestAxiomIntegrity:
    """
    Additional integrity checks for axiom protection.
    """
    
    def test_core_axioms_file_has_correct_structure(self):
        """
        Verify core-axioms.json has the expected structure.
        """
        axioms_path = Path(".agent/patterns/axioms/core-axioms.json")
        
        if axioms_path.exists():
            with open(axioms_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Should have axioms list
            assert "axioms" in data
            
            # Should have all 5 core axioms
            axiom_ids = [a.get("axiomId", "") for a in data["axioms"]]
            expected_axioms = [
                "A1_verifiability",
                "A2_user_primacy",
                "A3_transparency",
                "A4_non_harm",
                "A5_consistency"
            ]
            
            for expected in expected_axioms:
                assert expected in axiom_ids, \
                    f"Missing axiom {expected} in core-axioms.json"
    
    def test_never_modify_list_includes_critical_files(self):
        """
        Verify NEVER_MODIFY list includes all critical files.
        """
        from scripts.guardian.mutability_guard import NEVER_MODIFY
        
        critical_files = [
            ".agentrules",            ".agent/patterns/axioms/core-axioms.json",
        ]
        
        for critical in critical_files:
            assert critical in NEVER_MODIFY, \
                f"Critical file {critical} not in NEVER_MODIFY list!"
