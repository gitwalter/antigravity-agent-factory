"""
Schema validation tests for pattern files.

Tests validate that agent and skill patterns conform to expected structure.
"""

import json
import sys
from pathlib import Path

import pytest
from jsonschema import Draft7Validator

from scripts.validation.schema_validator import load_schemas  # noqa: E402

# Load canonical schemas
_SCHEMAS = load_schemas()
AGENT_SCHEMA = _SCHEMAS.get("agent", {})
SKILL_SCHEMA = _SCHEMAS.get("skill", {})

# Define internal pattern metadata schemas (these wrap the canonical frontmatter)
AGENT_PATTERN_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["metadata", "frontmatter", "sections"],
    "properties": {
        "metadata": {
            "type": "object",
            "required": ["patternId", "patternName", "category"],
            "properties": {
                "patternId": {"type": "string", "pattern": "^[a-z][a-z0-9-]*$"},
                "patternName": {"type": "string"},
                "category": {"type": "string"},
                "stackAgnostic": {"type": "boolean"},
                "description": {"type": "string"}
            }
        },
        "frontmatter": AGENT_SCHEMA,
        "sections": {
            "type": "object",
            "required": ["purpose"],
            "properties": {
                "title": {"type": "string"},
                "purpose": {"type": "string"},
                "whenActivated": {"type": "array", "items": {"type": "string"}},
                "workflow": {"type": "array"},
                "skillsUsed": {"type": "array"},
                "knowledgeFiles": {"type": "array"},
                "outputFormat": {"type": "string"},
                "importantRules": {"type": "array", "items": {"type": "string"}}
            }
        },
        "variables": {"type": "array"}
    }
}

SKILL_PATTERN_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["metadata", "frontmatter", "sections"],
    "properties": {
        "metadata": {
            "type": "object",
            "required": ["patternId", "patternName", "category"],
            "properties": {
                "patternId": {"type": "string", "pattern": "^[a-z][a-z0-9-]*$"},
                "patternName": {"type": "string"},
                "category": {"type": "string"},
                "stackAgnostic": {"type": "boolean"},
                "description": {"type": "string"},
                "composable": {"type": "boolean"}
            }
        },
        "frontmatter": SKILL_SCHEMA,
        "sections": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "introduction": {"type": "string"},
                "whenToUse": {"type": "array", "items": {"type": "string"}},
                "process": {"type": "array"},
                "fallbackProcedures": {"type": "array"},
                "importantRules": {"type": "array", "items": {"type": "string"}},
                "references": {"type": "array"}
            }
        },
        "variables": {"type": "array"}
    }
}


