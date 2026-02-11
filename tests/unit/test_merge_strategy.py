"""
Unit tests for scripts/git/merge_strategy.py

Tests merge strategies, conflict detection, and resolution mechanisms.
"""

import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.git.merge_strategy import (
    ConflictResolution,
    ArtifactType,
    MergeStrategy,
    DEFAULT_STRATEGIES,
    Conflict,
    ConflictPrompt,
    MergeResult,
    MergeEngine,
    merge_json_files,
    _deep_merge,
)
from scripts.analysis.repo_analyzer import RepoInventory, AntigravityruleAnalysis, McpAnalysis

class TestConflictResolution:
    """Tests for ConflictResolution enum."""
    
    def test_resolution_values(self):
        """Test that all resolutions have correct values."""
        assert ConflictResolution.KEEP_EXISTING.value == "keep"
        assert ConflictResolution.REPLACE.value == "replace"
        assert ConflictResolution.MERGE.value == "merge"
        assert ConflictResolution.RENAME_NEW.value == "rename"
        assert ConflictResolution.SKIP.value == "skip"


class TestArtifactType:
    """Tests for ArtifactType enum."""
    
    def test_artifact_type_values(self):
        """Test artifact type values."""
        assert ArtifactType.CURSORRULES.value == "cursorrules"
        assert ArtifactType.AGENT.value == "agent"
        assert ArtifactType.SKILL.value == "skill"
        assert ArtifactType.MCP_CONFIG.value == "mcp_config"
        assert ArtifactType.KNOWLEDGE.value == "knowledge"


class TestMergeStrategy:
    """Tests for MergeStrategy enum."""
    
    def test_strategy_values(self):
        """Test merge strategy values."""
        assert MergeStrategy.MERGE.value == "merge"
        assert MergeStrategy.ADD.value == "add"
        assert MergeStrategy.PRESERVE.value == "preserve"
        assert MergeStrategy.REPLACE.value == "replace"


class TestDefaultStrategies:
    """Tests for default strategy mappings."""
    
    def test_cursorrules_strategy(self):
        """Test default strategy for cursorrules."""
        assert DEFAULT_STRATEGIES[ArtifactType.CURSORRULES] == MergeStrategy.MERGE    
    def test_agent_strategy(self):
        """Test default strategy for agents."""
        assert DEFAULT_STRATEGIES[ArtifactType.AGENT] == MergeStrategy.ADD
    
    def test_command_strategy(self):
        """Test default strategy for commands (user custom)."""
        assert DEFAULT_STRATEGIES[ArtifactType.COMMAND] == MergeStrategy.PRESERVE
    
    def test_purpose_strategy(self):
        """Test default strategy for PURPOSE.md (user custom)."""
        assert DEFAULT_STRATEGIES[ArtifactType.PURPOSE] == MergeStrategy.PRESERVE


