"""
Unit Tests for ConfigManager

Tests the configuration management system including:
- Settings loading and saving
- Environment variable resolution
- Tool path resolution
- Knowledge evolution configuration

Author: Antigravity Agent FactoryVersion: 1.0.0
"""

import json
import os
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import tempfile
import shutil

# Import the module under test
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts" / "core"))

from config_manager import ConfigManager, KnowledgeEvolutionConfig


@pytest.fixture
def temp_factory_root():
    """Create a temporary factory root directory."""
    temp_dir = tempfile.mkdtemp()
    
    # Create required directory structure
    cursor_config = Path(temp_dir) / ".agent" / "config"
    cursor_config.mkdir(parents=True)
    
    # Create a minimal .agentrules to identify as factory root
    (Path(temp_dir) / ".agentrules").touch()    
    yield Path(temp_dir)
    
    # Cleanup
    shutil.rmtree(temp_dir)


@pytest.fixture
def config_manager(temp_factory_root):
    """Create a ConfigManager instance with temp directory."""
    # Reset singleton
    ConfigManager.reset_instance()
    
    manager = ConfigManager(factory_root=temp_factory_root)
    
    yield manager
    
    # Reset singleton after test
    ConfigManager.reset_instance()


class TestConfigManagerInitialization:
    """Tests for ConfigManager initialization."""
    
    def test_creates_default_settings(self, config_manager, temp_factory_root):
        """Test that default settings are created when none exist."""
        settings_path = temp_factory_root / ".agent" / "config" / "settings.json"        
        assert settings_path.exists()
        
        with open(settings_path) as f:
            settings = json.load(f)
        
        assert "system" in settings
        assert "tools" in settings
        assert "knowledge_evolution" in settings
    
    def test_singleton_pattern(self, temp_factory_root):
        """Test that ConfigManager follows singleton pattern."""
        ConfigManager.reset_instance()
        
        manager1 = ConfigManager.get_instance(temp_factory_root)
        manager2 = ConfigManager.get_instance()
        
        assert manager1 is manager2
        
        ConfigManager.reset_instance()
    
    def test_factory_root_detection(self, config_manager, temp_factory_root):
        """Test that factory root is correctly detected."""
        assert config_manager.factory_root == temp_factory_root
    
    def test_platform_detection(self, config_manager):
        """Test that platform is detected."""
        assert config_manager.current_platform in ["windows", "linux", "darwin"]


class TestConfigManagerGetSet:
    """Tests for get/set operations."""
    
    def test_get_simple_value(self, config_manager):
        """Test getting a simple configuration value."""
        version = config_manager.get("system.factory_version")
        
        assert version is not None
        assert isinstance(version, str)
    
    def test_get_nested_value(self, config_manager):
        """Test getting a nested configuration value."""
        mode = config_manager.get("knowledge_evolution.mode")
        
        assert mode == "awareness_hybrid"
    
    def test_get_with_default(self, config_manager):
        """Test getting a non-existent value with default."""
        value = config_manager.get("nonexistent.path", default="default_value")
        
        assert value == "default_value"
    
    def test_set_value(self, config_manager):
        """Test setting a configuration value."""
        config_manager.set("knowledge_evolution.mode", "stability_first")
        
        mode = config_manager.get("knowledge_evolution.mode")
        assert mode == "stability_first"
    
    def test_set_creates_path(self, config_manager):
        """Test that set creates missing path components."""
        config_manager.set("new.nested.path", "test_value")
        
        value = config_manager.get("new.nested.path")
        assert value == "test_value"


class TestEnvironmentVariableResolution:
    """Tests for environment variable resolution."""
    
    def test_resolves_env_var(self, config_manager):
        """Test that ${VAR} syntax is resolved."""
        with patch.dict(os.environ, {"TEST_VAR": "test_value"}):
            config_manager.set("test.value", "${TEST_VAR}")
            
            resolved = config_manager.get("test.value")
            assert resolved == "test_value"
    
    def test_missing_env_var_returns_empty(self, config_manager):
        """Test that missing env vars resolve to empty string."""
        config_manager.set("test.value", "${NONEXISTENT_VAR_12345}")
        
        resolved = config_manager.get("test.value")
        assert resolved == ""
    
    def test_partial_env_var_resolution(self, config_manager):
        """Test resolving env var in a larger string."""
        with patch.dict(os.environ, {"USER_NAME": "testuser"}):
            config_manager.set("test.path", "/home/${USER_NAME}/data")
            
            resolved = config_manager.get("test.path")
            assert resolved == "/home/testuser/data"


