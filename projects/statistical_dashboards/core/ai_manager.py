import os
import logging
from typing import List, Optional, Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

from core.config_manager import config_manager

logger = logging.getLogger(__name__)


class AIManager:
    """
    Handles interactions with Google Gemini LLMs for analytical insights and NLQ.
    Implements Phase 2: Intelligence Layer.
    """

    def __init__(
        self, model_name: Optional[str] = None, temperature: Optional[float] = None
    ):
        llm_config = config_manager.get_llm_config()

        # Priority: explicit arg > config file > default
        self.model_name = model_name or llm_config.get(
            "primary_model", "gemini-2.5-flash"
        )
        self.temperature = (
            temperature
            if temperature is not None
            else llm_config.get("default_temperature", 0.0)
        )
        self.fallback_model = llm_config.get("fallback_model", "gemini-1.5-flash")

        self.api_key = os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not found in environment variables.")

        # Configure LangSmith Tracing
        os.environ["LANGSMITH_TRACING"] = "true"
        os.environ["LANGSMITH_PROJECT"] = "antigravity-stats-dashboard"

        try:
            # Using centralized model config (e.g., gemini-2.5-flash or gemini-3-flash-preview)
            self.llm = ChatGoogleGenerativeAI(
                model=self.model_name,
                google_api_key=self.api_key,
                temperature=self.temperature,
                convert_system_message_to_human=True,
            )
        except Exception as e:
            logger.error(f"Failed to initialize LLM with model {self.model_name}: {e}")
            # Reliable fallback from config
            self.llm = ChatGoogleGenerativeAI(
                model=self.fallback_model,
                google_api_key=self.api_key,
                temperature=self.temperature,
                convert_system_message_to_human=True,
            )

    def generate_insight(self, context: str, data_summary: str) -> str:
        """
        Generates a plain-language insight based on statistical results.
        """
        system_prompt = (
            "You are an expert data scientist and business analyst at Antigravity Factory. "
            "Your goal is to explain complex statistical results to non-technical managers. "
            "Keep your tone professional, actionable, and concise. "
            "Use Markdown formatting for emphasis."
        )

        user_prompt = (
            f"### Context: {context}\n"
            f"### Data Summary/Results:\n{data_summary}\n\n"
            "Please provide a 2-3 sentence insight that explains what these numbers mean "
            "for the business and what action (if any) should be taken."
        )

        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt),
            ]
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            logger.error(f"Error generating AI insight: {e}")
            return f"Error generating automated insight: {str(e)}"

    def nlq_to_viz(self, query: str, columns: List[str]) -> Dict[str, Any]:
        """
        Processes a natural language query and suggests a visualization type and columns.
        """
        system_prompt = (
            "You are a visualization assistant. Given a list of available columns and a user query, "
            "determine the best visualization type and which columns to use."
        )

        user_prompt = (
            f"Available Columns: {', '.join(columns)}\n"
            f"User Query: '{query}'\n\n"
            "Return a JSON object with keys: 'chart_type' (scatter, line, bar, heatmap), "
            "'x_axis', 'y_axis', and 'reasoning'."
        )

        try:
            import json

            response = self.llm.invoke(user_prompt)
            # Assuming the LLM returns a clean JSON block or we try to parse it
            content = response.content
            # Simple cleanup if the LLM adds markdown backticks
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()

            return json.loads(content)
        except Exception as e:
            logger.error(f"Error in NLQ to Viz: {e}")
            return {"error": str(e)}

    def explain_anomaly(self, anomaly_data: Dict[str, Any], context: str) -> str:
        """
        Explains why a specific data point is considered an anomaly.
        """
        user_prompt = (
            f"Context: {context}\n"
            f"Anomaly Details: {anomaly_data}\n\n"
            "Explain why this point is an outlier and suggest possible operational causes "
            "(e.g., sensor error, shift change, batch delay)."
        )

        try:
            response = self.llm.invoke(user_prompt)
            return response.content
        except Exception as e:
            logger.error(f"Error explaining anomaly: {e}")
            return f"Could not generate anomaly explanation: {str(e)}"