def is_schema_file(filepath: Path) -> bool:
    """Check if a JSON file is a schema definition.
    
    Args:
        filepath: Path to the JSON file.
        
    Returns:
        True if the file is a schema definition.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return "$schema" in data or filepath.stem.endswith("-pattern")


class TestAgentPatternSchema:
    """Tests for agent pattern schema validation."""
    
    @pytest.fixture
    def validator(self):
        """Create a JSON schema validator."""
        return Draft7Validator(AGENT_PATTERN_SCHEMA)
    
    def test_schema_is_valid(self, validator):
        """Test that the schema itself is valid."""
        Draft7Validator.check_schema(AGENT_PATTERN_SCHEMA)
    
    def test_all_agent_patterns_valid(self, patterns_dir, validator):
        """Test that all agent patterns are valid against schema."""
        agents_dir = patterns_dir / "agents"
        errors = []
        
        for pattern_file in agents_dir.glob("*.json"):
            # Skip schema files
            if is_schema_file(pattern_file):
                continue
                
            with open(pattern_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            validation_errors = list(validator.iter_errors(data))
            for error in validation_errors:
                path = ".".join(str(p) for p in error.path)
                errors.append(f"{pattern_file.name} at '{path}': {error.message}")
        
        if errors:
            pytest.fail("\n".join(errors))
    
    def test_code_reviewer_pattern_valid(self, patterns_dir, validator):
        """Test that code-reviewer pattern is valid."""
        pattern_file = patterns_dir / "agents" / "code-reviewer.json"
        
        with open(pattern_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        errors = list(validator.iter_errors(data))
        assert len(errors) == 0, f"Validation errors: {[e.message for e in errors]}"
    
    def test_agent_pattern_ids_are_kebab_case(self, patterns_dir):
        """Test that agent pattern IDs use kebab-case."""
        agents_dir = patterns_dir / "agents"
        
        for pattern_file in agents_dir.glob("*.json"):
            if is_schema_file(pattern_file):
                continue
                
            with open(pattern_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            pattern_id = data.get("metadata", {}).get("patternId", "")
            assert pattern_id == pattern_id.lower(), \
                f"Pattern ID '{pattern_id}' should be lowercase"
            assert " " not in pattern_id, \
                f"Pattern ID '{pattern_id}' should not contain spaces"
    
    def test_agent_frontmatter_type_is_agent(self, patterns_dir):
        """Test that agent frontmatter type is 'agent'."""
        agents_dir = patterns_dir / "agents"
        
        for pattern_file in agents_dir.glob("*.json"):
            if is_schema_file(pattern_file):
                continue
                
            with open(pattern_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            frontmatter_type = data.get("frontmatter", {}).get("type")
            assert frontmatter_type == "agent", \
                f"Agent {pattern_file.name} should have type 'agent'"


class TestSkillPatternSchema:
    """Tests for skill pattern schema validation."""
    
    @pytest.fixture
    def validator(self):
        """Create a JSON schema validator."""
        return Draft7Validator(SKILL_PATTERN_SCHEMA)
    
    def test_schema_is_valid(self, validator):
        """Test that the schema itself is valid."""
        Draft7Validator.check_schema(SKILL_PATTERN_SCHEMA)
    
    def test_all_skill_patterns_valid(self, patterns_dir, validator):
        """Test that all skill patterns are valid against schema."""
        skills_dir = patterns_dir / "skills"
        errors = []
        
        for pattern_file in skills_dir.glob("*.json"):
            # Skip schema files
            if is_schema_file(pattern_file):
                continue
                
            with open(pattern_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            validation_errors = list(validator.iter_errors(data))
            for error in validation_errors:
                path = ".".join(str(p) for p in error.path)
                errors.append(f"{pattern_file.name} at '{path}': {error.message}")
        
        if errors:
            pytest.fail("\n".join(errors))
    
    def test_bugfix_workflow_pattern_valid(self, patterns_dir, validator):
        """Test that bugfix-workflow pattern is valid."""
        pattern_file = patterns_dir / "skills" / "bugfix-workflow.json"
        
        with open(pattern_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        errors = list(validator.iter_errors(data))
        assert len(errors) == 0, f"Validation errors: {[e.message for e in errors]}"
    
    def test_skill_pattern_ids_are_kebab_case(self, patterns_dir):
        """Test that skill pattern IDs use kebab-case."""
        skills_dir = patterns_dir / "skills"
        
        for pattern_file in skills_dir.glob("*.json"):
            if is_schema_file(pattern_file):
                continue
                
            with open(pattern_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            pattern_id = data.get("metadata", {}).get("patternId", "")
            assert pattern_id == pattern_id.lower(), \
                f"Pattern ID '{pattern_id}' should be lowercase"
    
    def test_skill_frontmatter_type_is_skill(self, patterns_dir):
        """Test that skill frontmatter type is 'skill'."""
        skills_dir = patterns_dir / "skills"
        
        for pattern_file in skills_dir.glob("*.json"):
            if is_schema_file(pattern_file):
                continue
                
            with open(pattern_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            frontmatter_type = data.get("frontmatter", {}).get("type")
            assert frontmatter_type == "skill", \
                f"Skill {pattern_file.name} should have type 'skill'"


class TestPatternConsistency:
    """Tests for pattern file consistency."""
    
    def test_pattern_id_matches_filename(self, patterns_dir):
        """Test that patternId matches the filename."""
        for pattern_type in ["agents", "skills"]:
            type_dir = patterns_dir / pattern_type
            
            for pattern_file in type_dir.glob("*.json"):
                if is_schema_file(pattern_file):
                    continue
                    
                with open(pattern_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                pattern_id = data.get("metadata", {}).get("patternId")
                expected_filename = f"{pattern_id}.json"
                
                assert pattern_file.name == expected_filename, \
                    f"Pattern ID '{pattern_id}' should match filename '{pattern_file.name}'"
    
    def test_frontmatter_name_matches_pattern_id(self, patterns_dir):
        """Test that frontmatter name matches pattern ID."""
        for pattern_type in ["agents", "skills"]:
            type_dir = patterns_dir / pattern_type
            
            for pattern_file in type_dir.glob("*.json"):
                if is_schema_file(pattern_file):
                    continue
                    
                with open(pattern_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                pattern_id = data.get("metadata", {}).get("patternId")
                frontmatter_name = data.get("frontmatter", {}).get("name")
                
                assert pattern_id == frontmatter_name, \
                    f"Pattern ID '{pattern_id}' should match frontmatter name '{frontmatter_name}'"
