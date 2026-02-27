#!/usr/bin/env python3
"""
Quick validation script for skills using global schema
"""

import sys
import os
import re
import json
from pathlib import Path

# Try to import jsonschema, but don't fail if not present (logic for quick/fallback)
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

    # Simple YAML-ish parser for when PyYAML isn't here
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


def validate_skill(skill_path, schema_path):
    """Validate a skill against the official schema."""
    skill_path = Path(skill_path)
    skill_md = skill_path / "SKILL.md"

    if not skill_md.exists():
        return False, "SKILL.md not found"

    content = skill_md.read_text(encoding="utf-8")
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
        return True, "Skill is valid!"
    else:
        # Fallback check for critical fields if jsonschema is missing
        required = schema.get("required", [])
        missing = [f for f in required if f not in data]
        if missing:
            return False, f"Missing required fields: {', '.join(missing)}"
        return True, "Skill is valid (minimal check, jsonschema missing)!"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python quick_validate.py <skill_directory>")
        sys.exit(1)

    # Resolve relative to repo root
    root = Path(__file__).resolve().parent.parent.parent.parent.parent.parent
    schema_path = root / "schemas" / "skill.schema.json"

    valid, message = validate_skill(sys.argv[1], schema_path)
    print(message)
    sys.exit(0 if valid else 1)
