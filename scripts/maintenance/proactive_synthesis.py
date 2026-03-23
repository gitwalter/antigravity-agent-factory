#!/usr/bin/env python3
"""
Proactive Knowledge Synthesis — Phase 2: Autonomous Evolution.
Analyzes CHANGELOG.md, project ideas, and recent walkthroughs to identify missing Knowledge Items (KIs).
Acts as a Success & Error Knowledge Bridge.
"""

import os
import sys
import json
import re
import glob
from datetime import datetime
from typing import List, Dict, Optional

# --- Configuration ---
ROOT_DIR = os.getcwd()
CHANGELOG_PATH = os.path.join(ROOT_DIR, "CHANGELOG.md")
KNOWLEDGE_MANIFEST = os.path.join(
    ROOT_DIR, ".agent", "knowledge", "core", "knowledge-manifest.json"
)
IDEAS_DIR = os.path.join(ROOT_DIR, "knowledge", "ideas")
KNOWLEDGE_DIR = os.path.join(ROOT_DIR, ".agent", "knowledge")
TMP_DIR = os.path.join(ROOT_DIR, "tmp")
BRAIN_DIR = os.path.expanduser(os.path.join("~", ".gemini", "antigravity", "brain"))


def load_manifest() -> Dict:
    if os.path.exists(KNOWLEDGE_MANIFEST):
        with open(KNOWLEDGE_MANIFEST, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"files": {}}


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


def get_recent_walkthroughs() -> List[str]:
    """Scan brain directory for recent walkthrough.md files to find success patterns."""
    walkthroughs = []
    if not os.path.exists(BRAIN_DIR):
        print(f"Brain dir not found: {BRAIN_DIR}")
        return walkthroughs

    for root, dirs, files in os.walk(BRAIN_DIR):
        if "walkthrough.md" in files:
            path = os.path.join(root, "walkthrough.md")
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    walkthroughs.append(f.read())
            except Exception as e:
                print(f"Could not read {path}: {e}")
    return walkthroughs


def draft_knowledge_item(topic: str, context: str = ""):
    """Draft a new Knowledge Item JSON in tmp/."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_topic = re.sub(r"[^a-zA-Z0-9]", "-", topic).lower()
    filename = f"{safe_topic}-patterns_{timestamp}.json"
    filepath = os.path.join(TMP_DIR, filename)

    ki_template = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "id": f"{safe_topic}-patterns",
        "title": f"{topic.title()} Patterns",
        "version": "1.0.0",
        "category": "integration",
        "description": f"Automatically identified patterns for {topic} based on recent project successes and activity.",
        "axiomAlignment": {
            "A1_verifiability": "Generated from verifiable walkthroughs",
            "A2_user_primacy": "Automates knowledge capture",
            "A3_transparency": "Clearly traces success paths",
            "A4_non_harm": "Read-only background synthesis process",
            "A5_consistency": "Enforces factory standardized patterns",
        },
        "patterns": {
            "success_pattern": {
                "description": f"Extracted success path for {topic}.",
                "use_when": f"Implementing or integrating {topic}",
                "code_example": f"// Context found: {context[:500]}..."
                if context
                else "// Implementation goes here",
                "best_practices": [
                    "Maintain architectural alignment",
                    "Verify memory access before executing",
                ],
            }
        },
        "related_skills": ["generating-documentation"],
        "related_knowledge": ["factory-patterns.json"],
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(ki_template, f, indent=4)
    return filepath


def analyze_factory_evolution(
    recent_changes: List[str], walkthroughs: List[str], manifest: Dict
):
    """Identify potential knowledge gaps and success patterns based on keywords and ideas."""
    known_topics = [fname.split("-")[0] for fname in manifest.get("files", {}).keys()]
    specialists = ["syarch", "wqss", "knops", "props", "exops", "pyai", "webex"]
    known_topics.extend(specialists)

    gaps = {}
    keywords = [
        "plane",
        "rag",
        "mcp",
        "workflow",
        "automation",
        "dashboard",
        "validation",
        "synthesis",
        "federated context",
        "ssgm",
        "memory broker",
        "success bridge",
    ]

    ideas_text = ""
    if os.path.exists(IDEAS_DIR):
        for root, dirs, files in os.walk(IDEAS_DIR):
            for f in files:
                if f.endswith(".md"):
                    with open(os.path.join(root, f), "r", encoding="utf-8") as ideaf:
                        ideas_text += ideaf.read() + "\n"

    all_source_text = (
        "\n".join(recent_changes) + "\n" + ideas_text + "\n" + "\n".join(walkthroughs)
    )

    for kw in keywords:
        if kw.lower() in all_source_text.lower():
            is_missing = True
            for topic in known_topics:
                # Handle cases where known_topic might contain hyphens
                if kw.lower() in topic.lower().replace("-", " "):
                    is_missing = False
                    break
            if is_missing:
                # Store a snippet of context for the draft
                idx = all_source_text.lower().find(kw.lower())
                context = all_source_text[
                    max(0, idx - 100) : min(len(all_source_text), idx + 100)
                ]
                gaps[kw.lower()] = context

    return gaps


def consolidate_drafts():
    """Moves verified drafts from tmp/ to .agent/knowledge/."""
    # Print intention; manual review is generally required before consolidation
    drafts = glob.glob(os.path.join(TMP_DIR, "*-patterns_*.json"))
    if drafts:
        print(
            f"Found {len(drafts)} drafts in {TMP_DIR}. Review, refine, and move manually to {KNOWLEDGE_DIR}."
        )
    else:
        print("No verified drafts to consolidate.")


def main():
    print("--- Proactive Knowledge Synthesis v1.2.0 (Success & Error Bridge) ---")

    # Handle consolidation requested via arg
    if len(sys.argv) > 1 and sys.argv[1] == "--consolidate":
        consolidate_drafts()
        return

    manifest = load_manifest()
    recent = get_recent_entries()
    walkthroughs = get_recent_walkthroughs()

    if not recent and not walkthroughs:
        print("No recent changes or walkthroughs found in defined sources.")
        return

    gaps = analyze_factory_evolution(recent, walkthroughs, manifest)

    if gaps:
        print(
            f"Potential Knowledge Gaps / Success Patterns Identified: {', '.join(gaps.keys())}"
        )
        for gap, context in gaps.items():
            path = draft_knowledge_item(gap, context)
            print(f"   [DRAFTED] {gap} -> {os.path.basename(path)}")
    else:
        print("No significant new patterns identified.")


if __name__ == "__main__":
    if not os.path.exists(TMP_DIR):
        os.makedirs(TMP_DIR)
    main()
