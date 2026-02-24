import os
import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class ConfigManager:
    """
    Centralized configuration manager for global dashboard settings,
    including LLM model codes and integration parameters.
    """

    # Default model codes as specified by user
    DEFAULT_LLM_CONFIG = {
        "primary_model": "gemini-2.5-flash",
        "preview_model": "gemini-3-flash-preview",
        "fallback_model": "gemini-2.5-flash-lite",
        "default_temperature": 0.0,
    }

    def __init__(self):
        self._project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../")
        )
        self._config_file = os.path.join(self._project_root, "config", "settings.json")
        self._config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Loads configuration from settings.json or returns defaults."""
        if not os.path.exists(self._config_file):
            logger.info(
                f"Config file not found at {self._config_file}. Using defaults."
            )
            # Ensure config directory exists
            os.makedirs(os.path.dirname(self._config_file), exist_ok=True)
            return self.DEFAULT_LLM_CONFIG

        try:
            with open(self._config_file, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading config file: {e}")
            return self.DEFAULT_LLM_CONFIG

    def get_llm_config(self) -> Dict[str, Any]:
        """Returns the LLM-specific configuration."""
        return self._config.get("llm", self.DEFAULT_LLM_CONFIG)

    def update_llm_config(self, new_config: Dict[str, Any]):
        """Updates and persists model configuration."""
        self._config["llm"] = new_config
        try:
            with open(self._config_file, "w") as f:
                json.dump(self._config, f, indent=4)
            logger.info("Successfully updated centralized LLM configuration.")
        except Exception as e:
            logger.error(f"Failed to persist configuration: {e}")


# Global instance for easy access
config_manager = ConfigManager()
