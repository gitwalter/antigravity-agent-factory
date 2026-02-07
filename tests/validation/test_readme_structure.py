"""
README project structure validation tests.

Tests validate that the project structure documented in README.md
accurately reflects the actual filesystem structure.

This ensures documentation stays synchronized with the codebase
as the project evolves, catching drift before it reaches production.
"""

import sys
from pathlib import Path

import pytest

# Add project root and scripts to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from scripts.validation.validate_readme_structure import StructureValidator


class TestReadmeExists:
    """Tests for README.md file existence and basic structure."""
    
    @pytest.fixture
    def validator(self, project_root):
        """Create a StructureValidator instance."""
        return StructureValidator(project_root)
    
    def test_readme_exists(self, project_root):
        """Test that README.md exists in project root."""
        readme_path = project_root / "README.md"
        assert readme_path.exists(), "README.md should exist in project root"
    
    def test_readme_has_content(self, project_root):
        """Test that README.md has content."""
        readme_path = project_root / "README.md"
        content = readme_path.read_text(encoding="utf-8")
        assert len(content) > 100, "README.md should have substantial content"
    
    def test_readme_has_project_structure_section(self, project_root):
        """Test that README.md has a Project Structure section."""
        readme_path = project_root / "README.md"
        content = readme_path.read_text(encoding="utf-8")
        assert "## Project Structure" in content, \
            "README.md should have a '## Project Structure' section"


class TestReadmeStructureCounts:
    """Tests for README project structure count accuracy."""
    
    @pytest.fixture
    def validator(self, project_root):
        """Create a StructureValidator instance."""
        return StructureValidator(project_root)
    
    @pytest.fixture
    def actual_counts(self, validator):
        """Get actual filesystem counts."""
        return validator.generate_counts_summary()
    
    @pytest.fixture
    def documented_counts(self, validator):
        """Get counts documented in README."""
        return validator.extract_readme_counts()
    
    def test_readme_structure_counts_match_filesystem(self, validator):
        """Test that all README counts match actual filesystem."""
        is_valid, discrepancies = validator.validate()
        
        if not is_valid:
            # Provide helpful error message
            actual = validator.generate_counts_summary()
            documented = validator.extract_readme_counts()
            
            msg_lines = ["README project structure counts do not match filesystem:"]
            msg_lines.append("")
            for discrepancy in discrepancies:
                msg_lines.append(f"  - {discrepancy}")
            msg_lines.append("")
            msg_lines.append("To fix, run: python scripts/validation/validate_readme_structure.py --update")
            
            pytest.fail("\n".join(msg_lines))
    
    def _check_count(self, actual: int, doc_info: dict, name: str):
        """
        Helper to check count with support for threshold (X+) vs exact counts.
        
        For threshold counts (is_threshold=True): actual >= documented
        For exact counts (is_threshold=False): actual == documented
        """
        doc_count = doc_info['count']
        is_threshold = doc_info['is_threshold']
        
        if is_threshold:
            assert actual >= doc_count, \
                f"{name} count below minimum: README says {doc_count}+, filesystem has {actual}"
        else:
            assert actual == doc_count, \
                f"{name} count mismatch: README says {doc_count}, filesystem has {actual}"
    
    def test_readme_agents_count(self, actual_counts, documented_counts):
        """Test that agents count in README matches filesystem."""
        actual = actual_counts.get("agents", 0)
        documented = documented_counts.get("agents")
        
        assert documented is not None, \
            "README should document agent count in Project Structure"
        self._check_count(actual, documented, "Agents")
    
    def test_readme_skills_count(self, actual_counts, documented_counts):
        """Test that skills count in README matches filesystem."""
        actual = actual_counts.get("skills", 0)
        documented = documented_counts.get("skills")
        
        assert documented is not None, \
            "README should document skills count in Project Structure"
        self._check_count(actual, documented, "Skills")
    
    def test_readme_blueprints_count(self, actual_counts, documented_counts):
        """Test that blueprints count in README matches filesystem."""
        actual = actual_counts.get("blueprints", 0)
        documented = documented_counts.get("blueprints")
        
        assert documented is not None, \
            "README should document blueprints count in Project Structure"
        self._check_count(actual, documented, "Blueprints")
    
    def test_readme_patterns_count(self, actual_counts, documented_counts):
        """Test that patterns count in README matches filesystem."""
        actual = actual_counts.get("patterns", 0)
        documented = documented_counts.get("patterns")
        
        assert documented is not None, \
            "README should document patterns count in Project Structure"
        self._check_count(actual, documented, "Patterns")
    
    def test_readme_knowledge_count(self, actual_counts, documented_counts):
        """Test that knowledge files count in README matches filesystem."""
        actual = actual_counts.get("knowledge", 0)
        documented = documented_counts.get("knowledge")
        
        assert documented is not None, \
            "README should document knowledge files count in Project Structure"
        self._check_count(actual, documented, "Knowledge")
    
    def test_readme_templates_count(self, actual_counts, documented_counts):
        """Test that templates count in README matches filesystem."""
        actual = actual_counts.get("templates", 0)
        documented = documented_counts.get("templates")
        
        assert documented is not None, \
            "README should document templates count in Project Structure"
        self._check_count(actual, documented, "Templates")


