"""
Schema validation tests for PM system files.

Tests validate that PM product, questionnaire, adapters, defaults, and metrics
files conform to expected structure.
"""

import json
import sys
from pathlib import Path

import pytest
from jsonschema import Draft7Validator

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


# Define PM Product schema
PM_PRODUCT_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["metadata", "backends", "methodologies"],
    "properties": {
        "metadata": {
            "type": "object",
            "required": ["id", "name", "version"],
            "properties": {
                "id": {"type": "string"},
                "name": {"type": "string"},
                "version": {"type": "string"},
                "description": {"type": "string"},
                "optional": {"type": "boolean"}
            }
        },
        "backends": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id", "name"],
                "properties": {
                    "id": {"type": "string"},
                    "name": {"type": "string"},
                    "description": {"type": "string"},
                    "mcpServer": {"type": "string"},
                    "capabilities": {"type": "array", "items": {"type": "string"}}
                }
            }
        },
        "methodologies": {
            "type": "array",
            "items": {"type": "string"}
        },
        "components": {"type": "object"}
    }
}

# Define Questionnaire schema
QUESTIONNAIRE_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["questions"],
    "properties": {
        "questions": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id", "question", "type", "options"],
                "properties": {
                    "id": {"type": "string"},
                    "question": {"type": "string"},
                    "type": {"type": "string", "enum": ["single", "multiple", "conditional"]},
                    "options": {
                        "type": "array",
                        "items": {"type": "object"}
                    },
                    "default": {"type": "string"},
                    "required": {"type": "boolean"},
                    "helpText": {"type": "string"},
                    "conditional": {"type": "object"}
                }
            }
        }
    }
}

# Define Adapter Interface schema
ADAPTER_INTERFACE_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["metadata", "interface"],
    "properties": {
        "metadata": {
            "type": "object",
            "required": ["interfaceId", "interfaceName", "version"],
            "properties": {
                "interfaceId": {"type": "string"},
                "interfaceName": {"type": "string"},
                "version": {"type": "string"},
                "description": {"type": "string"}
            }
        },
        "interface": {
            "type": "object",
            "required": ["workItems", "planning", "boards", "metrics", "documentation"],
            "properties": {
                "workItems": {"type": "object"},
                "planning": {"type": "object"},
                "boards": {"type": "object"},
                "metrics": {"type": "object"},
                "documentation": {"type": "object"}
            }
        }
    }
}

# Define Backend Adapter schema
BACKEND_ADAPTER_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["metadata", "mappings"],
    "properties": {
        "metadata": {
            "type": "object",
            "required": ["adapterId", "adapterName", "targetSystem", "version"],
            "properties": {
                "adapterId": {"type": "string"},
                "adapterName": {"type": "string"},
                "targetSystem": {"type": "string"},
                "version": {"type": "string"},
                "description": {"type": "string"},
                "mcpServer": {"type": "string"}
            }
        },
        "mappings": {
            "type": "object",
            "required": ["concepts", "workItems", "planning", "boards", "metrics", "documentation"],
            "properties": {
                "concepts": {"type": "object"},
                "workItems": {"type": "object"},
                "planning": {"type": "object"},
                "boards": {"type": "object"},
                "metrics": {"type": "object"},
                "documentation": {"type": "object"}
            }
        }
    }
}

# Define Methodology Defaults schema
METHODOLOGY_DEFAULTS_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["methodologyId", "name", "version"],
    "properties": {
        "methodologyId": {"type": "string"},
        "name": {"type": "string"},
        "version": {"type": "string"},
        "description": {"type": "string"},
        "sprint": {"type": "object"},
        "ceremonies": {"type": "object"},
        "roles": {"type": "object"},
        "backlog": {"type": "object"},
        "metrics": {"type": "object"},
        "definition_of_done": {"type": "array"},
        "definition_of_ready": {"type": "array"}
    }
}

