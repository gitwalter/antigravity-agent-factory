import os
import logging
from typing import List, Optional, Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

from projects.rag_knowledge_explorer.core.config_manager import config_manager

logger = logging.getLogger(__name__)


class AIManager:
    """
    Standalone AIManager for RAG Knowledge Explorer.
    """

    def __init__(
        self, model_name: Optional[str] = None, temperature: Optional[float] = None
    ):
        llm_config = config_manager.get_llm_config()

        self.model_name = model_name or llm_config.get(
            "primary_model", "gemini-2.5-flash"
        )
        self.temperature = (
            temperature
            if temperature is not None
            else llm_config.get("default_temperature", 0.0)
        )
        self.fallback_model = llm_config.get("fallback_model", "gemini-2.5-flash-lite")

        self.api_key = os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not found in environment variables.")

        os.environ["LANGSMITH_TRACING"] = "true"
        os.environ["LANGSMITH_PROJECT"] = "rag-knowledge-explorer"

        try:
            self.llm = ChatGoogleGenerativeAI(
                model=self.model_name,
                google_api_key=self.api_key,
                temperature=self.temperature,
                convert_system_message_to_human=True,
            )
        except Exception as e:
            logger.error(f"Failed to initialize LLM with model {self.model_name}: {e}")
            self.llm = ChatGoogleGenerativeAI(
                model=self.fallback_model,
                google_api_key=self.api_key,
                temperature=self.temperature,
                convert_system_message_to_human=True,
            )
