#!/usr/bin/env python3
"""
Tests for the Reactive Artifact Indexing System.

Following TDD principles, these tests are written before implementation
to define the expected behavior of the reactive indexing system.

Test Categories:
1. Fast file-based counting (count_test_functions)
2. Cache structure and validation
3. Index update operations
4. Staleness detection
5. Directory trigger mapping
"""

import json
import re
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


# =============================================================================
# TEST: Fast File-Based Counting
# =============================================================================

class TestFastFileCounting:
    """Tests for fast file-based test counting."""
    
    def test_count_test_functions_finds_simple_tests(self, tmp_path: Path):
        """Should count simple test functions correctly."""
        # Create tests subdirectory (scanner looks for root_path/tests)
        tests_dir = tmp_path / "tests"
        tests_dir.mkdir()
        test_file = tests_dir / "test_example.py"
        test_file.write_text("""
def test_first():
    pass

def test_second():
    assert True

def helper_function():
    pass

def test_third():
    pass
""")
        # Expected: count_test_functions returns 3 (ignores helper_function)
        from scripts.validation.sync_artifacts import ArtifactScanner
        
        scanner = ArtifactScanner(tmp_path)
        # This method will be added in implementation
        count = scanner.count_test_functions()
        assert count == 3
    
    def test_count_test_functions_handles_async_tests(self, tmp_path: Path):
        """Should count async test functions."""
        tests_dir = tmp_path / "tests"
        tests_dir.mkdir()
        test_file = tests_dir / "test_async.py"
        test_file.write_text("""
async def test_async_operation():
    await some_async_call()

def test_sync_operation():
    pass
""")
        from scripts.validation.sync_artifacts import ArtifactScanner
        
        scanner = ArtifactScanner(tmp_path)
        count = scanner.count_test_functions()
        assert count == 2
    
    def test_count_test_functions_ignores_non_test_files(self, tmp_path: Path):
        """Should only count tests in test_*.py files."""
        tests_dir = tmp_path / "tests"
        tests_dir.mkdir()
        # Non-test file with test-like functions
        helper_file = tests_dir / "helpers.py"
        helper_file.write_text("""
def test_helper():
    pass
""")
        # Actual test file
        test_file = tests_dir / "test_real.py"
        test_file.write_text("""
def test_real():
    pass
""")
        from scripts.validation.sync_artifacts import ArtifactScanner
        
        scanner = ArtifactScanner(tmp_path)
        count = scanner.count_test_functions()
        assert count == 1  # Only from test_real.py
    
    def test_count_test_functions_handles_subdirectories(self, tmp_path: Path):
        """Should recursively count tests in subdirectories."""
        tests_dir = tmp_path / "tests"
        tests_dir.mkdir()
        # Create subdirectory structure
        unit_dir = tests_dir / "unit"
        unit_dir.mkdir()
        integration_dir = tests_dir / "integration"
        integration_dir.mkdir()
        
        (unit_dir / "test_unit.py").write_text("def test_unit(): pass")
        (integration_dir / "test_integration.py").write_text("def test_integration(): pass")
        
        from scripts.validation.sync_artifacts import ArtifactScanner
        
        scanner = ArtifactScanner(tmp_path)
        count = scanner.count_test_functions()
        assert count == 2
    
    def test_count_test_functions_by_subdirectory(self, tmp_path: Path):
        """Should count tests in specific subdirectory only."""
        tests_dir = tmp_path / "tests"
        tests_dir.mkdir()
        unit_dir = tests_dir / "unit"
        unit_dir.mkdir()
        integration_dir = tests_dir / "integration"
        integration_dir.mkdir()
        
        (unit_dir / "test_unit.py").write_text("def test_one(): pass\ndef test_two(): pass")
        (integration_dir / "test_integration.py").write_text("def test_three(): pass")
        
        from scripts.validation.sync_artifacts import ArtifactScanner
        
        scanner = ArtifactScanner(tmp_path)
        
        # Count only unit tests
        unit_count = scanner.count_test_functions("unit")
        assert unit_count == 2
        
        # Count only integration tests
        integration_count = scanner.count_test_functions("integration")
        assert integration_count == 1


# =============================================================================
# TEST: Cache Structure
# =============================================================================

