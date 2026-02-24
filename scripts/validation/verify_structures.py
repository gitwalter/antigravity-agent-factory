import os
import json
import re
from pathlib import Path


def verify_knowledge_json(file_path):
    """Verify knowledge JSON structure."""
    errors = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        required_fields = ["id", "name", "version", "category", "description"]
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")

        if "patterns" not in data or not isinstance(data["patterns"], dict):
            errors.append("Missing or invalid 'patterns' object")

        if "best_practices" not in data or not isinstance(data["best_practices"], list):
            errors.append("Missing or invalid 'best_practices' array")

        if "anti_patterns" not in data or not isinstance(data["anti_patterns"], list):
            errors.append("Missing or invalid 'anti_patterns' array")

        file_id = Path(file_path).stem
        if data.get("id") != file_id:
            errors.append(f"ID mismatch: '{data.get('id')}' vs filename '{file_id}'")

    except Exception as e:
        errors.append(f"Parse error: {str(e)}")
    return errors


def verify_workflow_md(file_path):
    """Verify workflow markdown structure."""
    errors = []
    try:
        content = Path(file_path).read_text(encoding="utf-8")

        # Remove frontmatter
        cleaned_content = content.strip()
        if cleaned_content.startswith("---"):
            parts = cleaned_content.split("---", 2)
            if len(parts) >= 3:
                cleaned_content = parts[2].lstrip()

        if not cleaned_content.startswith("# "):
            errors.append("Missing H1 title")

        if "## Overview" not in content and "# " not in content:
            errors.append("Missing Overview section")

        if "## Trigger Conditions" not in content:
            errors.append("Missing Trigger Conditions section")

        if "Version:" not in content and "**Version:**" not in content:
            errors.append("Missing Version declaration")

        if (
            "Trigger Examples:" not in content
            and "**Trigger Examples:**" not in content
        ):
            errors.append("Missing Trigger Examples pattern")

    except Exception as e:
        errors.append(f"Read error: {str(e)}")
    return errors


def main():
    root = Path(__file__).parent.parent.parent
    knowledge_dir = root / ".agent" / "knowledge"
    workflow_dir = root / ".agent" / "workflows"

    print("--- Structural Verification Report ---")

    total_errors = 0

    print("\n[Knowledge JSONs]")
    excluded_json = [
        "-catalog.json",
        "-registry.json",
        "manifest.json",
        "dependency-graph.json",
        "project-info.json",
        "memory-config.json",
        "version-registry.json",
    ]
    for f in knowledge_dir.glob("*.json"):
        if any(f.name.endswith(ex) or f.name == ex for ex in excluded_json):
            continue
        errs = verify_knowledge_json(f)
        if errs:
            print(f"FAIL: {f.name}")
            for e in errs:
                print(f"  - {e}")
            total_errors += len(errs)
        else:
            print(f"PASS: {f.name}")

    print("\n[Workflow Markdowns]")
    for f in workflow_dir.rglob("*.md"):
        if "organization" in f.parts:
            continue
        errs = verify_workflow_md(f)
        if errs:
            print(f"FAIL: {f.name}")
            for e in errs:
                print(f"  - {e}")
            total_errors += len(errs)
        else:
            print(f"PASS: {f.name}")

    print(f"\nTotal structural errors found: {total_errors}")
    exit(1 if total_errors > 0 else 0)


if __name__ == "__main__":
    main()