class TestStructureValidatorFunctionality:
    """Tests for StructureValidator class functionality."""
    
    @pytest.fixture
    def validator(self, project_root):
        """Create a StructureValidator instance."""
        return StructureValidator(project_root)
    
    def test_scan_agents_returns_dict(self, validator):
        """Test that scan_agents returns expected structure."""
        result = validator.scan_agents()
        assert isinstance(result, dict), "scan_agents should return a dict"
        assert "count" in result, "scan_agents result should have 'count'"
        assert "agents" in result, "scan_agents result should have 'agents'"
        assert isinstance(result["agents"], list), "agents should be a list"
    
    def test_scan_skills_returns_dict(self, validator):
        """Test that scan_skills returns expected structure."""
        result = validator.scan_skills()
        assert isinstance(result, dict), "scan_skills should return a dict"
        assert "count" in result, "scan_skills result should have 'count'"
        assert "skills" in result, "scan_skills result should have 'skills'"
        assert isinstance(result["skills"], list), "skills should be a list"
    
    def test_scan_blueprints_returns_dict(self, validator):
        """Test that scan_blueprints returns expected structure."""
        result = validator.scan_blueprints()
        assert isinstance(result, dict), "scan_blueprints should return a dict"
        assert "count" in result, "scan_blueprints result should have 'count'"
        assert "blueprints" in result, "scan_blueprints result should have 'blueprints'"
    
    def test_scan_patterns_returns_dict(self, validator):
        """Test that scan_patterns returns expected structure."""
        result = validator.scan_patterns()
        assert isinstance(result, dict), "scan_patterns should return a dict"
        assert "total_files" in result, "scan_patterns result should have 'total_files'"
        assert "categories" in result, "scan_patterns result should have 'categories'"
    
    def test_scan_knowledge_returns_dict(self, validator):
        """Test that scan_knowledge returns expected structure."""
        result = validator.scan_knowledge()
        assert isinstance(result, dict), "scan_knowledge should return a dict"
        assert "count" in result, "scan_knowledge result should have 'count'"
        assert "files" in result, "scan_knowledge result should have 'files'"
    
    def test_scan_templates_returns_dict(self, validator):
        """Test that scan_templates returns expected structure."""
        result = validator.scan_templates()
        assert isinstance(result, dict), "scan_templates should return a dict"
        assert "total_files" in result, "scan_templates result should have 'total_files'"
        assert "categories" in result, "scan_templates result should have 'categories'"
    
    def test_scan_all_returns_complete_structure(self, validator):
        """Test that scan_all returns all component categories."""
        result = validator.scan_all()
        expected_keys = {"agents", "skills", "blueprints", "patterns", "knowledge", "templates"}
        assert set(result.keys()) == expected_keys, \
            f"scan_all should return all categories: {expected_keys}"
    
    def test_generate_counts_summary(self, validator):
        """Test that generate_counts_summary returns integer counts."""
        counts = validator.generate_counts_summary()
        for key, value in counts.items():
            assert isinstance(value, int), f"{key} count should be an integer"
            assert value >= 0, f"{key} count should be non-negative"
    
    def test_extract_readme_counts(self, validator):
        """Test that extract_readme_counts parses README correctly."""
        counts = validator.extract_readme_counts()
        assert isinstance(counts, dict), "extract_readme_counts should return a dict"
        # Should have at least some counts extracted
        assert len(counts) > 0, "Should extract at least some counts from README"
        # Each entry should have 'count' and 'is_threshold' keys
        for key, value in counts.items():
            assert isinstance(value, dict), f"{key} should be a dict with count info"
            assert 'count' in value, f"{key} should have 'count' key"
            assert 'is_threshold' in value, f"{key} should have 'is_threshold' key"
    
    def test_validate_returns_tuple(self, validator):
        """Test that validate returns expected tuple structure."""
        result = validator.validate()
        assert isinstance(result, tuple), "validate should return a tuple"
        assert len(result) == 2, "validate should return (is_valid, discrepancies)"
        is_valid, discrepancies = result
        assert isinstance(is_valid, bool), "First element should be boolean"
        assert isinstance(discrepancies, list), "Second element should be list"