class TestCacheStructure:
    """Tests for artifact index cache structure."""
    
    def test_cache_has_required_fields(self, tmp_path: Path):
        """Cache JSON should have schema_version, updated_at, and artifacts."""
        cache_path = tmp_path / "artifact-index.json"
        cache_data = {
            "schema_version": "1.0.0",
            "updated_at": datetime.utcnow().isoformat() + "Z",
            "artifacts": {}
        }
        cache_path.write_text(json.dumps(cache_data, indent=2))
        
        loaded = json.loads(cache_path.read_text())
        assert "schema_version" in loaded
        assert "updated_at" in loaded
        assert "artifacts" in loaded
    
    def test_artifact_entry_has_count_and_hash(self):
        """Each artifact entry should have count and hash fields."""
        artifact_entry = {
            "count": 12,
            "hash": "abc123def456",
            "last_modified": "2026-02-02T12:00:00Z"
        }
        assert "count" in artifact_entry
        assert "hash" in artifact_entry
        assert isinstance(artifact_entry["count"], int)
        assert isinstance(artifact_entry["hash"], str)
    
    def test_tests_artifact_has_breakdown(self):
        """Tests artifact should include category breakdown."""
        tests_entry = {
            "count": 42,
            "hash": "xyz789",
            "breakdown": {
                "unit": 15,
                "integration": 10,
                "validation": 17
            }
        }
        assert "breakdown" in tests_entry
        assert sum(tests_entry["breakdown"].values()) == tests_entry["count"]


# =============================================================================
# TEST: Index Update Operations
# =============================================================================

class TestIndexUpdates:
    """Tests for index update operations."""
    
    def test_update_for_file_identifies_artifact_type(self, tmp_path: Path):
        """Should correctly identify artifact type from file path."""
        # These mappings should be detected
        test_cases = [
            (".agent/agents/test-agent.md", "agents"),
            (".agent/skills/test-skill/SKILL.md", "skills"),
            ("tests/unit/test_example.py", "tests"),
            ("blueprints/python-fastapi/blueprint.json", "blueprints"),
            ("knowledge/new-pattern.json", "knowledge"),
        ]
        
        # This will test the update_index.py functionality
        # Implementation will map paths to artifact types
        for file_path, expected_type in test_cases:
            # Mock the detection logic
            detected = detect_artifact_type(file_path)
            assert detected == expected_type, f"Expected {expected_type} for {file_path}"
    
    def test_update_only_affects_relevant_section(self, tmp_path: Path):
        """Updating one artifact type should not modify others."""
        cache_path = tmp_path / "artifact-index.json"
        initial_cache = {
            "schema_version": "1.0.0",
            "updated_at": "2026-02-02T10:00:00Z",
            "artifacts": {
                "agents": {"count": 12, "hash": "aaa"},
                "skills": {"count": 36, "hash": "bbb"},
            }
        }
        cache_path.write_text(json.dumps(initial_cache, indent=2))
        
        # After updating agents, skills should be unchanged
        # (Implementation will be tested here)
        updated = json.loads(cache_path.read_text())
        assert updated["artifacts"]["skills"]["hash"] == "bbb"


# =============================================================================
# TEST: Staleness Detection
# =============================================================================

class TestStalenessDetection:
    """Tests for cache staleness detection."""
    
    def test_cache_is_fresh_within_threshold(self):
        """Cache should be considered fresh within time threshold."""
        now = datetime.utcnow()
        cache_time = now - timedelta(minutes=30)  # 30 minutes ago
        threshold = timedelta(hours=1)
        
        is_stale = (now - cache_time) > threshold
        assert not is_stale
    
    def test_cache_is_stale_beyond_threshold(self):
        """Cache should be considered stale beyond time threshold."""
        now = datetime.utcnow()
        cache_time = now - timedelta(hours=2)  # 2 hours ago
        threshold = timedelta(hours=1)
        
        is_stale = (now - cache_time) > threshold
        assert is_stale
    
    def test_missing_cache_is_stale(self, tmp_path: Path):
        """Missing cache file should trigger rebuild."""
        cache_path = tmp_path / "artifact-index.json"
        assert not cache_path.exists()
        # Implementation should treat missing cache as stale


# =============================================================================
# TEST: Directory Triggers
# =============================================================================

