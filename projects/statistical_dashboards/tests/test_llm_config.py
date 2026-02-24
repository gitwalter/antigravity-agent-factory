import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Ensure project root is in path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
PROJECT_APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)
if PROJECT_APP_ROOT not in sys.path:
    sys.path.append(PROJECT_APP_ROOT)

from core.config_manager import ConfigManager
from core.ai_manager import AIManager


class TestLLMConfiguration(unittest.TestCase):
    def setUp(self):
        # Create a temporary config manager to avoid messing with real settings
        self.config_manager = ConfigManager()

    def test_config_manager_load_defaults(self):
        """Test that ConfigManager loads default values correctly."""
        config = self.config_manager.get_llm_config()
        self.assertIn("primary_model", config)
        self.assertEqual(config["primary_model"], "gemini-2.5-flash")

    @patch("core.ai_manager.ChatGoogleGenerativeAI")
    @patch("core.ai_manager.config_manager")
    def test_ai_manager_uses_config(self, mock_config, mock_llm):
        """Test that AIManager correctly uses the centralized config values."""
        # Setup mock config
        mock_config.get_llm_config.return_value = {
            "primary_model": "test-primary-model",
            "fallback_model": "test-fallback-model",
            "default_temperature": 0.5,
        }

        # Initialize AIManager
        ai = AIManager()

        # Verify it used the values from the mock config
        self.assertEqual(ai.model_name, "test-primary-model")
        self.assertEqual(ai.temperature, 0.5)

        # Verify LLM was initialized with correct parameters
        mock_llm.assert_called_with(
            model="test-primary-model",
            google_api_key=os.environ.get("GEMINI_API_KEY"),
            temperature=0.5,
            convert_system_message_to_human=True,
        )

    def test_ai_manager_explicit_override(self):
        """Test that explicit arguments to AIManager override the config file."""
        ai = AIManager(model_name="explicit-model", temperature=0.9)
        self.assertEqual(ai.model_name, "explicit-model")
        self.assertEqual(ai.temperature, 0.9)


if __name__ == "__main__":
    unittest.main()
