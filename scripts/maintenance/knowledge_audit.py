#!/usr/bin/env python3
"""
Knowledge Audit Master Script for Antigravity Agent Factory.
Orchestrates link checking, dependency mapping, and knowledge debt detection.
Generates a weekly 'Knowledge Health' report.
"""

import os
import subprocess
import json
import re
import sys
from pathlib import Path
from datetime import datetime

# Configuration
REPO_ROOT = Path(__file__).resolve().parents[2]
AGENT_DIR = REPO_ROOT / ".agent"
WORKFLOWS_DIR = AGENT_DIR / "workflows"
KNOWLEDGE_DIR = AGENT_DIR / "knowledge"
SKILLS_DIR = AGENT_DIR / "skills"
REPORT_PATH = REPO_ROOT / "docs" / "audits" / "KNOWLEDGE_HEALTH.md"

PYTHON_CMD = [sys.executable]


def run_command(cmd, capture_output=True):
    try:
        result = subprocess.run(
            cmd, capture_output=capture_output, text=True, check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command {' '.join(cmd)}: {e.stderr}")
        return None


def detect_knowledge_debt():
    """Identifies low-content workflows and KIs."""
    debt_items = []

    # Check Workflows
    for wf in WORKFLOWS_DIR.rglob("*.md"):
        content = wf.read_text(encoding="utf-8")
        if len(content.split()) < 50:  # Threshold for 'thin' content
            debt_items.append(
                {
                    "type": "Workflow",
                    "path": str(wf.relative_to(REPO_ROOT)),
                    "reason": "Low content volume",
                }
            )

    # Check Knowledge Items
    for ki in KNOWLEDGE_DIR.rglob("*.json"):
        try:
            with open(ki, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not data.get("patterns") and not data.get("best_practices"):
                    debt_items.append(
                        {
                            "type": "Knowledge",
                            "path": str(ki.relative_to(REPO_ROOT)),
                            "reason": "No patterns or best practices",
                        }
                    )
        except Exception:
            pass

    return debt_items


def run_link_checker():
    """Runs the link checker and returns broken link count."""
    script = REPO_ROOT / "scripts" / "maintenance" / "audit" / "link_checker.py"
    output = run_command(PYTHON_CMD + [str(script), "--path", str(AGENT_DIR)])

    match = re.search(r"Broken Internal Links \((\d+)\)", output)
    return int(match.group(1)) if match else 0


def run_dependency_validator():
    """Runs the dependency validator and refreshes the map."""
    script = REPO_ROOT / "scripts" / "validation" / "dependency_validator.py"
    # Export the graph
    export_path = KNOWLEDGE_DIR / "core" / "artifact-dependency-map.json"
    run_command(PYTHON_CMD + [str(script), "--export", str(export_path)])

    # Get stats
    output = run_command(PYTHON_CMD + [str(script), "--stats"])
    try:
        return json.loads(output)
    except Exception:
        return {}


def generate_report(debt, broken_links, dep_stats):
    """Generates the KNOWLEDGE_HEALTH.md report."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report = [
        "# Knowledge Health Report",
        f"Generated: {now}",
        "",
        "## 📊 Summary Metrics",
        f"- **Broken Links**: {broken_links}",
        f"- **Knowledge Debt Items**: {len(debt)}",
        f"- **Total Artifacts**: {dep_stats.get('total_nodes', 'N/A')}",
        f"- **Total Dependencies**: {dep_stats.get('total_edges', 'N/A')}",
        "",
        "## 🛠️ Knowledge Debt",
        "| Type | Artifact Path | Reason |",
        "| :--- | :--- | :--- |",
    ]

    for item in debt:
        report.append(f"| {item['type']} | {item['path']} | {item['reason']} |")

    if not debt:
        report.append("| All clear | - | - |")

    report.append("\n## 🔗 Dependency Stats")
    nodes_by_type = dep_stats.get("nodes_by_type", {})
    for ntype, count in nodes_by_type.items():
        report.append(f"- **{ntype.capitalize()}s**: {count}")

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(report), encoding="utf-8")
    print(f"Report generated at {REPORT_PATH}")


def main():
    print("Starting Proactive Maintenance Audit...")

    print("Detecting Knowledge Debt...")
    debt = detect_knowledge_debt()

    print("Checking Links...")
    broken_links = run_link_checker()

    print("Validating Dependencies...")
    dep_stats = run_dependency_validator()

    print("Generating Health Report...")
    generate_report(debt, broken_links, dep_stats)

    print("Audit Complete.")


if __name__ == "__main__":
    main()
