"""Shared utilities for workflow-creator scripts."""

import re
from pathlib import Path


def parse_workflow_md(path: Path) -> tuple[str, str, str]:
    content = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    desc = ""
    if match:
        for line in match.group(1).splitlines():
            if line.startswith("description:"):
                desc = line.split(":", 1)[1].strip().strip('"').strip("'")
    return path.stem, desc, content
