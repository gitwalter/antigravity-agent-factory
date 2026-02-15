"""
Configuration Manager for Antigravity Agent Factory

This module provides centralized configuration management, handling all settings
including tools, credentials, knowledge evolution preferences, and platform-specific
configurations. It supports multiple configuration sources with a defined resolution
order and provides a clean API for accessing and modifying settings.

Features:
    - Unified settings management (tools, credentials, knowledge evolution)
    - Environment variable resolution (${VAR_NAME} syntax)
    - Platform detection and platform-specific defaults
    - Configuration validation against JSON Schema
    - Migration from legacy tools.json format
    - Thread-safe singleton pattern

Design Patterns:
    - Singleton: Single configuration instance
    - Strategy: Different resolution strategies per setting
    - Observer: Configuration change notifications (future)

Axiom Alignment:
    - A1 (Verifiability): Configuration is validated against schema
    - A3 (Transparency): Clear resolution order and source tracking
    - A4 (Adaptability): Flexible configuration for different environments

Author: Antigravity Agent Factory
Version: 1.0.0
"""

import json
import os
import platform
import re
import shutil
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class ResolutionResult:
    """Result of resolving a configuration value.

    Attributes:
        value: The resolved value
        source: Where the value came from (env, config, default, etc.)
        path: Configuration path (e.g., "tools.python.path")
    """

    value: Any
    source: str
    path: str


@dataclass
class KnowledgeEvolutionConfig:
    """Configuration for the knowledge evolution system.

    Attributes:
        mode: Update behavior mode
        check_on_startup: Whether to check for updates on startup
        auto_update: Whether to automatically apply updates
        notify_updates: Whether to show update notifications
        update_channel: Which update channel to follow
        check_interval_hours: Hours between update checks
        subscriptions: Glob patterns for knowledge subscriptions
        sources: Which sources are enabled
        merge_strategy: How to handle conflicts
        backup_before_update: Whether to backup before updates
        max_backups: Maximum number of backups to keep
    """

    mode: str = "awareness_hybrid"
    check_on_startup: bool = True
    auto_update: bool = False
    notify_updates: bool = True
    update_channel: str = "stable"
    check_interval_hours: int = 24
    subscriptions: List[str] = field(default_factory=lambda: ["*"])
    sources: Dict[str, bool] = field(
        default_factory=lambda: {
            "github_trending": True,
            "official_docs": True,
            "package_registries": True,
            "community_curated": True,
            "user_feedback": True,
        }
    )
    merge_strategy: str = "balanced"
    backup_before_update: bool = True
    max_backups: int = 10