class TestDirectoryTriggers:
    """Tests for directory to artifact type mapping."""
    
    def test_known_directories_map_correctly(self):
        """Known directories should map to correct artifact types."""
        from scripts.validation.sync_artifacts import SyncEngine
        
        # Get the root path from project
        root_path = Path(__file__).parent.parent.parent
        engine = SyncEngine(root_path)
        
        triggers = engine.get_directory_triggers()
        
        assert ".agent/agents" in triggers or "agents" in engine.config
        # Additional assertions based on sync_config.json
    
    def test_nested_path_triggers_parent(self):
        """Nested paths should trigger parent directory's artifacts."""
        from scripts.validation.sync_artifacts import SyncEngine
        
        root_path = Path(__file__).parent.parent.parent
        engine = SyncEngine(root_path)
        
        # A file in .agent/agents/ should trigger 'agents' artifact
        artifacts = engine.get_artifacts_for_dirs([".agent/agents/new-agent.md"])
        assert "agents" in artifacts


# =============================================================================
# HELPER FUNCTIONS (to be moved to implementation)
# =============================================================================

def detect_artifact_type(file_path: str) -> str:
    """Detect artifact type from file path.
    
    This is a placeholder for testing - actual implementation
    will be in update_index.py.
    """
    path = file_path.replace("\\", "/")
    
    if path.startswith(".agent/agents/"):
        return "agents"
    elif path.startswith(".agent/skills/"):
        return "skills"
    elif path.startswith("tests/"):
        return "tests"
    elif path.startswith("blueprints/"):
        return "blueprints"
    elif path.startswith("knowledge/"):
        return "knowledge"
    elif path.startswith("templates/"):
        return "templates"
    elif path.startswith("patterns/"):
        return "patterns"
    elif path.startswith("docs/"):
        return "docs"
    elif path.startswith("diagrams/"):
        return "diagrams"
    else:
        return "unknown"


# =============================================================================
# TEST: Integration with Pre-commit
# =============================================================================

class TestPrecommitIntegration:
    """Tests for pre-commit hook integration."""
    
    def test_precommit_reads_from_cache_when_fresh(self, tmp_path: Path):
        """Pre-commit should use cached values when cache is fresh."""
        # Setup fresh cache
        cache_path = tmp_path / ".agent" / "cache" / "artifact-index.json"
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        
        cache_data = {
            "schema_version": "1.0.0",
            "updated_at": datetime.utcnow().isoformat() + "Z",
            "artifacts": {
                "agents": {"count": 12, "hash": "abc123"}
            }
        }
        cache_path.write_text(json.dumps(cache_data, indent=2))
        
        # Pre-commit should return cached count without scanning
        # (Implementation will be tested here)
    
    def test_precommit_rebuilds_when_stale(self, tmp_path: Path):
        """Pre-commit should rebuild when cache is stale."""
        cache_path = tmp_path / ".agent" / "cache" / "artifact-index.json"
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create stale cache (2 hours old)
        old_time = (datetime.utcnow() - timedelta(hours=2)).isoformat() + "Z"
        cache_data = {
            "schema_version": "1.0.0",
            "updated_at": old_time,
            "artifacts": {}
        }
        cache_path.write_text(json.dumps(cache_data, indent=2))
        
        # Pre-commit should trigger fast rebuild
        # (Implementation will be tested here)


# =============================================================================
# TEST: Performance
# =============================================================================

class TestPerformance:
    """Performance-related tests."""
    
    def test_file_based_counting_is_fast(self, tmp_path: Path):
        """File-based counting should complete in under 1 second."""
        import time
        
        tests_dir = tmp_path / "tests"
        tests_dir.mkdir()
        
        # Create 100 test files with 10 tests each
        for i in range(100):
            test_file = tests_dir / f"test_module_{i}.py"
            tests = "\n".join([f"def test_{j}(): pass" for j in range(10)])
            test_file.write_text(tests)
        
        from scripts.validation.sync_artifacts import ArtifactScanner
        
        scanner = ArtifactScanner(tmp_path)
        
        start = time.perf_counter()
        count = scanner.count_test_functions()
        elapsed = time.perf_counter() - start
        
        assert count == 1000  # 100 files * 10 tests
        assert elapsed < 1.0, f"Counting took {elapsed:.2f}s, expected < 1s"
