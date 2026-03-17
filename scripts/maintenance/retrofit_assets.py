#!/usr/bin/env python3
"""
Retrofit Assets — Phase 2: Autonomous Evolution.
Ensures repository-wide compliance with evolving schemas and metadata standards.
"""

import os
import sys
import yaml
import json
import re
from typing import List, Dict, Optional

# --- Configuration ---
ROOT_DIR = os.getcwd()
AGENT_DIR = os.path.join(ROOT_DIR, ".agent")
WORKFLOWS_DIR = os.path.join(AGENT_DIR, "workflows")
SKILLS_DIR = os.path.join(AGENT_DIR, "skills")
AGENTS_DIR = os.path.join(AGENT_DIR, "agents")

TARGET_VERSION = "2.0.0"


def retrofit_markdown_asset(filepath: str):
    """Retrofit a markdown asset (workflow, skill, agent) with frontmatter updates."""
    if not os.path.exists(filepath):
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Simple frontmatter extractor
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not fm_match:
        return False

    fm_raw = fm_match.group(1)
    # SCRUB PROBLEM: Some frontmatter has markdown bolding like - **Memory Hook**
    # This confuses the YAML parser. We should strip it for the pure metadata.
    fm_clean = re.sub(r"\*\*(.*?)\*\*", r"\1", fm_raw)

    body = content[fm_match.end() :]

    try:
        data = yaml.safe_load(fm_clean)
    except Exception as e:
        print(f"Error parsing YAML in {filepath}: {e}")
        return False

    changed = False

    # Update version if missing or lower
    current_ver = str(data.get("version", "1.0.0"))
    if current_ver < TARGET_VERSION:
        data["version"] = TARGET_VERSION
        changed = True

    # Ensure mandatory fields (Prerequisites, best_practices for skills etc)
    # This is a baseline, can be specialized

    if changed:
        new_fm = yaml.dump(data, sort_keys=False)
        new_content = f"---\n{new_fm}---\n{body}"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True

    return False


def main():
    print("--- Retrofit Asset Migration v1.0.0 ---")
    print(f"Target Version: {TARGET_VERSION}")

    total_updated = 0

    # Scan workflows
    for f in os.listdir(WORKFLOWS_DIR):
        if f.endswith(".md"):
            if retrofit_markdown_asset(os.path.join(WORKFLOWS_DIR, f)):
                total_updated += 1
                print(f"   [RETROFITTED] Workflow: {f}")

    print(f"\nMigration Complete. Total Assets Updated: {total_updated}")


if __name__ == "__main__":
    main()
