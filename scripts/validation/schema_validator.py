#!/usr/bin/env python3
"""
Schema Validator - Full JSON Schema Validation for Factory Artifacts
====================================================================

Validates all Factory artifacts against their canonical JSON Schema definitions
in the ``schemas/`` directory using the ``jsonschema`` library.

Supported artifact types:
    - agents   (.cursor/agents/*.md YAML frontmatter)
    - skills   (.cursor/skills/*/SKILL.md YAML frontmatter)
    - knowledge (knowledge/*.json)
    - blueprints (blueprints/*/blueprint.json)
    - workflows  (workflows/**/*.md YAML frontmatter)
    - templates  (templates/**/*.j2, *.tmpl header metadata)
    - registry   (artifacts/registry.json)

Usage:
    python scripts/validation/schema_validator.py                    # Validate all
    python scripts/validation/schema_validator.py --type agent       # Validate agents only
    python scripts/validation/schema_validator.py --type knowledge   # Validate knowledge only
    python scripts/validation/schema_validator.py --verbose          # Verbose output
    python scripts/validation/schema_validator.py --summary          # Summary only

Exit Codes:
    0 - All validations pass
    1 - One or more validation errors found

Requirements:
    - Python 3.10+
    - jsonschema >= 4.17.0
    - PyYAML (optional, falls back to regex parser)

Author: Antigravity Agent Factory
Version: 1.0.0
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from jsonschema import Draft7Validator
except ImportError:
    print(
        "ERROR: jsonschema package required. Install with: pip install jsonschema>=4.17.0"
    )
    sys.exit(1)

try:
    import yaml

    HAS_YAML = True
except ImportError:
    HAS_YAML = False

# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent.parent
SCHEMAS_DIR = ROOT / "schemas"

ARTIFACT_DIRS = {
    "agent": ROOT / ".cursor" / "agents",
    "skill": ROOT / ".cursor" / "skills",
    "knowledge": ROOT / ".agent" / "knowledge",
    "blueprint": ROOT / "blueprints",
    "workflow": ROOT / "workflows",
    "template": ROOT / "templates",
    "registry": ROOT / "artifacts",
}

# Map of artifact type -> schema filename stem
SCHEMA_MAP = {
    "agent": "agent",
    "skill": "skill",
    "knowledge": "knowledge-file",
    "blueprint": "blueprint",
    "workflow": "workflow",
    "template": "template",
    "python-agent": "python-agent",
    "registry": "registry",
    "catalog": "catalog",
}

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)


# ---------------------------------------------------------------------------
@dataclass
class ValidationResult:
    """Result of validating a single artifact."""

    path: str
    artifact_type: str
    valid: bool
    errors: List[str] = field(default_factory=list)


@dataclass
class ValidationReport:
    """Aggregated validation report across all artifact types."""

    results: List[ValidationResult] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.results)

    @property
    def passed(self) -> int:
        return sum(1 for r in self.results if r.valid)

    @property
    def failed(self) -> int:
        return sum(1 for r in self.results if not r.valid)

    @property
    def ok(self) -> bool:
        return self.failed == 0

    def summary(self) -> str:
        """Return a human-readable summary string."""
        lines = [f"Schema Validation: {self.passed}/{self.total} passed"]
        if not self.ok:
            for r in self.results:
                if not r.valid:
                    lines.append(f"  FAIL {r.path}")
                    for err in r.errors[:5]:
                        lines.append(f"       - {err}")
                    if len(r.errors) > 5:
                        lines.append(f"       ... and {len(r.errors) - 5} more")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
def parse_yaml(text: str) -> Dict[str, Any]:
    """Parse YAML text into a dictionary.

    Uses PyYAML when available, falling back to a simple regex parser when
    PyYAML is absent **or** when it fails (e.g. frontmatter contains template
    expressions like ``{directories.patterns}`` that conflict with YAML flow
    mapping syntax).

    Args:
        text: Raw YAML string.

    Returns:
        Parsed dictionary.
    """
    if HAS_YAML:
        try:
            result = yaml.safe_load(text)
            if isinstance(result, dict):
                return result
        except yaml.YAMLError:
            pass  # fall through to simple parser
    return _parse_yaml_simple(text)


def _parse_yaml_simple(text: str) -> Dict[str, Any]:
    """Fallback regex-based YAML parser for frontmatter."""
    result: Dict[str, Any] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            items = [
                i.strip().strip("'\"") for i in value[1:-1].split(",") if i.strip()
            ]
            result[key] = items
        elif value.lower() in ("true", "false"):
            result[key] = value.lower() == "true"
        elif value.isdigit():
            result[key] = int(value)
        else:
            result[key] = value
    return result


def extract_frontmatter(content: str) -> Optional[Dict[str, Any]]:
    """Extract and parse YAML frontmatter from markdown content.

    Args:
        content: Full markdown file content.

    Returns:
        Parsed frontmatter dict, or None if no frontmatter found.
    """
    match = FRONTMATTER_RE.match(content)
    if not match:
        return None
    return parse_yaml(match.group(1))


# ---------------------------------------------------------------------------
def load_schemas() -> Dict[str, Dict[str, Any]]:
    """Load all JSON schemas from the schemas/ directory.

    Returns:
        Dict mapping schema key (e.g. ``"agent"``) to the parsed schema object.
    """
    schemas: Dict[str, Dict[str, Any]] = {}
    if not SCHEMAS_DIR.exists():
        return schemas
    for schema_file in sorted(SCHEMAS_DIR.glob("*.schema.json")):
        try:
            with open(schema_file, encoding="utf-8") as f:
                schema = json.load(f)
            key = schema_file.stem.replace(".schema", "")
            Draft7Validator.check_schema(schema)
            schemas[key] = schema
        except Exception as exc:
            print(f"WARNING: Failed to load schema {schema_file.name}: {exc}")
    return schemas


# ---------------------------------------------------------------------------
def discover_agents() -> List[Path]:
    """Discover all agent markdown files."""
    d = ARTIFACT_DIRS["agent"]
    if not d.exists():
        return []
    return sorted(p for p in d.rglob("*.md") if p.name != "README.md")


def discover_skills() -> List[Path]:
    """Discover all SKILL.md files."""
    d = ARTIFACT_DIRS["skill"]
    if not d.exists():
        return []
    return sorted(d.rglob("SKILL.md"))


def discover_knowledge() -> List[Path]:
    """Discover all knowledge JSON files (top-level only)."""
    d = ARTIFACT_DIRS["knowledge"]
    if not d.exists():
        return []
    return sorted(d.glob("*.json"))


def discover_blueprints() -> List[Path]:
    """Discover all blueprint.json files."""
    d = ARTIFACT_DIRS["blueprint"]
    if not d.exists():
        return []
    return sorted(d.rglob("blueprint.json"))


def discover_workflows() -> List[Path]:
    """Discover all workflow markdown files."""
    d = ARTIFACT_DIRS["workflow"]
    if not d.exists():
        return []
    return sorted(d.rglob("*.md"))


def discover_registry() -> List[Path]:
    """Discover the registry file."""
    p = ARTIFACT_DIRS["registry"] / "registry.json"
    return [p] if p.exists() else []


# ---------------------------------------------------------------------------
def validate_data(data: Dict[str, Any], schema: Dict[str, Any]) -> List[str]:
    """Validate a data dict against a JSON schema using Draft7Validator.

    Args:
        data: The data to validate.
        schema: The JSON Schema to validate against.

    Returns:
        List of human-readable error messages (empty if valid).
    """
    validator = Draft7Validator(schema)
    errors: List[str] = []
    for error in sorted(
        validator.iter_errors(data), key=lambda e: list(e.absolute_path)
    ):
        path = ".".join(str(p) for p in error.absolute_path) or "(root)"
        errors.append(f"{path}: {error.message}")
    return errors


def validate_frontmatter_file(
    path: Path,
    schema: Dict[str, Any],
    artifact_type: str,
) -> ValidationResult:
    """Validate a markdown file's YAML frontmatter against a schema.

    Args:
        path: Path to the markdown file.
        schema: JSON Schema dict.
        artifact_type: Label for reporting (e.g. ``"agent"``).

    Returns:
        ValidationResult instance.
    """
    rel = _rel(path)
    try:
        content = path.read_text(encoding="utf-8")
    except Exception as exc:
        return ValidationResult(rel, artifact_type, False, [f"Read error: {exc}"])

    data = extract_frontmatter(content)
    if data is None:
        return ValidationResult(
            rel, artifact_type, False, ["No YAML frontmatter found"]
        )

    errors = validate_data(data, schema)
    return ValidationResult(rel, artifact_type, len(errors) == 0, errors)


def validate_json_file(
    path: Path,
    schema: Dict[str, Any],
    artifact_type: str,
) -> ValidationResult:
    """Validate a JSON file against a schema.

    Args:
        path: Path to the JSON file.
        schema: JSON Schema dict.
        artifact_type: Label for reporting.

    Returns:
        ValidationResult instance.
    """
    rel = _rel(path)
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        return ValidationResult(rel, artifact_type, False, [f"Invalid JSON: {exc}"])
    except Exception as exc:
        return ValidationResult(rel, artifact_type, False, [f"Read error: {exc}"])

    errors = validate_data(data, schema)
    return ValidationResult(rel, artifact_type, len(errors) == 0, errors)


# ---------------------------------------------------------------------------
def validate_all(
    types: Optional[List[str]] = None,
    verbose: bool = False,
) -> ValidationReport:
    """Run schema validation across all (or selected) artifact types.

    Args:
        types: List of artifact type keys to validate (e.g. ``["agent", "skill"]``).
               If None, validates all types.
        verbose: Print per-file status.

    Returns:
        ValidationReport with results for every validated artifact.
    """
    schemas = load_schemas()
    report = ValidationReport()
    all_types = types or [
        "agent",
        "skill",
        "knowledge",
        "blueprint",
        "workflow",
        "registry",
        "catalog",
    ]

    # --- Agents ---
    if "agent" in all_types:
        schema = schemas.get("agent")
        if schema:
            files = discover_agents()
            if verbose:
                print(f"\nValidating {len(files)} agents against agent.schema.json ...")
            for path in files:
                result = validate_frontmatter_file(path, schema, "agent")
                report.results.append(result)
                if verbose:
                    _print_result(result)
        else:
            print("WARNING: agent.schema.json not found, skipping agents")

    # --- Skills ---
    if "skill" in all_types:
        schema = schemas.get("skill")
        if schema:
            files = discover_skills()
            if verbose:
                print(f"\nValidating {len(files)} skills against skill.schema.json ...")
            for path in files:
                result = validate_frontmatter_file(path, schema, "skill")
                report.results.append(result)
                if verbose:
                    _print_result(result)
        else:
            print("WARNING: skill.schema.json not found, skipping skills")

    # --- Knowledge ---
    if "knowledge" in all_types:
        schema = schemas.get("knowledge-file")
        if schema:
            files = discover_knowledge()
            if verbose:
                print(
                    f"\nValidating {len(files)} knowledge files against knowledge-file.schema.json ..."
                )
            for path in files:
                result = validate_json_file(path, schema, "knowledge")
                report.results.append(result)
                if verbose:
                    _print_result(result)
        else:
            print("WARNING: knowledge-file.schema.json not found, skipping knowledge")

    # --- Blueprints ---
    if "blueprint" in all_types:
        schema = schemas.get("blueprint")
        if schema:
            files = discover_blueprints()
            if verbose:
                print(
                    f"\nValidating {len(files)} blueprints against blueprint.schema.json ..."
                )
            for path in files:
                result = validate_json_file(path, schema, "blueprint")
                report.results.append(result)
                if verbose:
                    _print_result(result)
        else:
            print("WARNING: blueprint.schema.json not found, skipping blueprints")

    # --- Workflows ---
    if "workflow" in all_types:
        schema = schemas.get("workflow")
        if schema:
            files = discover_workflows()
            if verbose:
                print(
                    f"\nValidating {len(files)} workflows against workflow.schema.json ..."
                )
            for path in files:
                result = validate_frontmatter_file(path, schema, "workflow")
                report.results.append(result)
                if verbose:
                    _print_result(result)
        else:
            print("WARNING: workflow.schema.json not found, skipping workflows")

    # --- Registry ---
    if "registry" in all_types:
        schema = schemas.get("registry")
        if schema:
            files = discover_registry()
            if verbose:
                print("\nValidating registry against registry.schema.json ...")
            for path in files:
                result = validate_json_file(path, schema, "registry")
                report.results.append(result)
                if verbose:
                    _print_result(result)
        else:
            if verbose:
                print("NOTE: registry.schema.json not found, skipping registry")

    # --- Catalogs ---
    if "catalog" in all_types:
        schema = schemas.get("catalog")
        if schema:
            # Catalogs are in knowledge dir with -catalog.json suffix
            d = ARTIFACT_DIRS["knowledge"]
            if d.exists():
                catalog_names = [
                    "skill-catalog.json",
                    "pattern-catalog.json",
                    "template-catalog.json",
                    "blueprint-catalog.json",
                    "agent-catalog.json",
                    "workflow-catalog.json",
                    "registry-catalog.json",
                ]
                files = [d / name for name in catalog_names if (d / name).exists()]
                if verbose:
                    print(
                        f"\nValidating {len(files)} catalogs against catalog.schema.json ..."
                    )
                for path in files:
                    result = validate_json_file(path, schema, "catalog")
                    report.results.append(result)
                    if verbose:
                        _print_result(result)
        else:
            if verbose:
                print("WARNING: catalog.schema.json not found, skipping catalogs")

    return report


# ---------------------------------------------------------------------------
def _rel(path: Path) -> str:
    """Return path relative to project root as a string."""
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def _print_result(result: ValidationResult) -> None:
    """Print a single validation result."""
    if result.valid:
        print(f"  [OK]   {result.path}")
    else:
        print(f"  [FAIL] {result.path}")
        for err in result.errors[:3]:
            print(f"         - {err}")
        if len(result.errors) > 3:
            print(f"         ... and {len(result.errors) - 3} more")


# ---------------------------------------------------------------------------
def main() -> int:
    """CLI entry point.

    Returns:
        Exit code: 0 on success, 1 on validation failures.
    """
    parser = argparse.ArgumentParser(
        description="Validate Factory artifacts against canonical JSON schemas"
    )
    parser.add_argument(
        "--type",
        choices=[
            "agent",
            "skill",
            "knowledge",
            "blueprint",
            "workflow",
            "registry",
            "catalog",
            "all",
        ],
        default="all",
        help="Artifact type to validate (default: all)",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Verbose per-file output"
    )
    parser.add_argument(
        "--summary", action="store_true", help="Print summary only (no per-file detail)"
    )
    args = parser.parse_args()

    types = None if args.type == "all" else [args.type]
    verbose = args.verbose and not args.summary

    print("=" * 60)
    print("  Schema Validation Pipeline")
    print("=" * 60)

    report = validate_all(types=types, verbose=verbose)

    print("\n" + report.summary())
    print()

    if report.ok:
        print("RESULT: ALL SCHEMA VALIDATIONS PASSED")
    else:
        print("RESULT: SCHEMA VALIDATION ERRORS FOUND")
    print("=" * 60)

    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())
