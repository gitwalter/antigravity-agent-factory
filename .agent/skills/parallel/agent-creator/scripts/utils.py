"""Shared utilities for agent-creator scripts."""

import re
from pathlib import Path


def extract_frontmatter(content: str):
    """Simple frontmatter extraction logic."""
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None

    text = match.group(1)
    result = {}
    for line in text.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            if v.startswith("[") and v.endswith("]"):
                v = [i.strip().strip('"').strip("'") for i in v[1:-1].split(",")]
            elif v.lower() == "true":
                v = True
            elif v.lower() == "false":
                v = False
            result[k] = v
    return result


def parse_agent_md(agent_path: Path) -> tuple[str, str, str]:
    """Parse an agent .md file, returning (name, description, full_content)."""
    content = agent_path.read_text(encoding="utf-8")
    data = extract_frontmatter(content)
    if not data:
        raise ValueError(f"Agent {agent_path} missing frontmatter")

    return data.get("name", ""), data.get("description", ""), content
