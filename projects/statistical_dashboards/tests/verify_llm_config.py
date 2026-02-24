import os
import sys

# Ensure project root is in path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from projects.statistical_dashboards.core.ai_manager import AIManager
from projects.statistical_dashboards.core.config_manager import config_manager


def verify_llm_config():
    print("Verifying Centralized LLM Configuration...")

    # 1. Check ConfigManager directly
    config = config_manager.get_llm_config()
    print(f"Loaded Config: {config}")

    expected_primary = "gemini-2.5-flash"
    if config.get("primary_model") == expected_primary:
        print(f"✅ Success: ConfigManager primary model is {expected_primary}")
    else:
        print(
            f"❌ Failure: ConfigManager primary model is {config.get('primary_model')}"
        )

    # 2. Check AIManager initialization
    ai = AIManager()
    print(f"AIManager Model: {ai.model_name}")
    print(f"AIManager Fallback: {ai.fallback_model}")

    if ai.model_name == expected_primary:
        print(f"✅ Success: AIManager correctly initialized with {expected_primary}")
    else:
        print(f"❌ Failure: AIManager initialized with {ai.model_name}")


if __name__ == "__main__":
    verify_llm_config()
