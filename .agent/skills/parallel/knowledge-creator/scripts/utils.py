"""Shared utilities for knowledge-creator scripts."""

import json
from pathlib import Path


def parse_knowledge_json(path: Path) -> tuple[str, str, dict]:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data.get("title", ""), data.get("description", ""), data
