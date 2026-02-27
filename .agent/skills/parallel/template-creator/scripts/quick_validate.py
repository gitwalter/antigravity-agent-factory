#!/usr/bin/env python3
"""
Quick validation script for templates using global schema
"""

import sys
import re
import json
from pathlib import Path

try:
    from jsonschema import Draft7Validator

    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False


def extract_metadata(path: Path):
    """Extract metadata from template file (handles header comments)."""
    content = path.read_text(encoding="utf-8")
    # Look for JSON-like block in comments or frontmatter
    match = re.search(r"\{.*\}", content, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except Exception:
            pass
    return None


def validate_template(path, schema_path):
    path = Path(path)
    if not path.exists():
        return False, f"Template file not found at {path}"

    data = extract_metadata(path)
    if data is None:
        return False, "No metadata found in template"

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
                path_str = ".".join(str(p) for p in err.path) or "root"
                msg += f"  - {path_str}: {err.message}\n"
            return False, msg
        return True, "Template metadata is valid!"
    return True, "Template metadata present (jsonschema missing)"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python quick_validate.py <template_file_path>")
        sys.exit(1)

    root = Path(__file__).resolve().parent.parent.parent.parent.parent.parent
    schema_path = root / "schemas" / "template.schema.json"

    valid, message = validate_template(sys.argv[1], schema_path)
    print(message)
    sys.exit(0 if valid else 1)
