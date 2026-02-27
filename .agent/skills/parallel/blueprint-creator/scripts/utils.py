"""Shared utilities for blueprint-creator scripts."""

import json
from pathlib import Path


def parse_blueprint_json(path: Path) -> tuple[str, str, dict]:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data.get("id", ""), data.get("name", ""), data
