import os
import pytest
from scripts.ai.core.llm_config import get_config, get_primary_model


def test_config_defaults():
    config = get_config(reload=True)
    assert config.llm.primary_model is not None
    assert config.embedding.dimension > 0


def test_shorthand_accessors():
    assert get_primary_model() == get_config().llm.primary_model
