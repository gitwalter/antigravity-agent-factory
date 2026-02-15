"""
Schema validation tests for blueprint files.

Tests validate that all blueprint.json files conform to expected structure.
"""

import json

import pytest
from jsonschema import Draft7Validator

from scripts.validation.schema_validator import load_schemas  # noqa: E402

# Load the canonical blueprint schema from schemas/blueprint.schema.json
_SCHEMAS = load_schemas()
BLUEPRINT_SCHEMA = _SCHEMAS.get("blueprint", {})


class TestBlueprintSchema:
    """Tests for blueprint schema validation."""

    @pytest.fixture
    def validator(self):
        """Create a JSON schema validator from the canonical schema."""
        assert BLUEPRINT_SCHEMA, "blueprint.schema.json could not be loaded"
        return Draft7Validator(BLUEPRINT_SCHEMA)

    def test_schema_is_valid(self, validator):
        """Test that the schema itself is valid."""
        # This will raise if schema is invalid
        Draft7Validator.check_schema(BLUEPRINT_SCHEMA)

    def test_all_blueprints_valid(self, blueprints_dir, validator):
        """Test that all blueprint.json files are valid against schema."""
        errors = []

        for blueprint_dir in blueprints_dir.iterdir():
            if blueprint_dir.is_dir():
                blueprint_file = blueprint_dir / "blueprint.json"
                if blueprint_file.exists():
                    with open(blueprint_file, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    validation_errors = list(validator.iter_errors(data))
                    for error in validation_errors:
                        errors.append(f"{blueprint_file}: {error.message}")

        if errors:
            pytest.fail("\n".join(errors))

    def test_python_fastapi_blueprint_valid(self, blueprints_dir, validator):
        """Test that python-fastapi blueprint is valid."""
        blueprint_file = blueprints_dir / "python-fastapi" / "blueprint.json"

        with open(blueprint_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        errors = list(validator.iter_errors(data))
        assert len(errors) == 0, f"Validation errors: {[e.message for e in errors]}"

    def test_blueprint_ids_match_directory_names(self, blueprints_dir):
        """Test that blueprintId matches the directory name."""
        for blueprint_dir in blueprints_dir.iterdir():
            if blueprint_dir.is_dir():
                blueprint_file = blueprint_dir / "blueprint.json"
                if blueprint_file.exists():
                    with open(blueprint_file, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    blueprint_id = data.get("metadata", {}).get("blueprintId")
                    assert (
                        blueprint_id == blueprint_dir.name
                    ), f"Blueprint ID '{blueprint_id}' should match directory name '{blueprint_dir.name}'"

    def test_blueprint_has_valid_language(self, blueprints_dir):
        """Test that blueprints have valid primary language."""
        valid_languages = {
            "python",
            "typescript",
            "javascript",
            "java",
            "csharp",
            "go",
            "rust",
            "abap",
            "kotlin",
            "groovy",
            "solidity",
        }

        for blueprint_dir in blueprints_dir.iterdir():
            if blueprint_dir.is_dir():
                blueprint_file = blueprint_dir / "blueprint.json"
                if blueprint_file.exists():
                    with open(blueprint_file, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    language = data.get("stack", {}).get("primaryLanguage", "").lower()
                    assert (
                        language in valid_languages
                    ), f"Blueprint {blueprint_dir.name} has invalid language: {language}"

    def test_blueprint_agent_references_format(self, blueprints_dir):
        """Test that agent references have correct format."""
        for blueprint_dir in blueprints_dir.iterdir():
            if blueprint_dir.is_dir():
                blueprint_file = blueprint_dir / "blueprint.json"
                if blueprint_file.exists():
                    with open(blueprint_file, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    for agent in data.get("agents", []):
                        assert (
                            "patternId" in agent
                        ), f"Agent in {blueprint_dir.name} missing patternId"

                        pattern_id = agent["patternId"]
                        # Pattern ID should be kebab-case
                        assert (
                            pattern_id == pattern_id.lower()
                        ), f"Pattern ID '{pattern_id}' should be lowercase"
