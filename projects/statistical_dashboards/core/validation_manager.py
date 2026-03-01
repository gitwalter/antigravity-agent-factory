import json
import os
import jsonschema
from typing import Dict, Any, Tuple, List


class ValidationManager:
    """Manages JSON Schema validation for warehouse data ingestion."""

    def __init__(
        self, schemas_dir: str = "projects/statistical_dashboards/schemas/warehouse"
    ):
        self.schemas_dir = schemas_dir
        self.schemas = self._load_schemas()

    def _load_schemas(self) -> Dict[str, Any]:
        schemas = {}
        if not os.path.exists(self.schemas_dir):
            return schemas

        for filename in os.listdir(self.schemas_dir):
            if filename.endswith(".schema.json"):
                name = filename.split(".")[0]
                filepath = os.path.join(self.schemas_dir, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        schemas[name] = json.load(f)
                except Exception as e:
                    print(f"Error loading schema {filename}: {e}")
        return schemas

    def validate_payload(
        self, schema_name: str, payload_list: List[Dict[str, Any]]
    ) -> Tuple[bool, List[str]]:
        """Validates a list of dictionaries against a loaded JSON schema.
        Returns a tuple of (is_valid, list_of_errors).
        """
        if schema_name not in self.schemas:
            return False, [f"Schema '{schema_name}' not found."]

        schema = self.schemas[schema_name]
        errors = []

        for idx, row in enumerate(payload_list):
            try:
                jsonschema.validate(instance=row, schema=schema)
            except jsonschema.exceptions.ValidationError as e:
                errors.append(
                    f"Row {idx+1}: {e.message} at '{'/'.join(map(str, e.path))}'"
                )

        is_valid = len(errors) == 0
        return is_valid, errors

    def get_schema_details(self, schema_name: str) -> Dict[str, Any]:
        """Returns the schema dictionary for UI documentation purposes."""
        return self.schemas.get(schema_name, {})