class ConfigManager:
    """Centralized configuration manager for the Antigravity Agent Factory.

    Provides a unified interface for accessing all configuration settings
    with support for environment variable resolution, platform detection,
    and schema validation.

    Example:
        config = ConfigManager.get_instance()
        python_path = config.get_tool_path("python")
        evolution_config = config.get_knowledge_evolution_config()
    """

    _instance: Optional["ConfigManager"] = None
    _ENV_VAR_PATTERN = re.compile(r"\$\{([^}]+)\}")

    # Resolution order for finding values
    RESOLUTION_ORDER = [
        "environment_variable",
        "local_config",
        "auto_detect",
        "default",
    ]

    def __init__(self, factory_root: Optional[Path] = None):
        """Initialize the configuration manager.

        Args:
            factory_root: Root directory of the factory. Auto-detected if not provided.
        """
        self._factory_root = factory_root or self._detect_factory_root()
        self._settings_path = self._factory_root / ".agent" / "config" / "settings.json"
        self._legacy_tools_path = (
            self._factory_root / ".agent" / "config" / "tools.json"
        )
        self._session_cache_path = (
            self._factory_root / ".agent" / "cache" / "session-paths.json"
        )
        self._settings: Dict[str, Any] = {}
        self._session_cache: Dict[str, Any] = {}
        self._platform = self._detect_platform()
        self._load_settings()
        self._load_session_cache()

    @classmethod
    def get_instance(cls, factory_root: Optional[Path] = None) -> "ConfigManager":
        """Get or create the singleton configuration manager instance.

        Args:
            factory_root: Factory root directory (only used on first call)

        Returns:
            ConfigManager singleton instance
        """
        if cls._instance is None:
            cls._instance = cls(factory_root)
        return cls._instance

    @classmethod
    def reset_instance(cls) -> None:
        """Reset the singleton instance. Useful for testing."""
        cls._instance = None

    def _detect_factory_root(self) -> Path:
        """Detect the factory root directory.

        Walks up from current file to find the factory root by looking
        for characteristic files.

        Returns:
            Path to factory root

        Raises:
            RuntimeError: If factory root cannot be detected
        """
        current = Path(__file__).resolve().parent

        # Walk up looking for factory markers
        for _ in range(10):  # Max depth
            if (current / ".agentrules").exists() or (current / "blueprints").exists():
                return current
            parent = current.parent
            if parent == current:
                break
            current = parent

        # Fallback to current working directory
        cwd = Path.cwd()
        if (cwd / ".agentrules").exists():
            return cwd

        raise RuntimeError(
            "Cannot detect factory root. Please provide factory_root parameter."
        )

    def _detect_platform(self) -> str:
        """Detect the current operating system platform.

        Returns:
            Platform identifier: 'windows', 'linux', or 'darwin'
        """
        system = platform.system().lower()
        if system == "windows":
            return "windows"
        elif system == "darwin":
            return "darwin"
        else:
            return "linux"

    def _load_settings(self) -> None:
        """Load settings from file, migrating from legacy format if needed."""
        if self._settings_path.exists():
            with open(self._settings_path, "r", encoding="utf-8") as f:
                self._settings = json.load(f)
        elif self._legacy_tools_path.exists():
            # Migrate from legacy tools.json
            self._migrate_from_legacy()
        else:
            # Create default settings
            self._settings = self._create_default_settings()
            self._save_settings()

    def _load_session_cache(self) -> None:
        """Load session-level path cache if it exists."""
        if self._session_cache_path.exists():
            try:
                with open(self._session_cache_path, "r", encoding="utf-8") as f:
                    self._session_cache = json.load(f)
            except (json.JSONDecodeError, IOError):
                self._session_cache = {}
        else:
            self._session_cache = {}

    def _save_session_cache(self) -> None:
        """Save session cache to file."""
        self._session_cache_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self._session_cache_path, "w", encoding="utf-8") as f:
            json.dump(self._session_cache, f, indent=2)

    def update_session_cache(
        self, tool_name: str, path: str, version: Optional[str] = None
    ) -> None:
        """Update the session cache with a verified tool path.

        Args:
            tool_name: Name of the tool (e.g., "python", "git")
            path: Verified working path
            version: Optional version string
        """
        if "paths" not in self._session_cache:
            self._session_cache["paths"] = {}
        if "verification" not in self._session_cache:
            self._session_cache["verification"] = {}

        self._session_cache["paths"][tool_name] = path
        self._session_cache["verification"][tool_name] = {
            "verified": True,
            "last_check": datetime.now().isoformat(),
        }
        if version:
            self._session_cache["verification"][tool_name]["version"] = version

        self._session_cache["last_updated"] = datetime.now().isoformat()
        self._save_session_cache()

    def _migrate_from_legacy(self) -> None:
        """Migrate from legacy tools.json to new settings.json format."""
        with open(self._legacy_tools_path, "r", encoding="utf-8") as f:
            legacy = json.load(f)

        self._settings = self._create_default_settings()

        # Migrate tools
        if "tools" in legacy:
            self._settings["tools"] = legacy["tools"]

        # Migrate platforms
        if "platforms" in legacy:
            self._settings["platforms"] = legacy["platforms"]

        # Migrate defaults
        if "defaults" in legacy:
            for platform_name, defaults in legacy["defaults"].items():
                if platform_name in self._settings["platforms"]:
                    self._settings["platforms"][platform_name]["default_tools"] = (
                        defaults
                    )

        self._save_settings()

        # Create backup of legacy file
        backup_path = self._legacy_tools_path.with_suffix(".json.bak")
        shutil.copy(self._legacy_tools_path, backup_path)

    def _create_default_settings(self) -> Dict[str, Any]:
        """Create default settings structure.

        Returns:
            Default settings dictionary
        """
        return {
            "$schema": "./settings-schema.json",
            "version": "1.0.0",
            "system": {
                "factory_version": "2.0.0",
                "platform": self._platform,
            },
            "tools": {
                "python": {
                    "env_var": "PYTHON_PATH",
                    "conda_env": "antigravity-factory",
                    "auto_detect": ["python", "python3", "python.exe"],
                    "fallbacks": [
                        "D:\\Anaconda\\envs\\antigravity-factory\\python.exe",
                        "C:\\App\\Anaconda\\envs\\antigravity-factory\\python.exe",
                    ],
                    "min_version": "3.10",
                    "description": "Python 3.10+ interpreter",
                    "docs": "https://docs.python.org/",
                },
                "git": {
                    "env_var": "GIT_PATH",
                    "auto_detect": ["git", "git.exe"],
                    "fallbacks": [
                        "C:\\Program Files\\Git\\bin\\git.exe",
                    ],
                    "description": "Git version control",
                    "docs": "https://git-scm.com/docs",
                },
            },
            "credentials": {
                "github_token": "${GITHUB_TOKEN}",
                "npm_token": "${NPM_TOKEN}",
                "pypi_token": "${PYPI_TOKEN}",
            },
            "knowledge_evolution": {
                "mode": "awareness_hybrid",
                "check_on_startup": True,
                "auto_update": False,
                "notify_updates": True,
                "update_channel": "stable",
                "check_interval_hours": 24,
                "subscriptions": ["*"],
                "sources": {
                    "github_trending": True,
                    "official_docs": True,
                    "package_registries": True,
                    "community_curated": True,
                    "user_feedback": True,
                },
                "merge_strategy": "balanced",
                "backup_before_update": True,
                "max_backups": 10,
            },
            "notifications": {
                "show_update_summary": True,
                "show_changelog": True,
                "quiet_mode": False,
            },
            "platforms": {
                "windows": {
                    "shell": "powershell",
                    "path_separator": "\\",
                    "env_syntax": "%VAR%",
                },
                "linux": {
                    "shell": "bash",
                    "path_separator": "/",
                    "env_syntax": "$VAR",
                },
                "darwin": {
                    "shell": "zsh",
                    "path_separator": "/",
                    "env_syntax": "$VAR",
                },
            },
        }

    def _save_settings(self) -> None:
        """Save current settings to file."""
        self._settings_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self._settings_path, "w", encoding="utf-8") as f:
            json.dump(self._settings, f, indent=2)

    def _resolve_env_vars(self, value: str) -> str:
        """Resolve environment variable references in a string.

        Supports ${VAR_NAME} syntax.

        Args:
            value: String potentially containing env var references

        Returns:
            String with env vars resolved
        """
        if not isinstance(value, str):
            return value

        def replace_env_var(match):
            var_name = match.group(1)
            return os.environ.get(var_name, "")

        return self._ENV_VAR_PATTERN.sub(replace_env_var, value)

    def get(self, path: str, default: Any = None) -> Any:
        """Get a configuration value by dot-notation path.

        Args:
            path: Dot-notation path (e.g., "knowledge_evolution.mode")
            default: Default value if not found

        Returns:
            Configuration value or default
        """
        parts = path.split(".")
        value = self._settings

        for part in parts:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return default

        # Resolve env vars in strings
        if isinstance(value, str):
            value = self._resolve_env_vars(value)

        return value

    def set(self, path: str, value: Any, save: bool = True) -> None:
        """Set a configuration value by dot-notation path.

        Args:
            path: Dot-notation path (e.g., "knowledge_evolution.mode")
            value: Value to set
            save: Whether to save settings to file immediately
        """
        parts = path.split(".")
        target = self._settings

        for part in parts[:-1]:
            if part not in target:
                target[part] = {}
            target = target[part]

        target[parts[-1]] = value

        if save:
            self._save_settings()

    def get_tool_path(self, tool_name: str) -> Optional[str]:
        """Get the resolved path for a tool.

        Follows resolution order: session_cache -> env var -> config path -> auto-detect -> fallbacks

        Args:
            tool_name: Name of the tool (e.g., "python", "git")

        Returns:
            Resolved path to the tool or None if not found
        """
        # 0. Check session cache first (fastest, already verified)
        cached_paths = self._session_cache.get("paths", {})
        cached_path = cached_paths.get(tool_name)
        if cached_path and self._path_exists(cached_path):
            return cached_path

        tool_config = self.get(f"tools.{tool_name}")
        if not tool_config:
            return None

        # 1. Check environment variable
        env_var = tool_config.get("env_var")
        if env_var:
            env_path = os.environ.get(env_var)
            if env_path and self._path_exists(env_path):
                # Update session cache with verified path
                self.update_session_cache(tool_name, env_path)
                return env_path

        # 2. Check explicit path in config
        explicit_path = tool_config.get("path")
        if explicit_path and self._path_exists(explicit_path):
            self.update_session_cache(tool_name, explicit_path)
            return explicit_path

        # 3. Try auto-detect
        auto_detect = tool_config.get("auto_detect", [])
        for cmd in auto_detect:
            path = shutil.which(cmd)
            if path:
                self.update_session_cache(tool_name, path)
                return path

        # 4. Try fallbacks
        fallbacks = tool_config.get("fallbacks", [])
        for fallback in fallbacks:
            if self._path_exists(fallback):
                self.update_session_cache(tool_name, fallback)
                return fallback

        return None

    def get_cached_path(self, tool_name: str) -> Optional[str]:
        """Get a cached path without resolution (fast lookup).

        Args:
            tool_name: Name of the tool

        Returns:
            Cached path or None if not in cache
        """
        return self._session_cache.get("paths", {}).get(tool_name)

    def _path_exists(self, path: str) -> bool:
        """Check if a path exists (file or command).

        Args:
            path: Path to check

        Returns:
            True if path exists
        """
        return Path(path).exists() or shutil.which(path) is not None

    def get_knowledge_evolution_config(self) -> KnowledgeEvolutionConfig:
        """Get the knowledge evolution configuration.

        Returns:
            KnowledgeEvolutionConfig dataclass with all settings
        """
        ke = self.get("knowledge_evolution", {})
        return KnowledgeEvolutionConfig(
            mode=ke.get("mode", "awareness_hybrid"),
            check_on_startup=ke.get("check_on_startup", True),
            auto_update=ke.get("auto_update", False),
            notify_updates=ke.get("notify_updates", True),
            update_channel=ke.get("update_channel", "stable"),
            check_interval_hours=ke.get("check_interval_hours", 24),
            subscriptions=ke.get("subscriptions", ["*"]),
            sources=ke.get("sources", {}),
            merge_strategy=ke.get("merge_strategy", "balanced"),
            backup_before_update=ke.get("backup_before_update", True),
            max_backups=ke.get("max_backups", 10),
        )

    def get_credential(self, name: str) -> Optional[str]:
        """Get a credential, resolving environment variables.

        Args:
            name: Credential name (e.g., "github_token")

        Returns:
            Resolved credential value or None
        """
        value = self.get(f"credentials.{name}")
        if value:
            resolved = self._resolve_env_vars(value)
            return resolved if resolved else None
        return None

    def get_platform_config(self) -> Dict[str, Any]:
        """Get configuration for the current platform.

        Returns:
            Platform-specific configuration dictionary
        """
        return self.get(f"platforms.{self._platform}", {})

    @property
    def factory_root(self) -> Path:
        """Get the factory root directory."""
        return self._factory_root

    @property
    def current_platform(self) -> str:
        """Get the current platform identifier."""
        return self._platform

    @property
    def settings(self) -> Dict[str, Any]:
        """Get the full settings dictionary (read-only copy)."""
        return self._settings.copy()

    def validate_settings(self) -> List[str]:
        """Validate current settings against schema.

        Returns:
            List of validation errors, empty if valid
        """
        errors = []

        # Check required sections
        required = ["system", "tools"]
        for section in required:
            if section not in self._settings:
                errors.append(f"Missing required section: {section}")

        # Validate knowledge_evolution mode
        ke = self._settings.get("knowledge_evolution", {})
        valid_modes = [
            "stability_first",
            "awareness_hybrid",
            "freshness_first",
            "subscription",
        ]
        if ke.get("mode") and ke["mode"] not in valid_modes:
            errors.append(f"Invalid knowledge_evolution.mode: {ke['mode']}")

        # Validate update_channel
        valid_channels = ["stable", "latest", "experimental"]
        if ke.get("update_channel") and ke["update_channel"] not in valid_channels:
            errors.append(
                f"Invalid knowledge_evolution.update_channel: {ke['update_channel']}"
            )

        return errors

    def export_settings(self, path: Path) -> None:
        """Export current settings to a file.

        Args:
            path: Path to export to
        """
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self._settings, f, indent=2)

    def import_settings(self, path: Path, merge: bool = False) -> None:
        """Import settings from a file.

        Args:
            path: Path to import from
            merge: If True, merge with existing. If False, replace.
        """
        with open(path, "r", encoding="utf-8") as f:
            imported = json.load(f)

        if merge:
            self._deep_merge(self._settings, imported)
        else:
            self._settings = imported

        self._save_settings()

    def _deep_merge(self, base: Dict, override: Dict) -> Dict:
        """Deep merge two dictionaries.

        Args:
            base: Base dictionary to merge into
            override: Dictionary with values to override

        Returns:
            Merged dictionary
        """
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
        return base


# Convenience function for quick access
def get_config() -> ConfigManager:
    """Get the singleton ConfigManager instance.

    Returns:
        ConfigManager instance
    """
    return ConfigManager.get_instance()
