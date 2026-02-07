"""
Unit tests for ProjectConfig dataclass.

Tests cover:
- Direct instantiation with various parameter combinations
- from_dict() factory method with valid/partial/empty data
- from_yaml_file() with valid and invalid YAML files
- from_json_file() with valid and invalid JSON files
- Default value handling
"""

import json
import sys
from pathlib import Path

import pytest
import yaml

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.core.generate_project import ProjectConfig


class TestProjectConfigInstantiation:
    """Tests for direct ProjectConfig instantiation."""
    
    def test_minimal_instantiation(self):
        """Test creating ProjectConfig with only required field."""
        config = ProjectConfig(project_name="minimal-project")
        
        assert config.project_name == "minimal-project"
        assert config.project_description == ""
        assert config.domain == "general"
        assert config.primary_language == "python"
        assert config.frameworks == []
        assert config.triggers == []
        assert config.agents == []
        assert config.skills == []
        assert config.mcp_servers == []
        assert config.style_guide == "default"
        assert config.blueprint_id is None
        assert config.team_context == ""
    
    def test_full_instantiation(self):
        """Test creating ProjectConfig with all fields."""
        mcp_servers = [{"name": "test", "url": "https://test.com"}]
        
        config = ProjectConfig(
            project_name="full-project",
            project_description="Full description",
            domain="web-development",
            primary_language="typescript",
            frameworks=["react", "nodejs"],
            triggers=["jira", "github"],
            agents=["code-reviewer"],
            skills=["tdd"],
            mcp_servers=mcp_servers,
            style_guide="google",
            blueprint_id="typescript-react",
            team_context="Small team"
        )
        
        assert config.project_name == "full-project"
        assert config.project_description == "Full description"
        assert config.domain == "web-development"
        assert config.primary_language == "typescript"
        assert config.frameworks == ["react", "nodejs"]
        assert config.triggers == ["jira", "github"]
        assert config.agents == ["code-reviewer"]
        assert config.skills == ["tdd"]
        assert config.mcp_servers == mcp_servers
        assert config.style_guide == "google"
        assert config.blueprint_id == "typescript-react"
        assert config.team_context == "Small team"
    
    def test_mutable_default_isolation(self):
        """Test that mutable defaults are isolated between instances."""
        config1 = ProjectConfig(project_name="project1")
        config2 = ProjectConfig(project_name="project2")
        
        config1.frameworks.append("fastapi")
        
        assert "fastapi" in config1.frameworks
        assert "fastapi" not in config2.frameworks


class TestProjectConfigFromDict:
    """Tests for ProjectConfig.from_dict() factory method."""
    
    def test_from_dict_valid_full(self, sample_config_dict):
        """Test from_dict with complete valid dictionary."""
        config = ProjectConfig.from_dict(sample_config_dict)
        
        assert config.project_name == "dict-test-project"
        assert config.project_description == "Project from dictionary"
        assert config.domain == "web-development"
        assert config.primary_language == "python"
        assert config.frameworks == ["fastapi", "sqlalchemy"]
        assert config.triggers == ["jira", "confluence"]
        assert config.agents == ["code-reviewer", "test-generator"]
        assert config.skills == ["bugfix-workflow", "tdd"]
        assert len(config.mcp_servers) == 1
        assert config.mcp_servers[0]["name"] == "atlassian"
        assert config.style_guide == "google"
    
    def test_from_dict_minimal(self):
        """Test from_dict with minimal dictionary."""
        data = {"project_name": "minimal"}
        config = ProjectConfig.from_dict(data)
        
        assert config.project_name == "minimal"
        assert config.project_description == ""
        assert config.domain == "general"
    
    def test_from_dict_empty(self):
        """Test from_dict with empty dictionary uses defaults."""
        config = ProjectConfig.from_dict({})
        
        assert config.project_name == "new-project"
        assert config.domain == "general"
        assert config.primary_language == "python"
    
    def test_from_dict_partial(self):
        """Test from_dict with partial dictionary."""
        data = {
            "project_name": "partial-project",
            "domain": "data-science",
            "frameworks": ["pandas", "numpy"]
        }
        config = ProjectConfig.from_dict(data)
        
        assert config.project_name == "partial-project"
        assert config.domain == "data-science"
        assert config.frameworks == ["pandas", "numpy"]
        assert config.primary_language == "python"  # Default
        assert config.triggers == []  # Default
    
    def test_from_dict_extra_fields_ignored(self):
        """Test that extra fields in dictionary are ignored."""
        data = {
            "project_name": "extra-fields",
            "unknown_field": "should be ignored",
            "another_unknown": 123
        }
        config = ProjectConfig.from_dict(data)
        
        assert config.project_name == "extra-fields"
        assert not hasattr(config, "unknown_field")


