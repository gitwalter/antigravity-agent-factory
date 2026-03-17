#!/usr/bin/env python3
"""
Proactive Knowledge Synthesis — Phase 2: Autonomous Evolution.
Analyzes CHANGELOG.md and project ideas to identify missing Knowledge Items (KIs).
"""

import os
import sys
import json
import re
from datetime import datetime
from typing import List, Dict, Optional

# --- Configuration ---
ROOT_DIR = os.getcwd()
CHANGELOG_PATH = os.path.join(ROOT_DIR, "CHANGELOG.md")
KNOWLEDGE_MANIFEST = os.path.join(
    ROOT_DIR, ".agent", "knowledge", "knowledge-manifest.json"
)
IDEAS_DIR = os.path.join(ROOT_DIR, "knowledge", "ideas")
KNOWLEDGE_DIR = os.path.join(ROOT_DIR, ".agent", "knowledge")
TMP_DIR = os.path.join(ROOT_DIR, "tmp")


def load_manifest() -> Dict:
    if os.path.exists(KNOWLEDGE_MANIFEST):
        with open(KNOWLEDGE_MANIFEST, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"files": []}


def get_recent_entries() -> List[str]:
    """Extract recent entries from CHANGELOG.md."""
    if not os.path.exists(CHANGELOG_PATH):
        return []

    with open(CHANGELOG_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Split by version headers (## [x.y.z])
    version_blocks = re.split(r"## \[\d+\.\d+\.\d+\]", content)
    # Filter out the first block (intro) and keep the last 3 versions
    entries = [v.strip() for v in version_blocks[1:4] if v.strip()]
    return entries


def draft_knowledge_item(topic: str):
    """Draft a new Knowledge Item JSON in tmp/."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{topic}-patterns_{timestamp}.json"
    filepath = os.path.join(TMP_DIR, filename)

    ki_template = {
        "id": f"{topic}-patterns",
        "name": f"{topic.capitalize()} Patterns",
        "version": "1.0.0",
        "category": "integration",
        "description": f"Automatically identified patterns for {topic} based on recent project activity.",
        "patterns": {
            "example_implementation": {
                "description": "Example pattern detected during synthesis.",
                "code": f"# Implementation for {topic} goes here",
            }
        },
        "best_practices": [
            "Maintain architectural alignment",
            "Follow 5-layer architecture rules",
        ],
        "anti_patterns": ["Hardcoding IDs", "Skipping validation"],
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(ki_template, f, indent=4)
    return filepath


def scan_for_gaps(recent_changes: List[str], manifest: Dict):
    """Identify potential knowledge gaps based on keywords and ideas."""
    # Manifest files is a dict where keys are filenames
    known_topics = [fname.split("-")[0] for fname in manifest.get("files", {}).keys()]

    # Also check existing specialist names
    specialists = ["syarch", "wqss", "knops", "props", "exops", "pyai", "webex"]
    known_topics.extend(specialists)

    gaps = []
    # common patterns to look for
    keywords = [
        "plane",
        "rag",
        "mcp",
        "workflow",
        "automation",
        "dashboard",
        "validation",
        "synthesis",
    ]

    # Gather text from ideas too
    ideas_text = ""
    if os.path.exists(IDEAS_DIR):
        for root, dirs, files in os.walk(IDEAS_DIR):
            for f in files:
                if f.endswith(".md"):
                    with open(os.path.join(root, f), "r", encoding="utf-8") as ideaf:
                        ideas_text += ideaf.read() + "\n"

    all_source_text = "\n".join(recent_changes) + "\n" + ideas_text

    for kw in keywords:
        if kw.lower() in all_source_text.lower():
            # Check if this keyword represents a missing topic
            is_missing = True
            for topic in known_topics:
                if kw.lower() in topic.lower():
                    is_missing = False
                    break
            if is_missing:
                gaps.append(kw.lower())

    return list(set(gaps))


def main():
    print("--- Proactive Knowledge Synthesis v1.1.0 ---")
    manifest = load_manifest()
    recent = get_recent_entries()

    if not recent:
        print("No recent changes found in CHANGELOG.md.")
        return

    gaps = scan_for_gaps(recent, manifest)

    if gaps:
        print(f"Potential Knowledge Gaps Identified: {', '.join(gaps)}")
        for gap in gaps:
            path = draft_knowledge_item(gap)
            print(f"   [DRAFTED] {gap} -> {os.path.basename(path)}")
    else:
        print("No significant knowledge gaps identified in recent work.")


if __name__ == "__main__":
    if not os.path.exists(TMP_DIR):
        os.makedirs(TMP_DIR)
    main()
