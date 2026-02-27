#!/usr/bin/env python3
"""
Quick validation script for blueprints using global schema
"""

import sys
import json
from pathlib import Path

try:
    from jsonschema import Draft7Validator

    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False


def validate_blueprint(path, schema_path):
    path = Path(path)
    if not path.exists():
        return False, f"Blueprint file not found at {path}"

    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"

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
        return True, "Blueprint is valid!"
    return True, "Blueprint is JSON (jsonschema missing)"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python quick_validate.py <blueprint_file_path>")
        sys.exit(1)

    root = Path(__file__).resolve().parent.parent.parent.parent.parent.parent
    schema_path = root / "schemas" / "blueprint.schema.json"

    valid, message = validate_blueprint(sys.argv[1], schema_path)
    print(message)
    sys.exit(0 if valid else 1)
