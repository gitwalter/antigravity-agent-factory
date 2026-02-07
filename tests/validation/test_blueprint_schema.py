"""
Schema validation tests for blueprint files.

Tests validate that all blueprint.json files conform to expected structure.
"""

import json
import sys
from pathlib import Path

import pytest
from jsonschema import Draft7Validator

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


# Define blueprint schema
BLUEPRINT_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["metadata", "stack"],
    "properties": {
        "metadata": {
            "type": "object",
            "required": ["blueprintId", "blueprintName", "description"],
            "properties": {
                "blueprintId": {"type": "string", "pattern": "^[a-z][a-z0-9-]*$"},
                "blueprintName": {"type": "string"},
                "description": {"type": "string"},
                "version": {"type": "string"},
                "author": {"type": "string"},
                "tags": {"type": "array", "items": {"type": "string"}}
            }
        },
        "stack": {
            "type": "object",
            "required": ["primaryLanguage"],
            "properties": {
                "primaryLanguage": {"type": "string"},
                "frameworks": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["name"],
                        "properties": {
                            "name": {"type": "string"},
                            "version": {"type": "string"},
                            "purpose": {"type": "string"}
                        }
                    }
                },
                "databases": {"type": "array"},
                "tools": {"type": "array"},
                "styleGuides": {"type": "array"}
            }
        },
        "agents": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["patternId"],
                "properties": {
                    "patternId": {"type": "string"},
                    "required": {"type": "boolean"},
                    "customizations": {"type": "object"}
                }
            }
        },
        "skills": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["patternId"],
                "properties": {
                    "patternId": {"type": "string"},
                    "required": {"type": "boolean"}
                }
            }
        },
        "knowledge": {"type": "array"},
        "templates": {"type": "object"},
        "workflows": {"type": "array"},
        "mcpServers": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "url": {"type": "string"},
                    "purpose": {"type": "string"},
                    "required": {"type": "boolean"}
                }
            }
        },
        "projectStructure": {"type": "object"},
        "agentrules": {"type": "object"}
    }
}


class TestBlueprintSchema:
    """Tests for blueprint schema validation."""
    
    @pytest.fixture
    def validator(self):
        """Create a JSON schema validator."""
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
                    with open(blueprint_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    validation_errors = list(validator.iter_errors(data))
                    for error in validation_errors:
                        errors.append(f"{blueprint_file}: {error.message}")
        
        if errors:
            pytest.fail("\n".join(errors))
    
    def test_python_fastapi_blueprint_valid(self, blueprints_dir, validator):
        """Test that python-fastapi blueprint is valid."""
        blueprint_file = blueprints_dir / "python-fastapi" / "blueprint.json"
        
        with open(blueprint_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        errors = list(validator.iter_errors(data))
        assert len(errors) == 0, f"Validation errors: {[e.message for e in errors]}"
    
    def test_blueprint_ids_match_directory_names(self, blueprints_dir):
        """Test that blueprintId matches the directory name."""
        for blueprint_dir in blueprints_dir.iterdir():
            if blueprint_dir.is_dir():
                blueprint_file = blueprint_dir / "blueprint.json"
                if blueprint_file.exists():
                    with open(blueprint_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    blueprint_id = data.get("metadata", {}).get("blueprintId")
                    assert blueprint_id == blueprint_dir.name, \
                        f"Blueprint ID '{blueprint_id}' should match directory name '{blueprint_dir.name}'"
    
    def test_blueprint_has_valid_language(self, blueprints_dir):
        """Test that blueprints have valid primary language."""
        valid_languages = {"python", "typescript", "javascript", "java", "csharp", "go", "rust", "abap", "kotlin", "groovy", "solidity"}
        
        for blueprint_dir in blueprints_dir.iterdir():
            if blueprint_dir.is_dir():
                blueprint_file = blueprint_dir / "blueprint.json"
                if blueprint_file.exists():
                    with open(blueprint_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    language = data.get("stack", {}).get("primaryLanguage", "").lower()
                    assert language in valid_languages, \
                        f"Blueprint {blueprint_dir.name} has invalid language: {language}"
    
    def test_blueprint_agent_references_format(self, blueprints_dir):
        """Test that agent references have correct format."""
        for blueprint_dir in blueprints_dir.iterdir():
            if blueprint_dir.is_dir():
                blueprint_file = blueprint_dir / "blueprint.json"
                if blueprint_file.exists():
                    with open(blueprint_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    for agent in data.get("agents", []):
                        assert "patternId" in agent, \
                            f"Agent in {blueprint_dir.name} missing patternId"
                        
                        pattern_id = agent["patternId"]
                        # Pattern ID should be kebab-case
                        assert pattern_id == pattern_id.lower(), \
                            f"Pattern ID '{pattern_id}' should be lowercase"