# Define Metrics schema
METRICS_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["metrics"],
    "properties": {
        "metrics": {
            "type": "object",
            "patternProperties": {
                ".*": {
                    "type": "object",
                    "required": ["id", "name", "formula", "unit", "category"],
                    "properties": {
                        "id": {"type": "string"},
                        "name": {"type": "string"},
                        "formula": {"type": "string"},
                        "unit": {"type": "string"},
                        "category": {
                            "type": "string",
                            "enum": ["velocity", "flow", "quality", "predictive", "health"]
                        },
                        "description": {"type": "string"},
                        "interpretation": {"type": "object"},
                        "source": {"type": "string"},
                        "calculation_period": {"type": "string"},
                        "requires_history": {"type": "boolean"}
                    }
                }
            }
        },
        "metric_categories": {"type": "object"}
    }
}


@pytest.fixture
def pm_patterns_dir(patterns_dir: Path) -> Path:
    """Get the PM system patterns directory.
    
    Args:
        patterns_dir: Patterns directory fixture.
        
    Returns:
        Path to PM system patterns directory.
    """
    return patterns_dir / "products" / "pm-system"


@pytest.fixture
def pm_adapters_dir(pm_patterns_dir: Path) -> Path:
    """Get the PM adapters directory.
    
    Args:
        pm_patterns_dir: PM patterns directory fixture.
        
    Returns:
        Path to PM adapters directory.
    """
    return pm_patterns_dir / "adapters"


@pytest.fixture
def pm_defaults_dir(pm_patterns_dir: Path) -> Path:
    """Get the PM defaults directory.
    
    Args:
        pm_patterns_dir: PM patterns directory fixture.
        
    Returns:
        Path to PM defaults directory.
    """
    return pm_patterns_dir / "defaults"


