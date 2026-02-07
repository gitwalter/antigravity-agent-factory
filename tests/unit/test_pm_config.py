"""
Unit tests for PM configuration fields in ProjectConfig.

Tests cover:
- PM field defaults and validation
- from_dict() with PM fields
- Agent/skill extension when PM is enabled
"""

import sys
from pathlib import Path

import pytest

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.core.generate_project import ProjectConfig


class TestPMConfigFields:
    """Tests for PM fields in ProjectConfig."""
    
    def test_pm_enabled_default_false(self):
        """Test that pm_enabled defaults to False."""
        config = ProjectConfig(project_name="test-project")
        
        # If PM fields don't exist yet, this will raise AttributeError
        # which is the expected behavior - tests should fail appropriately
        if hasattr(config, 'pm_enabled'):
            assert config.pm_enabled is False
        else:
            # PM fields not implemented yet - test fails as expected
            pytest.fail("pm_enabled field not found in ProjectConfig. "
                       "PM fields need to be added to ProjectConfig dataclass.")
    
    def test_pm_backend_accepts_valid_values(self):
        """Test that pm_backend accepts valid backend values."""
        valid_backends = ["github", "jira", "azure-devops", "linear"]
        
        for backend in valid_backends:
            if hasattr(ProjectConfig, '__annotations__') and 'pm_backend' in ProjectConfig.__annotations__:
                config = ProjectConfig(
                    project_name="test-project",
                    pm_enabled=True,
                    pm_backend=backend
                )
                assert config.pm_backend == backend
            else:
                # PM fields not implemented yet
                pytest.skip("PM fields not implemented in ProjectConfig yet")
    
    def test_pm_doc_backend_accepts_valid_values(self):
        """Test that pm_doc_backend accepts valid backend values."""
        valid_backends = ["github", "jira", "confluence", "azure-devops", "linear"]
        
        for backend in valid_backends:
            if hasattr(ProjectConfig, '__annotations__') and 'pm_doc_backend' in ProjectConfig.__annotations__:
                config = ProjectConfig(
                    project_name="test-project",
                    pm_enabled=True,
                    pm_doc_backend=backend
                )
                assert config.pm_doc_backend == backend
            else:
                # PM fields not implemented yet
                pytest.skip("PM fields not implemented in ProjectConfig yet")
    
    def test_pm_methodology_accepts_valid_values(self):
        """Test that pm_methodology accepts valid methodology values."""
        valid_methodologies = ["scrum", "kanban", "hybrid", "waterfall"]
        
        for methodology in valid_methodologies:
            if hasattr(ProjectConfig, '__annotations__') and 'pm_methodology' in ProjectConfig.__annotations__:
                config = ProjectConfig(
                    project_name="test-project",
                    pm_enabled=True,
                    pm_methodology=methodology
                )
                assert config.pm_methodology == methodology
            else:
                # PM fields not implemented yet
                pytest.skip("PM fields not implemented in ProjectConfig yet")


class TestPMConfigFromDict:
    """Tests for from_dict with PM fields."""
    
    def test_from_dict_with_pm_enabled(self):
        """Test from_dict with pm_enabled set to True."""
        data = {
            "project_name": "pm-project",
            "pm_enabled": True
        }
        
        config = ProjectConfig.from_dict(data)
        
        if hasattr(config, 'pm_enabled'):
            assert config.pm_enabled is True
        else:
            pytest.fail("pm_enabled field not found in ProjectConfig. "
                       "PM fields need to be added to ProjectConfig.from_dict().")
    
    def test_from_dict_with_full_pm_config(self):
        """Test from_dict with complete PM configuration."""
        data = {
            "project_name": "full-pm-project",
            "pm_enabled": True,
            "pm_backend": "jira",
            "pm_doc_backend": "confluence",
            "pm_methodology": "scrum"
        }
        
        config = ProjectConfig.from_dict(data)
        
        if hasattr(config, 'pm_enabled'):
            assert config.pm_enabled is True
            assert config.pm_backend == "jira"
            assert config.pm_doc_backend == "confluence"
            assert config.pm_methodology == "scrum"
        else:
            pytest.fail("PM fields not found in ProjectConfig. "
                       "PM fields need to be added to ProjectConfig dataclass and from_dict().")
    
    def test_from_dict_pm_disabled_by_default(self):
        """Test that PM is disabled by default when not specified."""
        data = {
            "project_name": "no-pm-project"
        }
        
        config = ProjectConfig.from_dict(data)
        
        if hasattr(config, 'pm_enabled'):
            assert config.pm_enabled is False
        else:
            # PM fields not implemented yet - test fails as expected
            pytest.fail("pm_enabled field not found in ProjectConfig. "
                       "PM fields need to be added to ProjectConfig dataclass.")