class TestProjectComponentsExist:
    """Tests to verify expected project components exist."""
    
    @pytest.fixture
    def validator(self, project_root):
        """Create a StructureValidator instance."""
        return StructureValidator(project_root)
    
    def test_agents_directory_exists(self, project_root):
        """Test that .agent/agents directory exists."""
        agents_dir = project_root / ".agent" / "agents"
        assert agents_dir.exists(), ".agent/agents directory should exist"
    
    def test_skills_directory_exists(self, project_root):
        """Test that .agent/skills directory exists."""
        skills_dir = project_root / ".agent" / "skills"
        assert skills_dir.exists(), ".agent/skills directory should exist"
    
    def test_blueprints_directory_exists(self, project_root):
        """Test that blueprints directory exists."""
        blueprints_dir = project_root / "blueprints"
        assert blueprints_dir.exists(), "blueprints directory should exist"
    
    def test_patterns_directory_exists(self, project_root):
        """Test that patterns directory exists."""
        patterns_dir = project_root / "patterns"
        assert patterns_dir.exists(), "patterns directory should exist"
    
    def test_knowledge_directory_exists(self, project_root):
        """Test that knowledge directory exists."""
        knowledge_dir = project_root / "knowledge"
        assert knowledge_dir.exists(), "knowledge directory should exist"
    
    def test_templates_directory_exists(self, project_root):
        """Test that templates directory exists."""
        templates_dir = project_root / "templates"
        assert templates_dir.exists(), "templates directory should exist"
    
    def test_has_minimum_agents(self, validator):
        """Test that project has at least some agents defined."""
        result = validator.scan_agents()
        assert result["count"] >= 5, \
            f"Project should have at least 5 agents, found {result['count']}"
    
    def test_has_minimum_skills(self, validator):
        """Test that project has at least some skills defined."""
        result = validator.scan_skills()
        assert result["count"] >= 10, \
            f"Project should have at least 10 skills, found {result['count']}"
    
    def test_has_minimum_blueprints(self, validator):
        """Test that project has at least some blueprints defined."""
        result = validator.scan_blueprints()
        assert result["count"] >= 10, \
            f"Project should have at least 10 blueprints, found {result['count']}"