class TestConflict:
    """Tests for Conflict dataclass."""
    
    def test_conflict_creation(self):
        """Test creating a Conflict."""
        conflict = Conflict(
            artifact_type=ArtifactType.AGENT,
            artifact_name="code-reviewer",
            existing_path=Path("/repo/.agent/agents/code-reviewer.md"),
            new_content="# New content",
        )
        
        assert conflict.artifact_type == ArtifactType.AGENT
        assert conflict.artifact_name == "code-reviewer"
        assert conflict.existing_hash == ""
    
    def test_get_existing_content(self):
        """Test reading existing file content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            test_file.write_text("Existing content")
            
            conflict = Conflict(
                artifact_type=ArtifactType.AGENT,
                artifact_name="test",
                existing_path=test_file,
                new_content="New content",
            )
            
            assert conflict.get_existing_content() == "Existing content"
    
    def test_get_existing_content_nonexistent(self):
        """Test reading non-existent file returns empty string."""
        conflict = Conflict(
            artifact_type=ArtifactType.AGENT,
            artifact_name="test",
            existing_path=Path("/nonexistent/file.md"),
            new_content="New content",
        )
        
        assert conflict.get_existing_content() == ""


class TestConflictPrompt:
    """Tests for ConflictPrompt dataclass."""
    
    def test_format_prompt(self):
        """Test formatting a conflict prompt."""
        conflict = Conflict(
            artifact_type=ArtifactType.CURSORRULES,
            artifact_name=".agentrules",
            existing_path=Path("/repo/.agentrules"),
            new_content="New rules",
            diff_summary="+50 lines, -10 lines",
        )
        
        prompt = ConflictPrompt(
            conflict=conflict,
            options=[
                ConflictResolution.KEEP_EXISTING,
                ConflictResolution.REPLACE,
                ConflictResolution.MERGE,
            ],
            recommendation=ConflictResolution.MERGE,
            reason="Merge preserves customizations",
        )
        
        formatted = prompt.format_prompt()
        
        assert "CONFLICT: cursorrules" in formatted
        assert ".agentrules" in formatted
        assert "Recommendation: merge" in formatted
        assert "[1] keep" in formatted
        assert "[2] replace" in formatted
        assert "[3] merge" in formatted


class TestMergeResult:
    """Tests for MergeResult dataclass."""
    
    def test_successful_result(self):
        """Test creating a successful merge result."""
        result = MergeResult(
            success=True,
            content="Merged content",
            message="Merge successful",
        )
        
        assert result.success is True
        assert result.content == "Merged content"
    
    def test_failed_result(self):
        """Test creating a failed merge result."""
        result = MergeResult(
            success=False,
            message="Merge failed: conflicting sections",
        )
        
        assert result.success is False
        assert "failed" in result.message


class TestMergeEngine:
    """Tests for MergeEngine class."""
    
    def _create_inventory(self, tmpdir: Path) -> RepoInventory:
        """Helper to create a test inventory."""
        return RepoInventory(
            path=tmpdir,
            agentrules=AntigravityruleAnalysis(exists=True, content="# Existing rules"),
            mcp=McpAnalysis(exists=True, servers=["filesystem"]),
            existing_agents=["code-reviewer"],
            existing_skills=["tdd"],
            existing_knowledge=["patterns.json"],
        )
    
    def test_engine_creation(self):
        """Test creating a MergeEngine."""
        with tempfile.TemporaryDirectory() as tmpdir:
            inventory = self._create_inventory(Path(tmpdir))
            engine = MergeEngine(inventory)
            
            assert engine.inventory == inventory
            assert engine.resolutions == {}
    
    def test_detect_cursorrules_conflict(self):
        """Test detecting cursorrules conflict."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            cursorrules = repo_path / ".agentrules"
            cursorrules.write_text("# Existing rules")
            
            inventory = RepoInventory(
                path=repo_path,
                agentrules=AntigravityruleAnalysis(                    exists=True,
                    content="# Existing rules"
                ),
            )
            
            engine = MergeEngine(inventory)
            conflicts = engine.detect_conflicts(
                desired_agents=[],
                desired_skills=[],
                desired_knowledge=[],
                new_cursorrules="# New rules\n# Different content",
            )
            
            assert len(conflicts) == 1
            assert conflicts[0].artifact_type == ArtifactType.CURSORRULES    
    def test_detect_agent_conflict(self):
        """Test detecting agent conflict."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            agents_dir = repo_path / ".agent" / "agents"
            agents_dir.mkdir(parents=True)
            (agents_dir / "code-reviewer.md").write_text("# Existing agent")
            
            # Create factory patterns dir
            factory_root = repo_path / "factory"
            patterns_dir = factory_root / "patterns" / "agents"
            patterns_dir.mkdir(parents=True)
            (patterns_dir / "code-reviewer.json").write_text("{}")
            
            inventory = RepoInventory(
                path=repo_path,
                existing_agents=["code-reviewer"],
            )
            
            engine = MergeEngine(inventory, factory_root=factory_root)
            conflicts = engine.detect_conflicts(
                desired_agents=["code-reviewer"],
                desired_skills=[],
                desired_knowledge=[],
            )
            
            assert len(conflicts) == 1
            assert conflicts[0].artifact_type == ArtifactType.AGENT
            assert conflicts[0].artifact_name == "code-reviewer"
    
    def test_detect_skill_conflict(self):
        """Test detecting skill conflict."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            skill_dir = repo_path / ".agent" / "skills" / "tdd"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text("# Existing skill")
            
            inventory = RepoInventory(
                path=repo_path,
                existing_skills=["tdd"],
            )
            
            engine = MergeEngine(inventory)
            conflicts = engine.detect_conflicts(
                desired_agents=[],
                desired_skills=["tdd"],
                desired_knowledge=[],
            )
            
            assert len(conflicts) == 1
            assert conflicts[0].artifact_type == ArtifactType.SKILL
    
    def test_detect_mcp_conflict(self):
        """Test detecting MCP configuration conflict."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            cursor_dir = repo_path / ".agent"
            cursor_dir.mkdir()
            (cursor_dir / "mcp.json").write_text('{"mcpServers": {"git": {}}}')            
            inventory = RepoInventory(
                path=repo_path,
                mcp=McpAnalysis(exists=True, servers=["git"]),
            )
            
            engine = MergeEngine(inventory)
            conflicts = engine.detect_conflicts(
                desired_agents=[],
                desired_skills=[],
                desired_knowledge=[],
                new_mcp_servers={"git": {"command": "new"}, "filesystem": {}},
            )
            
            assert len(conflicts) == 1
            assert conflicts[0].artifact_type == ArtifactType.MCP_CONFIG
            assert "git" in conflicts[0].diff_summary
    
    def test_no_conflict_when_different_content_is_same(self):
        """Test no conflict when content is identical."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            cursorrules = repo_path / ".agentrules"
            content = "# Same content"
            cursorrules.write_text(content)
            
            inventory = RepoInventory(
                path=repo_path,
                agentrules=AntigravityruleAnalysis(exists=True, content=content),            )
            
            engine = MergeEngine(inventory)
            conflicts = engine.detect_conflicts(
                desired_agents=[],
                desired_skills=[],
                desired_knowledge=[],
                new_cursorrules=content,            )
            
            assert len(conflicts) == 0
    
    def test_get_conflict_prompt_cursorrules(self):
        """Test getting prompt for cursorrules conflict."""
        with tempfile.TemporaryDirectory() as tmpdir:
            inventory = RepoInventory(path=Path(tmpdir))
            engine = MergeEngine(inventory)
            
            conflict = Conflict(
                artifact_type=ArtifactType.CURSORRULES,
                artifact_name=".agentrules",
                existing_path=Path(tmpdir) / ".agentrules",
                new_content="New content",
            )
            
            prompt = engine.get_conflict_prompt(conflict)
            
            assert prompt.recommendation == ConflictResolution.MERGE
            assert ConflictResolution.MERGE in prompt.options
    
    def test_get_conflict_prompt_command(self):
        """Test getting prompt for command conflict (user custom)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            inventory = RepoInventory(path=Path(tmpdir))
            engine = MergeEngine(inventory)
            
            conflict = Conflict(
                artifact_type=ArtifactType.COMMAND,
                artifact_name="my-command",
                existing_path=Path(tmpdir) / ".agent" / "commands" / "my-command.md",
                new_content="New content",
            )
            
            prompt = engine.get_conflict_prompt(conflict)
            
            assert prompt.recommendation == ConflictResolution.KEEP_EXISTING
            assert ConflictResolution.REPLACE not in prompt.options
    
    def test_set_and_get_resolution(self):
        """Test setting and getting a resolution."""
        with tempfile.TemporaryDirectory() as tmpdir:
            inventory = RepoInventory(path=Path(tmpdir))
            engine = MergeEngine(inventory)
            
            conflict = Conflict(
                artifact_type=ArtifactType.AGENT,
                artifact_name="code-reviewer",
                existing_path=Path(tmpdir) / "agent.md",
                new_content="New",
            )
            
            engine.set_resolution(conflict, ConflictResolution.REPLACE)
            
            resolution = engine.get_resolution(conflict)
            assert resolution == ConflictResolution.REPLACE
    
    def test_should_skip_artifact(self):
        """Test checking if artifact should be skipped."""
        with tempfile.TemporaryDirectory() as tmpdir:
            inventory = RepoInventory(path=Path(tmpdir))
            engine = MergeEngine(inventory)
            
            conflict = Conflict(
                artifact_type=ArtifactType.AGENT,
                artifact_name="skip-me",
                existing_path=Path(tmpdir) / "agent.md",
                new_content="New",
            )
            
            # Not set - should not skip
            assert engine.should_skip_artifact(ArtifactType.AGENT, "skip-me") is False
            
            # Set to KEEP_EXISTING - should skip
            engine.set_resolution(conflict, ConflictResolution.KEEP_EXISTING)
            assert engine.should_skip_artifact(ArtifactType.AGENT, "skip-me") is True
    
    def test_should_rename_artifact(self):
        """Test checking if artifact should be renamed."""
        with tempfile.TemporaryDirectory() as tmpdir:
            inventory = RepoInventory(path=Path(tmpdir))
            engine = MergeEngine(inventory)
            
            conflict = Conflict(
                artifact_type=ArtifactType.AGENT,
                artifact_name="rename-me",
                existing_path=Path(tmpdir) / "agent.md",
                new_content="New",
            )
            
            engine.set_resolution(conflict, ConflictResolution.RENAME_NEW)
            
            assert engine.should_rename_artifact(ArtifactType.AGENT, "rename-me") is True
    
    def test_get_renamed_name_with_extension(self):
        """Test getting renamed name for file with extension."""
        with tempfile.TemporaryDirectory() as tmpdir:
            inventory = RepoInventory(path=Path(tmpdir))
            engine = MergeEngine(inventory)
            
            renamed = engine.get_renamed_name("patterns.json")
            
            assert renamed == "patterns-factory.json"
    
    def test_get_renamed_name_without_extension(self):
        """Test getting renamed name for file without extension."""
        with tempfile.TemporaryDirectory() as tmpdir:
            inventory = RepoInventory(path=Path(tmpdir))
            engine = MergeEngine(inventory)
            
            renamed = engine.get_renamed_name("code-reviewer")
            
            assert renamed == "code-reviewer-factory"


class TestMergeJsonFiles:
    """Tests for merge_json_files function."""
    
    def test_merge_simple_objects(self):
        """Test merging simple JSON objects."""
        existing = '{"key1": "value1"}'
        new = '{"key2": "value2"}'
        
        result = merge_json_files(existing, new)
        
        assert result.success is True
        merged = json.loads(result.content)
        assert merged["key1"] == "value1"
        assert merged["key2"] == "value2"
    
    def test_merge_overlapping_keys(self):
        """Test merging with overlapping keys (new takes precedence)."""
        existing = '{"key": "old_value"}'
        new = '{"key": "new_value"}'
        
        result = merge_json_files(existing, new)
        
        assert result.success is True
        merged = json.loads(result.content)
        assert merged["key"] == "new_value"
    
    def test_merge_nested_objects(self):
        """Test deep merging nested objects."""
        existing = '{"outer": {"inner1": "a"}}'
        new = '{"outer": {"inner2": "b"}}'
        
        result = merge_json_files(existing, new, strategy="deep")
        
        assert result.success is True
        merged = json.loads(result.content)
        assert merged["outer"]["inner1"] == "a"
        assert merged["outer"]["inner2"] == "b"
    
    def test_merge_arrays_no_duplicates(self):
        """Test merging arrays without duplicates."""
        existing = '{"items": ["a", "b"]}'
        new = '{"items": ["b", "c"]}'
        
        result = merge_json_files(existing, new, strategy="deep")
        
        assert result.success is True
        merged = json.loads(result.content)
        assert set(merged["items"]) == {"a", "b", "c"}
    
    def test_merge_invalid_json(self):
        """Test merging invalid JSON returns error."""
        existing = 'not valid json'
        new = '{"key": "value"}'
        
        result = merge_json_files(existing, new)
        
        assert result.success is False
        assert "JSON" in result.message
    
    def test_shallow_merge(self):
        """Test shallow merge replaces nested objects."""
        existing = '{"outer": {"inner1": "a"}}'
        new = '{"outer": {"inner2": "b"}}'
        
        result = merge_json_files(existing, new, strategy="shallow")
        
        assert result.success is True
        merged = json.loads(result.content)
        # Shallow merge replaces entirely
        assert "inner1" not in merged["outer"]
        assert merged["outer"]["inner2"] == "b"


class TestDeepMerge:
    """Tests for _deep_merge helper function."""
    
    def test_merge_flat_dicts(self):
        """Test merging flat dictionaries."""
        base = {"a": 1, "b": 2}
        overlay = {"c": 3}
        
        result = _deep_merge(base, overlay)
        
        assert result == {"a": 1, "b": 2, "c": 3}
    
    def test_merge_nested_dicts(self):
        """Test merging nested dictionaries."""
        base = {"level1": {"level2": {"a": 1}}}
        overlay = {"level1": {"level2": {"b": 2}}}
        
        result = _deep_merge(base, overlay)
        
        assert result["level1"]["level2"]["a"] == 1
        assert result["level1"]["level2"]["b"] == 2
    
    def test_overlay_takes_precedence(self):
        """Test that overlay values take precedence."""
        base = {"key": "base_value"}
        overlay = {"key": "overlay_value"}
        
        result = _deep_merge(base, overlay)
        
        assert result["key"] == "overlay_value"
    
    def test_merge_lists(self):
        """Test merging lists without duplicates."""
        base = {"items": [1, 2, 3]}
        overlay = {"items": [3, 4, 5]}
        
        result = _deep_merge(base, overlay)
        
        assert set(result["items"]) == {1, 2, 3, 4, 5}