class TestToolPathResolution:
    """Tests for tool path resolution."""
    
    def test_get_tool_path_from_env(self, config_manager):
        """Test tool path resolution from environment variable."""
        with patch.dict(os.environ, {"PYTHON_PATH": "/custom/python"}):
            with patch.object(config_manager, "_path_exists", return_value=True):
                path = config_manager.get_tool_path("python")
                assert path == "/custom/python"
    
    def test_get_tool_path_from_config(self, config_manager):
        """Test tool path resolution from explicit config."""
        config_manager.set("tools.python.path", "/explicit/python")
        
        with patch.object(config_manager, "_path_exists", return_value=True):
            path = config_manager.get_tool_path("python")
            assert path == "/explicit/python"
    
    def test_get_tool_path_returns_none_for_unknown(self, config_manager):
        """Test that unknown tool returns None."""
        path = config_manager.get_tool_path("unknown_tool_xyz")
        assert path is None


class TestKnowledgeEvolutionConfig:
    """Tests for knowledge evolution configuration."""
    
    def test_get_knowledge_evolution_config(self, config_manager):
        """Test getting knowledge evolution configuration."""
        ke_config = config_manager.get_knowledge_evolution_config()
        
        assert isinstance(ke_config, KnowledgeEvolutionConfig)
        assert ke_config.mode == "awareness_hybrid"
        assert ke_config.check_on_startup is True
    
    def test_knowledge_evolution_sources(self, config_manager):
        """Test knowledge evolution sources configuration."""
        ke_config = config_manager.get_knowledge_evolution_config()
        
        assert "github_trending" in ke_config.sources
        assert ke_config.sources["github_trending"] is True


class TestCredentialManagement:
    """Tests for credential management."""
    
    def test_get_credential_resolves_env(self, config_manager):
        """Test getting a credential resolves environment variable."""
        with patch.dict(os.environ, {"GITHUB_TOKEN": "ghp_test_token"}):
            token = config_manager.get_credential("github_token")
            assert token == "ghp_test_token"
    
    def test_get_missing_credential_returns_none(self, config_manager):
        """Test getting a missing credential returns None."""
        token = config_manager.get_credential("nonexistent_credential")
        assert token is None


class TestSettingsValidation:
    """Tests for settings validation."""
    
    def test_validate_valid_settings(self, config_manager):
        """Test validating correct settings returns no errors."""
        errors = config_manager.validate_settings()
        assert len(errors) == 0
    
    def test_validate_invalid_mode(self, config_manager):
        """Test that invalid mode is caught."""
        config_manager.set("knowledge_evolution.mode", "invalid_mode")
        
        errors = config_manager.validate_settings()
        assert any("mode" in e for e in errors)
    
    def test_validate_invalid_channel(self, config_manager):
        """Test that invalid update channel is caught."""
        config_manager.set("knowledge_evolution.update_channel", "invalid_channel")
        
        errors = config_manager.validate_settings()
        assert any("channel" in e for e in errors)


class TestLegacyMigration:
    """Tests for migrating from legacy tools.json."""
    
    def test_migrates_legacy_tools(self, temp_factory_root):
        """Test migration from legacy tools.json format."""
        ConfigManager.reset_instance()
        
        # Create legacy tools.json
        legacy_path = temp_factory_root / ".agent" / "config" / "tools.json"        legacy_path.parent.mkdir(parents=True, exist_ok=True)
        
        legacy_content = {
            "version": "1.0.0",
            "tools": {
                "python": {
                    "path": "/legacy/python",
                    "description": "Legacy Python"
                }
            }
        }
        
        with open(legacy_path, "w") as f:
            json.dump(legacy_content, f)
        
        # Create manager - should migrate
        manager = ConfigManager(factory_root=temp_factory_root)
        
        # Check migration
        assert manager.get("tools.python") is not None
        
        # Check backup was created
        backup_path = legacy_path.with_suffix(".json.bak")
        assert backup_path.exists()
        
        ConfigManager.reset_instance()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
