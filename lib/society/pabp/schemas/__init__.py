"""
PABP Schema Validation Module

Provides schema loading and validation utilities for the Portable Agent
Behavior Protocol (PABP) v1.0.0 component types.

Schemas sourced from: https://github.com/gitwalter/antigravity-agent-factory

Supported component types:
    agent, skill, knowledge, workflow, blueprint, attestation,
    contract, identity, protocol, rule, template
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Directory containing all .schema.json files
SCHEMA_DIR = Path(__file__).parent

# All supported PABP component types
COMPONENT_TYPES = [
    "agent",
    "skill",
    "knowledge",
    "workflow",
    "blueprint",
    "attestation",
    "contract",
    "identity",
    "protocol",
    "rule",
    "template",
]


def _load_schema(component_type: str) -> Dict[str, Any]:
    """Load a JSON Schema file for the given component type.

    Args:
        component_type: One of the COMPONENT_TYPES (e.g. ``"agent"``).

    Returns:
        Parsed JSON Schema as a dict.

    Raises:
        FileNotFoundError: If the schema file is missing.
        ValueError: If ``component_type`` is not recognised.
    """
    if component_type not in COMPONENT_TYPES:
        raise ValueError(
            f"Unknown component type '{component_type}'. "
            f"Must be one of: {', '.join(COMPONENT_TYPES)}"
        )
    schema_path = SCHEMA_DIR / f"{component_type}.schema.json"
    with open(schema_path, "r", encoding="utf-8-sig") as fh:
        return json.load(fh)


def get_schema(component_type: str) -> Dict[str, Any]:
    """Public accessor – returns the parsed schema dict for *component_type*."""
    return _load_schema(component_type)


def get_all_schemas() -> Dict[str, Dict[str, Any]]:
    """Return a mapping of every component type to its parsed schema."""
    return {ct: _load_schema(ct) for ct in COMPONENT_TYPES}


def validate(
    data: Dict[str, Any], component_type: Optional[str] = None
) -> Tuple[bool, List[str]]:
    """Validate *data* against its PABP schema.

    If *component_type* is ``None`` it is inferred from ``data["$type"]``.

    Returns:
        ``(is_valid, errors)`` where *errors* is a list of human-readable
        error messages (empty when valid).

    Note:
        This performs basic structural validation without requiring
        ``jsonschema`` as a dependency.  For full JSON-Schema validation
        install ``jsonschema`` and call :func:`validate_strict`.
    """
    errors: List[str] = []

    # Resolve component type
    if component_type is None:
        component_type = data.get("$type")
        if component_type is None:
            return False, [
                "Missing '$type' field and no component_type argument provided"
            ]

    if component_type not in COMPONENT_TYPES:
        return False, [f"Unknown component type: '{component_type}'"]

    schema = _load_schema(component_type)

    # Check required fields
    required = schema.get("required", [])
    for field in required:
        if field not in data:
            errors.append(f"Missing required field: '{field}'")

    # Check $pabp version
    if "$pabp" in data and data["$pabp"] != "1.0.0":
        errors.append(f"Unsupported PABP version: '{data['$pabp']}' (expected '1.0.0')")

    # Check $type matches
    if "$type" in data and data["$type"] != component_type:
        errors.append(
            f"$type mismatch: data has '{data['$type']}' but validating against '{component_type}'"
        )

    # Basic type checks for known properties
    schema_props = schema.get("properties", {})
    for key, value in data.items():
        if key in schema_props:
            prop_schema = schema_props[key]
            expected_type = prop_schema.get("type")
            if expected_type and not _type_matches(value, expected_type):
                errors.append(
                    f"Field '{key}': expected type '{expected_type}', "
                    f"got '{type(value).__name__}'"
                )

    return (len(errors) == 0, errors)


def validate_strict(
    data: Dict[str, Any], component_type: Optional[str] = None
) -> Tuple[bool, List[str]]:
    """Full JSON-Schema validation using the ``jsonschema`` library.

    Raises:
        ImportError: If ``jsonschema`` is not installed.
    """
    try:
        import jsonschema  # type: ignore
    except ImportError:
        raise ImportError(
            "The 'jsonschema' package is required for strict validation. "
            "Install it with: pip install jsonschema"
        )

    if component_type is None:
        component_type = data.get("$type")
        if component_type is None:
            return False, [
                "Missing '$type' field and no component_type argument provided"
            ]

    schema = _load_schema(component_type)
    errors: List[str] = []

    validator = jsonschema.Draft7Validator(schema)
    for error in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        errors.append(
            f"{'.'.join(str(p) for p in error.path) or '(root)'}: {error.message}"
        )

    return (len(errors) == 0, errors)


def _type_matches(value: Any, json_type: str) -> bool:
    """Check if a Python value matches a JSON Schema type string."""
    type_map = {
        "string": str,
        "integer": int,
        "number": (int, float),
        "boolean": bool,
        "array": list,
        "object": dict,
    }
    expected = type_map.get(json_type)
    if expected is None:
        return True  # Unknown type — skip check
    # In JSON, booleans are not integers
    if json_type == "integer" and isinstance(value, bool):
        return False
    return isinstance(value, expected)