class TestProjectConfigFromYaml:
    """Tests for ProjectConfig.from_yaml_file() factory method."""
    
    def test_from_yaml_file_valid(self, sample_yaml_config):
        """Test from_yaml_file with valid YAML."""
        config = ProjectConfig.from_yaml_file(str(sample_yaml_config))
        
        assert config.project_name == "dict-test-project"
        assert config.primary_language == "python"
        assert "fastapi" in config.frameworks
    
    def test_from_yaml_file_minimal(self, tmp_path):
        """Test from_yaml_file with minimal YAML content."""
        yaml_path = tmp_path / "minimal.yaml"
        yaml_path.write_text("project_name: yaml-minimal\n")
        
        config = ProjectConfig.from_yaml_file(str(yaml_path))
        
        assert config.project_name == "yaml-minimal"
        assert config.domain == "general"
    
    def test_from_yaml_file_not_found(self, tmp_path):
        """Test from_yaml_file with non-existent file."""
        nonexistent = tmp_path / "nonexistent.yaml"
        
        with pytest.raises(FileNotFoundError):
            ProjectConfig.from_yaml_file(str(nonexistent))
    
    def test_from_yaml_file_invalid_yaml(self, tmp_path):
        """Test from_yaml_file with invalid YAML syntax."""
        invalid_yaml = tmp_path / "invalid.yaml"
        invalid_yaml.write_text("project_name: test\n  invalid: indentation")
        
        with pytest.raises(yaml.YAMLError):
            ProjectConfig.from_yaml_file(str(invalid_yaml))


class TestProjectConfigFromJson:
    """Tests for ProjectConfig.from_json_file() factory method."""
    
    def test_from_json_file_valid(self, sample_json_config):
        """Test from_json_file with valid JSON."""
        config = ProjectConfig.from_json_file(str(sample_json_config))
        
        assert config.project_name == "dict-test-project"
        assert config.primary_language == "python"
        assert "fastapi" in config.frameworks
    
    def test_from_json_file_minimal(self, tmp_path):
        """Test from_json_file with minimal JSON content."""
        json_path = tmp_path / "minimal.json"
        json_path.write_text('{"project_name": "json-minimal"}')
        
        config = ProjectConfig.from_json_file(str(json_path))
        
        assert config.project_name == "json-minimal"
        assert config.domain == "general"
    
    def test_from_json_file_not_found(self, tmp_path):
        """Test from_json_file with non-existent file."""
        nonexistent = tmp_path / "nonexistent.json"
        
        with pytest.raises(FileNotFoundError):
            ProjectConfig.from_json_file(str(nonexistent))
    
    def test_from_json_file_invalid_json(self, tmp_path):
        """Test from_json_file with invalid JSON syntax."""
        invalid_json = tmp_path / "invalid.json"
        invalid_json.write_text("{project_name: missing-quotes}")
        
        with pytest.raises(json.JSONDecodeError):
            ProjectConfig.from_json_file(str(invalid_json))
    
    def test_from_json_file_empty(self, tmp_path):
        """Test from_json_file with empty JSON object."""
        empty_json = tmp_path / "empty.json"
        empty_json.write_text("{}")
        
        config = ProjectConfig.from_json_file(str(empty_json))
        
        assert config.project_name == "new-project"


class TestProjectConfigDefaults:
    """Tests for default value handling."""
    
    def test_default_values_consistency(self):
        """Test that default values are consistent across creation methods."""
        config_direct = ProjectConfig(project_name="test")
        config_dict = ProjectConfig.from_dict({"project_name": "test"})
        
        assert config_direct.domain == config_dict.domain
        assert config_direct.primary_language == config_dict.primary_language
        assert config_direct.style_guide == config_dict.style_guide
    
    def test_none_vs_empty_handling(self):
        """Test handling of None vs empty values."""
        data = {
            "project_name": "test",
            "blueprint_id": None,
            "frameworks": []
        }
        config = ProjectConfig.from_dict(data)
        
        assert config.blueprint_id is None
        assert config.frameworks == []