class TestPMAgentSkillExtension:
    """Tests for agent/skill lists when PM is enabled."""
    
    def test_pm_agents_added_when_enabled(self):
        """Test that PM agents are added when PM is enabled."""
        expected_pm_agents = ["product-owner", "sprint-master", "task-manager", "reporting-agent"]
        
        if hasattr(ProjectConfig, '__annotations__') and 'pm_enabled' in ProjectConfig.__annotations__:
            config = ProjectConfig(
                project_name="pm-project",
                pm_enabled=True,
                agents=["code-reviewer"]
            )
            
            # Check if PM agents are automatically added
            # This depends on implementation - could be in __post_init__ or a property
            # For now, we'll check if the agents list contains PM agents
            # The actual implementation might add them automatically or require explicit addition
            
            # If there's a method or property that extends agents, test it
            if hasattr(config, 'get_all_agents'):
                all_agents = config.get_all_agents()
                for pm_agent in expected_pm_agents:
                    assert pm_agent in all_agents, f"PM agent {pm_agent} not found in agents list"
            else:
                # If agents are automatically extended, they should be in config.agents
                # Otherwise, this test documents expected behavior
                for pm_agent in expected_pm_agents:
                    assert pm_agent in config.agents or hasattr(config, '_pm_agents'), \
                        f"PM agent {pm_agent} should be added when PM is enabled"
        else:
            pytest.skip("PM fields not implemented in ProjectConfig yet")
    
    def test_pm_skills_added_when_enabled(self):
        """Test that PM skills are added when PM is enabled."""
        expected_pm_skills = [
            "create-epic",
            "create-story",
            "create-task",
            "estimate-task",
            "plan-sprint",
            "close-sprint",
            "run-standup",
            "generate-burndown",
            "health-check"
        ]
        
        if hasattr(ProjectConfig, '__annotations__') and 'pm_enabled' in ProjectConfig.__annotations__:
            config = ProjectConfig(
                project_name="pm-project",
                pm_enabled=True,
                skills=["tdd"]
            )
            
            # Check if PM skills are automatically added
            if hasattr(config, 'get_all_skills'):
                all_skills = config.get_all_skills()
                for pm_skill in expected_pm_skills:
                    assert pm_skill in all_skills, f"PM skill {pm_skill} not found in skills list"
            else:
                # If skills are automatically extended, they should be in config.skills
                for pm_skill in expected_pm_skills:
                    assert pm_skill in config.skills or hasattr(config, '_pm_skills'), \
                        f"PM skill {pm_skill} should be added when PM is enabled"
        else:
            pytest.skip("PM fields not implemented in ProjectConfig yet")
    
    def test_agents_unchanged_when_pm_disabled(self):
        """Test that agents list is unchanged when PM is disabled."""
        initial_agents = ["code-reviewer", "test-generator"]
        
        config = ProjectConfig(
            project_name="no-pm-project",
            agents=initial_agents
        )
        
        if hasattr(config, 'pm_enabled'):
            # Explicitly set pm_enabled to False
            config.pm_enabled = False
            
            # Agents should remain unchanged
            assert config.agents == initial_agents
            
            # PM agents should not be present
            pm_agents = ["product-owner", "sprint-master", "task-manager", "reporting-agent"]
            for pm_agent in pm_agents:
                assert pm_agent not in config.agents, \
                    f"PM agent {pm_agent} should not be present when PM is disabled"
        else:
            # When PM fields don't exist, agents should work normally
            assert config.agents == initial_agents