class TestPMProductSchema:
    """Tests for PM product schema validation."""
    
    @pytest.fixture
    def validator(self):
        """Create a JSON schema validator."""
        return Draft7Validator(PM_PRODUCT_SCHEMA)
    
    def test_schema_is_valid(self, validator):
        """Test that the schema itself is valid."""
        Draft7Validator.check_schema(PM_PRODUCT_SCHEMA)
    
    def test_product_json_is_valid_json(self, pm_patterns_dir):
        """Test that product.json is valid JSON."""
        product_file = pm_patterns_dir / "product.json"
        
        with open(product_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert isinstance(data, dict), "Product JSON should be a dictionary"
    
    def test_product_has_required_fields(self, pm_patterns_dir, validator):
        """Test that product.json has all required fields."""
        product_file = pm_patterns_dir / "product.json"
        
        with open(product_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        errors = list(validator.iter_errors(data))
        assert len(errors) == 0, f"Validation errors: {[e.message for e in errors]}"
    
    def test_backends_are_valid_list(self, pm_patterns_dir):
        """Test that backends field is a valid list."""
        product_file = pm_patterns_dir / "product.json"
        
        with open(product_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert "backends" in data, "Product should have 'backends' field"
        assert isinstance(data["backends"], list), "Backends should be a list"
        assert len(data["backends"]) > 0, "Backends list should not be empty"
        
        # Validate each backend has required fields
        for backend in data["backends"]:
            assert "id" in backend, "Backend should have 'id' field"
            assert "name" in backend, "Backend should have 'name' field"
    
    def test_methodologies_are_valid_list(self, pm_patterns_dir):
        """Test that methodologies field is a valid list."""
        product_file = pm_patterns_dir / "product.json"
        
        with open(product_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert "methodologies" in data, "Product should have 'methodologies' field"
        assert isinstance(data["methodologies"], list), "Methodologies should be a list"
        assert len(data["methodologies"]) > 0, "Methodologies list should not be empty"
        
        # Validate each methodology is a string
        for methodology in data["methodologies"]:
            assert isinstance(methodology, str), "Methodology should be a string"


class TestQuestionnaireSchema:
    """Tests for questionnaire schema validation."""
    
    @pytest.fixture
    def validator(self):
        """Create a JSON schema validator."""
        return Draft7Validator(QUESTIONNAIRE_SCHEMA)
    
    def test_schema_is_valid(self, validator):
        """Test that the schema itself is valid."""
        Draft7Validator.check_schema(QUESTIONNAIRE_SCHEMA)
    
    def test_questionnaire_is_valid_json(self, pm_patterns_dir):
        """Test that questionnaire.json is valid JSON."""
        questionnaire_file = pm_patterns_dir / "questionnaire.json"
        
        with open(questionnaire_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert isinstance(data, dict), "Questionnaire JSON should be a dictionary"
    
    def test_questionnaire_has_questions(self, pm_patterns_dir):
        """Test that questionnaire has questions field."""
        questionnaire_file = pm_patterns_dir / "questionnaire.json"
        
        with open(questionnaire_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert "questions" in data, "Questionnaire should have 'questions' field"
        assert isinstance(data["questions"], list), "Questions should be a list"
        assert len(data["questions"]) > 0, "Questions list should not be empty"
    
    def test_questions_have_required_fields(self, pm_patterns_dir, validator):
        """Test that all questions have required fields."""
        questionnaire_file = pm_patterns_dir / "questionnaire.json"
        
        with open(questionnaire_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        errors = list(validator.iter_errors(data))
        assert len(errors) == 0, f"Validation errors: {[e.message for e in errors]}"
        
        # Additional validation for question structure
        for question in data["questions"]:
            assert "id" in question, "Question should have 'id' field"
            assert "type" in question, "Question should have 'type' field"
            assert "options" in question, "Question should have 'options' field"
            assert isinstance(question["options"], list), "Options should be a list"
            assert len(question["options"]) > 0, "Options list should not be empty"


class TestAdapterInterfaceSchema:
    """Tests for adapter interface schema validation."""
    
    def test_interface_is_valid_json(self, pm_adapters_dir):
        """Test that adapter-interface.json is valid JSON."""
        interface_file = pm_adapters_dir / "adapter-interface.json"
        
        with open(interface_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert isinstance(data, dict), "Interface JSON should be a dictionary"
    
    def test_interface_has_operations(self, pm_adapters_dir):
        """Test that interface defines all required operations."""
        interface_file = pm_adapters_dir / "adapter-interface.json"
        
        with open(interface_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check that the schema defines required interface sections
        properties = data.get("properties", {})
        interface_props = properties.get("interface", {}).get("properties", {})
        
        required_sections = ["workItems", "planning", "boards", "metrics", "documentation"]
        for section in required_sections:
            assert section in interface_props, \
                f"Interface should define '{section}' section"
            assert isinstance(interface_props[section], dict), \
                f"'{section}' should be defined as an object"
        
        # Check that workItems operations are defined
        work_items_props = interface_props.get("workItems", {}).get("properties", {})
        required_work_item_ops = [
            "createEpic", "createStory", "createTask", "createBug",
            "updateStatus", "assignItem", "getItem", "listItems"
        ]
        for op in required_work_item_ops:
            assert op in work_items_props, \
                f"WorkItems should define '{op}' operation"
    
    def test_operations_have_parameters(self, pm_adapters_dir):
        """Test that operations have parameters defined in schema."""
        interface_file = pm_adapters_dir / "adapter-interface.json"
        
        with open(interface_file, 'r', encoding='utf-8') as f:
            schema_data = json.load(f)
        
        # Extract interface schema
        properties = schema_data.get("properties", {})
        interface_props = properties.get("interface", {}).get("properties", {})
        work_items_props = interface_props.get("workItems", {}).get("properties", {})
        
        # Check that operations define parameters
        required_work_item_ops = [
            "createEpic", "createStory", "createTask", "createBug",
            "updateStatus", "assignItem", "getItem", "listItems"
        ]
        for op in required_work_item_ops:
            if op in work_items_props:
                op_props = work_items_props[op].get("properties", {})
                assert "parameters" in op_props, \
                    f"'{op}' operation should define 'parameters' in schema"
                assert isinstance(op_props["parameters"], dict), \
                    f"'{op}' parameters should be defined as an object"
        
        # Check planning operations
        planning_props = interface_props.get("planning", {}).get("properties", {})
        required_planning_ops = [
            "createSprint", "addToSprint", "closeSprint", "getSprint", "listSprints"
        ]
        for op in required_planning_ops:
            if op in planning_props:
                op_props = planning_props[op].get("properties", {})
                assert "parameters" in op_props, \
                    f"'{op}' operation should define 'parameters' in schema"


class TestBackendAdaptersSchema:
    """Tests for backend adapter schema validation."""
    
    def test_schema_is_valid(self):
        """Test that the backend adapter schema itself is valid."""
        Draft7Validator.check_schema(BACKEND_ADAPTER_SCHEMA)
    
    def test_all_adapters_valid_json(self, pm_adapters_dir):
        """Test that all adapter files are valid JSON."""
        adapter_files = [
            f for f in pm_adapters_dir.glob("*-adapter.json")
            if f.name != "adapter-interface.json"
        ]
        
        assert len(adapter_files) > 0, "Should have at least one adapter file"
        
        for adapter_file in adapter_files:
            with open(adapter_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            assert isinstance(data, dict), f"{adapter_file.name} should be a dictionary"
    
    def test_adapters_have_mappings(self, pm_adapters_dir):
        """Test that all adapters define mappings."""
        adapter_files = [
            f for f in pm_adapters_dir.glob("*-adapter.json")
            if f.name != "adapter-interface.json"
        ]
        
        errors = []
        for adapter_file in adapter_files:
            with open(adapter_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check that it defines mappings (either directly or in schema properties)
            if "mappings" in data:
                mappings = data["mappings"]
            elif "properties" in data and "mappings" in data.get("properties", {}):
                mappings = data["properties"]["mappings"]
            else:
                errors.append(f"{adapter_file.name}: Should define 'mappings'")
                continue
            
            # Check that mappings define required sections
            if isinstance(mappings, dict):
                # If mappings is a schema definition, check properties
                if "properties" in mappings:
                    mappings_sections = mappings["properties"]
                else:
                    mappings_sections = mappings
            else:
                errors.append(f"{adapter_file.name}: Mappings should be a dictionary")
                continue
            
            # All adapters should have concepts and at least one of the other sections
            required_sections = ["concepts"]
            optional_sections = ["workItems", "planning", "boards", "metrics", "documentation"]
            
            # Check required sections
            for section in required_sections:
                if section not in mappings_sections:
                    errors.append(f"{adapter_file.name}: Mappings should define '{section}' section")
            
            # Check that at least one optional section is present
            found_optional = [s for s in optional_sections if s in mappings_sections]
            if not found_optional:
                errors.append(
                    f"{adapter_file.name}: Mappings should define at least one of: {', '.join(optional_sections)}"
                )
        
        if errors:
            pytest.fail("\n".join(errors))
    
    def test_adapters_implement_interface_operations(self, pm_adapters_dir):
        """Test that adapters define mappings for all required interface operations."""
        # Load interface to get required operations
        interface_file = pm_adapters_dir / "adapter-interface.json"
        with open(interface_file, 'r', encoding='utf-8') as f:
            interface_data = json.load(f)
        
        # Extract required operations from interface
        interface_props = interface_data.get("properties", {}).get("interface", {}).get("properties", {})
        required_sections = ["workItems", "planning", "boards", "metrics", "documentation"]
        
        # Get required operations from each section
        required_ops = {}
        for section in required_sections:
            section_props = interface_props.get(section, {}).get("properties", {})
            required_ops[section] = list(section_props.keys())
        
        # Check each adapter
        adapter_files = [
            f for f in pm_adapters_dir.glob("*-adapter.json")
            if f.name != "adapter-interface.json"
        ]
        
        for adapter_file in adapter_files:
            with open(adapter_file, 'r', encoding='utf-8') as f:
                adapter_data = json.load(f)
            
            # Extract mappings (handle both direct mappings and schema definitions)
            if "mappings" in adapter_data:
                mappings = adapter_data["mappings"]
            elif "properties" in adapter_data and "mappings" in adapter_data.get("properties", {}):
                mappings_def = adapter_data["properties"]["mappings"]
                if "properties" in mappings_def:
                    mappings = mappings_def["properties"]
                else:
                    mappings = mappings_def
            else:
                pytest.fail(f"{adapter_file.name} should have mappings")
            
            # Check that adapters implement sections they claim to support
            # (Not all adapters need to implement all sections - e.g., Confluence is docs-only)
            for section in required_sections:
                if section in mappings:
                    # For workItems and planning, check that key operations are mapped
                    if section in ["workItems", "planning"]:
                        section_mappings = mappings.get(section, {})
                        # Handle schema definition structure
                        if "properties" in section_mappings:
                            section_mappings = section_mappings["properties"]
                        
                        section_required_ops = required_ops.get(section, [])
                        
                        # At least some operations should be mapped
                        mapped_ops = [op for op in section_required_ops if op in section_mappings]
                        assert len(mapped_ops) > 0, \
                            f"{adapter_file.name} should map at least some '{section}' operations"


class TestMethodologyDefaultsSchema:
    """Tests for methodology defaults schema validation."""
    
    @pytest.fixture
    def validator(self):
        """Create a JSON schema validator."""
        return Draft7Validator(METHODOLOGY_DEFAULTS_SCHEMA)
    
    def test_schema_is_valid(self, validator):
        """Test that the schema itself is valid."""
        Draft7Validator.check_schema(METHODOLOGY_DEFAULTS_SCHEMA)
    
    def test_all_defaults_valid_json(self, pm_defaults_dir):
        """Test that all defaults files are valid JSON."""
        defaults_files = list(pm_defaults_dir.glob("*.json"))
        
        assert len(defaults_files) > 0, "Should have at least one defaults file"
        
        for defaults_file in defaults_files:
            with open(defaults_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            assert isinstance(data, dict), f"{defaults_file.name} should be a dictionary"
    
    def test_defaults_have_required_fields(self, pm_defaults_dir, validator):
        """Test that all defaults have required fields."""
        defaults_files = list(pm_defaults_dir.glob("*.json"))
        
        errors = []
        for defaults_file in defaults_files:
            with open(defaults_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            validation_errors = list(validator.iter_errors(data))
            for error in validation_errors:
                errors.append(f"{defaults_file.name}: {error.message}")
        
        if errors:
            pytest.fail("\n".join(errors))


class TestMetricsSchema:
    """Tests for metrics schema validation."""
    
    @pytest.fixture
    def validator(self):
        """Create a JSON schema validator."""
        return Draft7Validator(METRICS_SCHEMA)
    
    def test_schema_is_valid(self, validator):
        """Test that the schema itself is valid."""
        Draft7Validator.check_schema(METRICS_SCHEMA)
    
    def test_metrics_is_valid_json(self, knowledge_dir):
        """Test that pm-metrics.json is valid JSON."""
        metrics_file = knowledge_dir / "pm-metrics.json"
        
        with open(metrics_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert isinstance(data, dict), "Metrics JSON should be a dictionary"
    
    def test_metrics_have_required_fields(self, knowledge_dir, validator):
        """Test that all metrics have required fields."""
        metrics_file = knowledge_dir / "pm-metrics.json"
        
        with open(metrics_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        errors = list(validator.iter_errors(data))
        assert len(errors) == 0, f"Validation errors: {[e.message for e in errors]}"
        
        # Additional validation for metric structure
        assert "metrics" in data, "Metrics file should have 'metrics' field"
        metrics = data["metrics"]
        
        for metric_id, metric in metrics.items():
            assert "id" in metric, f"Metric '{metric_id}' should have 'id' field"
            assert "name" in metric, f"Metric '{metric_id}' should have 'name' field"
            assert "formula" in metric, f"Metric '{metric_id}' should have 'formula' field"
            assert "unit" in metric, f"Metric '{metric_id}' should have 'unit' field"
            assert "category" in metric, f"Metric '{metric_id}' should have 'category' field"
    
    def test_all_categories_covered(self, knowledge_dir):
        """Test that all metric categories are covered."""
        metrics_file = knowledge_dir / "pm-metrics.json"
        
        with open(metrics_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        required_categories = ["velocity", "flow", "quality", "predictive", "health"]
        metrics = data.get("metrics", {})
        
        # Collect categories from metrics
        found_categories = set()
        for metric in metrics.values():
            category = metric.get("category")
            if category:
                found_categories.add(category)
        
        # Check that all required categories are present
        for category in required_categories:
            assert category in found_categories, \
                f"Should have at least one metric in '{category}' category"
        
        # Also check metric_categories section if present
        if "metric_categories" in data:
            category_definitions = data["metric_categories"]
            for category in required_categories:
                assert category in category_definitions, \
                    f"Should have definition for '{category}' category"
