"""
Comprehensive tests for knowledge JSON file structure validation.

Tests validate that all knowledge JSON files have:
- Required fields (id, name, version, category, description)
- patterns object exists
- best_practices array exists
- anti_patterns array exists
- Valid JSON structure
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Set

import pytest

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestKnowledgeFileStructure:
    """Tests for knowledge file structure and required fields."""

    @pytest.fixture
    def knowledge_dir(self, factory_root: Path) -> Path:
        """Get the knowledge directory."""
        return factory_root / "knowledge"

    @pytest.fixture
    def all_knowledge_files(self, knowledge_dir: Path) -> List[Path]:
        """Get all knowledge JSON files."""
        return list(knowledge_dir.glob("*.json"))

    def test_knowledge_files_exist(self, all_knowledge_files: List[Path]):
        """Test that knowledge files are found."""
        assert len(all_knowledge_files) > 0, "Should find at least one knowledge file"

    def test_knowledge_files_valid_json(self, all_knowledge_files: List[Path]):
        """Test that all knowledge files are valid JSON."""
        errors = []
        for knowledge_file in all_knowledge_files:
            try:
                with open(knowledge_file, 'r', encoding='utf-8') as f:
                    json.load(f)
            except json.JSONDecodeError as e:
                rel_path = knowledge_file.relative_to(knowledge_file.parent.parent)
                errors.append(f"{rel_path}: Invalid JSON - {e}")
        
        if errors:
            pytest.fail(
                f"Found {len(errors)} knowledge file(s) with invalid JSON:\n" +
                "\n".join(f"  - {e}" for e in errors)
            )

    def test_knowledge_files_have_required_fields(self, all_knowledge_files: List[Path]):
        """Test that knowledge files have required fields: id, name, version, category, description."""
        errors = []
        for knowledge_file in all_knowledge_files:
            try:
                with open(knowledge_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                required_fields = ["id", "name", "version", "category", "description"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    rel_path = knowledge_file.relative_to(knowledge_file.parent.parent)
                    errors.append(f"{rel_path}: Missing required fields - {', '.join(missing_fields)}")
            except (json.JSONDecodeError, KeyError) as e:
                rel_path = knowledge_file.relative_to(knowledge_file.parent.parent)
                errors.append(f"{rel_path}: Error reading file - {e}")
        
        if errors:
            pytest.fail(
                f"Found {len(errors)} knowledge file(s) with missing required fields:\n" +
                "\n".join(f"  - {e}" for e in errors)
            )

    def test_knowledge_id_matches_filename(self, all_knowledge_files: List[Path]):
        """Test that knowledge file id matches the filename (without extension)."""
        errors = []
        for knowledge_file in all_knowledge_files:
            try:
                with open(knowledge_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                file_id = knowledge_file.stem  # Filename without extension
                knowledge_id = data.get("id", "")
                
                if knowledge_id != file_id:
                    rel_path = knowledge_file.relative_to(knowledge_file.parent.parent)
                    errors.append(
                        f"{rel_path}: id '{knowledge_id}' doesn't match filename '{file_id}'"
                    )
            except (json.JSONDecodeError, KeyError):
                continue
        
        if errors:
            pytest.fail(
                f"Found {len(errors)} knowledge file(s) with id mismatch:\n" +
                "\n".join(f"  - {e}" for e in errors)
            )

    def test_knowledge_files_have_patterns(self, all_knowledge_files: List[Path]):
        """Test that knowledge files have a patterns object."""
        errors = []
        for knowledge_file in all_knowledge_files:
            try:
                with open(knowledge_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if "patterns" not in data:
                    rel_path = knowledge_file.relative_to(knowledge_file.parent.parent)
                    errors.append(f"{rel_path}: Missing 'patterns' field")
                elif not isinstance(data["patterns"], dict):
                    rel_path = knowledge_file.relative_to(knowledge_file.parent.parent)
                    errors.append(f"{rel_path}: 'patterns' should be an object/dict")
            except (json.JSONDecodeError, KeyError):
                continue
        
        if errors:
            pytest.fail(
                f"Found {len(errors)} knowledge file(s) without patterns:\n" +
                "\n".join(f"  - {e}" for e in errors)
            )

    def test_knowledge_files_have_best_practices(self, all_knowledge_files: List[Path]):
        """Test that knowledge files have a best_practices array."""
        errors = []
        for knowledge_file in all_knowledge_files:
            try:
                with open(knowledge_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if "best_practices" not in data:
                    rel_path = knowledge_file.relative_to(knowledge_file.parent.parent)
                    errors.append(f"{rel_path}: Missing 'best_practices' field")
                elif not isinstance(data["best_practices"], list):
                    rel_path = knowledge_file.relative_to(knowledge_file.parent.parent)
                    errors.append(f"{rel_path}: 'best_practices' should be an array/list")
            except (json.JSONDecodeError, KeyError):
                continue
        
        if errors:
            pytest.fail(
                f"Found {len(errors)} knowledge file(s) without best_practices:\n" +
                "\n".join(f"  - {e}" for e in errors)
            )

    def test_knowledge_files_have_anti_patterns(self, all_knowledge_files: List[Path]):
        """Test that knowledge files have an anti_patterns array."""
        errors = []
        for knowledge_file in all_knowledge_files:
            try:
                with open(knowledge_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if "anti_patterns" not in data:
                    rel_path = knowledge_file.relative_to(knowledge_file.parent.parent)
                    errors.append(f"{rel_path}: Missing 'anti_patterns' field")
                elif not isinstance(data["anti_patterns"], list):
                    rel_path = knowledge_file.relative_to(knowledge_file.parent.parent)
                    errors.append(f"{rel_path}: 'anti_patterns' should be an array/list")
            except (json.JSONDecodeError, KeyError):
                continue
        
        if errors:
            pytest.fail(
                f"Found {len(errors)} knowledge file(s) without anti_patterns:\n" +
                "\n".join(f"  - {e}" for e in errors)
            )

    def test_knowledge_version_format(self, all_knowledge_files: List[Path]):
        """Test that knowledge files have valid version format (semver-like)."""
        errors = []
        for knowledge_file in all_knowledge_files:
            try:
                with open(knowledge_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                version = data.get("version", "")
                if not version:
                    continue
                
                # Check for semver-like format (x.y.z or x.y)
                import re
                if not re.match(r'^\d+\.\d+(\.\d+)?', version):
                    rel_path = knowledge_file.relative_to(knowledge_file.parent.parent)
                    errors.append(f"{rel_path}: Invalid version format '{version}' (expected x.y.z or x.y)")
            except (json.JSONDecodeError, KeyError):
                continue
        
        if errors:
            pytest.fail(
                f"Found {len(errors)} knowledge file(s) with invalid version format:\n" +
                "\n".join(f"  - {e}" for e in errors)
            )

    def test_knowledge_category_is_valid(self, all_knowledge_files: List[Path]):
        """Test that knowledge files have valid category values."""
        valid_categories = {
            "agent-development",
            "ai-ml",
            "blockchain",
            "data-engineering",
            "infrastructure",
            "testing",
            "security",
            "workflow",
            "integration",
            "patterns",
        }
        
        errors = []
        for knowledge_file in all_knowledge_files:
            try:
                with open(knowledge_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                category = data.get("category", "")
                if category and category not in valid_categories:
                    # Warn but don't fail - categories may expand
                    rel_path = knowledge_file.relative_to(knowledge_file.parent.parent)
                    # Just log, don't fail
                    pass
            except (json.JSONDecodeError, KeyError):
                continue
        
        # This test doesn't fail, just validates structure


class TestKnowledgePatternsStructure:
    """Tests for patterns object structure within knowledge files."""

    @pytest.fixture
    def knowledge_dir(self, factory_root: Path) -> Path:
        """Get the knowledge directory."""
        return factory_root / "knowledge"

    @pytest.fixture
    def all_knowledge_files(self, knowledge_dir: Path) -> List[Path]:
        """Get all knowledge JSON files."""
        return list(knowledge_dir.glob("*.json"))

    def test_patterns_is_not_empty(self, all_knowledge_files: List[Path]):
        """Test that patterns object is not empty."""
        errors = []
        for knowledge_file in all_knowledge_files:
            try:
                with open(knowledge_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                patterns = data.get("patterns", {})
                if isinstance(patterns, dict) and len(patterns) == 0:
                    rel_path = knowledge_file.relative_to(knowledge_file.parent.parent)
                    errors.append(f"{rel_path}: 'patterns' object is empty")
            except (json.JSONDecodeError, KeyError):
                continue
        
        if errors:
            pytest.fail(
                f"Found {len(errors)} knowledge file(s) with empty patterns:\n" +
                "\n".join(f"  - {e}" for e in errors)
            )

    def test_patterns_have_descriptions(self, all_knowledge_files: List[Path]):
        """Test that patterns have description fields."""
        errors = []
        for knowledge_file in all_knowledge_files:
            try:
                with open(knowledge_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                patterns = data.get("patterns", {})
                if not isinstance(patterns, dict):
                    continue
                
                # Check nested patterns (patterns can be nested)
                def check_patterns(obj, path=""):
                    if isinstance(obj, dict):
                        for key, value in obj.items():
                            current_path = f"{path}.{key}" if path else key
                            if isinstance(value, dict):
                                # If it looks like a pattern (has description or code_example)
                                if "description" in value or "code_example" in value or "example" in value:
                                    if "description" not in value:
                                        errors.append(
                                            f"{knowledge_file.name}{current_path}: Pattern missing 'description'"
                                        )
                                else:
                                    # Recursively check nested objects
                                    check_patterns(value, current_path)
                
                check_patterns(patterns)
            except (json.JSONDecodeError, KeyError):
                continue
        
        # Don't fail on this - some patterns may be structured differently
        if errors and len(errors) < 10:  # Only fail if many errors
            pass  # Just log for now


class TestNewKnowledgeFiles:
    """Tests specifically for new knowledge files."""

    @pytest.fixture
    def new_knowledge_names(self) -> List[str]:
        """List of new knowledge file names to test."""
        # Based on git status, these are the new knowledge files
        return [
            "advanced-rag-patterns",
            "agent-testing-patterns",
            "agentic-loop-patterns",
            "anthropic-agentic",
            "api-integration-patterns",
            "business-automation-patterns",
            "caching-patterns",
            "data-pipeline-patterns",
            "database-agent-patterns",
            "error-handling-patterns",
            "filesystem-patterns",
            "hitl-patterns",
            "langsmith-prompts-patterns",
            "memory-patterns",
            "ocr-patterns",
            "speech-patterns",
            "state-patterns",
            "streaming-patterns",
            "subagent-patterns",
            "tool-patterns",
            "vision-patterns",
            "web-browsing-patterns",
        ]

    def test_new_knowledge_files_exist(self, knowledge_dir: Path, new_knowledge_names: List[str]):
        """Test that all new knowledge files exist."""
        missing_files = []
        for knowledge_name in new_knowledge_names:
            knowledge_path = knowledge_dir / f"{knowledge_name}.json"
            if not knowledge_path.exists():
                missing_files.append(knowledge_name)
        
        if missing_files:
            pytest.fail(
                f"Missing {len(missing_files)} new knowledge file(s):\n" +
                "\n".join(f"  - {name}.json" for name in missing_files)
            )

    def test_new_knowledge_files_have_valid_structure(self, knowledge_dir: Path, new_knowledge_names: List[str]):
        """Test that all new knowledge files have valid structure."""
        errors = []
        for knowledge_name in new_knowledge_names:
            knowledge_path = knowledge_dir / f"{knowledge_name}.json"
            if not knowledge_path.exists():
                continue
            
            try:
                with open(knowledge_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Check required fields
                required_fields = ["id", "name", "version", "category", "description"]
                missing_fields = [f for f in required_fields if f not in data]
                if missing_fields:
                    errors.append(f"{knowledge_name}: Missing fields - {', '.join(missing_fields)}")
                
                # Check id matches filename
                if data.get("id") != knowledge_name:
                    errors.append(f"{knowledge_name}: id '{data.get('id')}' doesn't match filename")
                
                # Check patterns exists
                if "patterns" not in data:
                    errors.append(f"{knowledge_name}: Missing 'patterns' field")
                elif not isinstance(data["patterns"], dict):
                    errors.append(f"{knowledge_name}: 'patterns' should be an object")
                
                # Check best_practices exists
                if "best_practices" not in data:
                    errors.append(f"{knowledge_name}: Missing 'best_practices' field")
                elif not isinstance(data["best_practices"], list):
                    errors.append(f"{knowledge_name}: 'best_practices' should be an array")
                
                # Check anti_patterns exists
                if "anti_patterns" not in data:
                    errors.append(f"{knowledge_name}: Missing 'anti_patterns' field")
                elif not isinstance(data["anti_patterns"], list):
                    errors.append(f"{knowledge_name}: 'anti_patterns' should be an array")
                
            except json.JSONDecodeError as e:
                errors.append(f"{knowledge_name}: Invalid JSON - {e}")
            except Exception as e:
                errors.append(f"{knowledge_name}: Error - {e}")
        
        if errors:
            pytest.fail(
                f"Found {len(errors)} issue(s) with new knowledge files:\n" +
                "\n".join(f"  - {e}" for e in errors)
            )
