"""Shared utilities for template-creator scripts."""

import re
from pathlib import Path
import json


def parse_template_metadata(path: Path) -> tuple[str, str, dict]:
    content = path.read_text(encoding="utf-8")
    match = re.search(r"\{.*\}", content, re.DOTALL)
    data = {}
    if match:
        try:
            data = json.loads(match.group(0))
        except Exception:
            pass
    return data.get("name", ""), data.get("description", ""), data
