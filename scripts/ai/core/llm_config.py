"""
Central LLM & Embedding Model Configuration.

Uses Pydantic for validation and structured logging.
Reads from config/llm_config.json at project root.
"""

import json
import os
import logging
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# ─── Configuration Models ─────────────────────────────────────────────────────


class LLMModelConfig(BaseModel):
    primary_model: str = Field(default="gemini-2.0-flash")
    fallback_model: str = Field(default="gemini-2.0-flash-lite")
    preview_model: str = Field(default="gemini-3-flash-preview")
    default_temperature: float = Field(default=0.0)


class EmbeddingConfig(BaseModel):
    model: str = Field(default="sentence-transformers/all-MiniLM-L6-v2")
    dimension: int = Field(default=384)


class GlobalAIConfig(BaseSettings):
    llm: LLMModelConfig = Field(default_factory=LLMModelConfig)
    embedding: EmbeddingConfig = Field(default_factory=EmbeddingConfig)

    model_config = SettingsConfigDict(
        env_prefix="AI_", env_nested_delimiter="__", extra="ignore"
    )


# ─── Config Helper ────────────────────────────────────────────────────────────


def _get_config_path() -> str:
    """Resolve project root and config path."""
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../../config/llm_config.json")
    )


def load_ai_config() -> GlobalAIConfig:
    """Load configuration from JSON file or environment variables."""
    path = _get_config_path()

    config_data = {}
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                config_data = json.load(f)
        except Exception as e:
            logging.warning(f"Failed to load AI config from {path}: {e}")

    # Pydantic Settings will merge JSON data (if passed) with Env Vars and Defaults
    return GlobalAIConfig(**config_data)


# ─── Global instance (singleton pattern) ─────────────────────────────────────

_config: Optional[GlobalAIConfig] = None


def get_config(reload: bool = False) -> GlobalAIConfig:
    """Get the global AI configuration."""
    global _config
    if _config is None or reload:
        _config = load_ai_config()
    return _config


# ─── Shorthand Accessors (Compatible with original API) ───────────────────────


def get_primary_model() -> str:
    return get_config().llm.primary_model


def get_fallback_model() -> str:
    return get_config().llm.fallback_model


def get_preview_model() -> str:
    return get_config().llm.preview_model


def get_temperature() -> float:
    return get_config().llm.default_temperature


def get_embedding_model() -> str:
    return get_config().embedding.model


def get_embedding_dimension() -> int:
    return get_config().embedding.dimension


if __name__ == "__main__":
    # Quick debug view
    print(get_config().model_dump_json(indent=2))
