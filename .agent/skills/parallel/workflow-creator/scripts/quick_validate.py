#!/usr/bin/env python3
"""
Quick validation script for workflows using global schema
"""

import sys
import os
import re
import json
from pathlib import Path

try:
    from jsonschema import Draft7Validator

    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False


def extract_frontmatter(content: str):
    """Simple frontmatter extraction."""
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
            result[k] = v
    return result


def validate_workflow(workflow_path, schema_path):
    """Validate a workflow against the official schema."""
    workflow_path = Path(workflow_path)
    if not workflow_path.exists():
        return False, f"Workflow file not found at {workflow_path}"

    content = workflow_path.read_text(encoding="utf-8")
    data = extract_frontmatter(content)
    if data is None:
        return False, "No YAML frontmatter found"

    if not Path(schema_path).exists():
        return False, f"Schema file not found at {schema_path}"

    with open(schema_path, encoding="utf-8") as f:
        schema = json.load(f)

    if HAS_JSONSCHEMA:
        validator = Draft7Validator(schema)
        errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
        if errors:
            msg = "Schema validation failed:\n"
            for err in errors:
                path = ".".join(str(p) for p in err.path) or "root"
                msg += f"  - {path}: {err.message}\n"
            return False, msg
        return True, "Workflow is valid!"
    return True, "Workflow frontmatter present (jsonschema missing)"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python quick_validate.py <workflow_file_path>")
        sys.exit(1)

    root = Path(__file__).resolve().parent.parent.parent.parent.parent.parent
    schema_path = root / "schemas" / "workflow.schema.json"

    valid, message = validate_workflow(sys.argv[1], schema_path)
    print(message)
    sys.exit(0 if valid else 1)
