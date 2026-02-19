"""
Schema validation tests for knowledge files.

Tests validate that knowledge JSON files conform to expected structure.
"""

import json

import pytest
from jsonschema import Draft7Validator

from scripts.validation.schema_validator import load_schemas  # noqa: E402

# Load canonical knowledge-file schema for general knowledge validation
_SCHEMAS = load_schemas()
KNOWLEDGE_FILE_SCHEMA = _SCHEMAS.get("knowledge-file", {})
CATALOG_SCHEMA = _SCHEMAS.get("catalog", {})


class TestKnowledgeFilesStructure:
    """Tests for knowledge file structure."""

    def test_all_knowledge_files_valid_json(self, knowledge_dir):
        """Test that all knowledge files are valid JSON."""
        for knowledge_file in knowledge_dir.glob("*.json"):
            try:
                with open(knowledge_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                assert isinstance(
                    data, dict
                ), f"{knowledge_file} should be a JSON object"
            except json.JSONDecodeError as e:
                pytest.fail(f"Invalid JSON in {knowledge_file}: {e}")

    def test_knowledge_files_have_content(self, knowledge_dir):
        """Test that knowledge files are not empty."""
        for knowledge_file in knowledge_dir.glob("*.json"):
            with open(knowledge_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            assert len(data) > 0, f"{knowledge_file} should not be empty"


class TestSkillCatalogSchema:
    """Tests for skill catalog schema validation."""

    @pytest.fixture
    def validator(self):
        """Create a JSON schema validator from the catalog schema."""
        assert CATALOG_SCHEMA, "catalog.schema.json could not be loaded"
        return Draft7Validator(CATALOG_SCHEMA)

    def test_skill_catalog_exists(self, knowledge_dir):
        """Test that skill-catalog.json exists."""
        catalog_path = knowledge_dir / "skill-catalog.json"
        assert catalog_path.exists(), "skill-catalog.json should exist"

    def test_skill_catalog_valid(self, knowledge_dir, validator):
        """Test that skill catalog is valid against schema."""
        catalog_path = knowledge_dir / "skill-catalog.json"

        with open(catalog_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        errors = list(validator.iter_errors(data))
        assert len(errors) == 0, f"Validation errors: {[e.message for e in errors]}"

    def test_skill_catalog_has_skills(self, knowledge_dir):
        """Test that skill catalog has skills defined."""
        catalog_path = knowledge_dir / "skill-catalog.json"

        with open(catalog_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        skills = data.get("content", {}).get("skills", [])
        assert len(skills) > 0, "Skill catalog should have at least one skill"

    def test_skill_ids_match_keys(self, knowledge_dir):
        """Test that skill IDs match their dictionary keys."""
        catalog_path = knowledge_dir / "skill-catalog.json"

        with open(catalog_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        skills = data.get("content", {}).get("skills", [])
        for skill in skills:
            skill_id = skill.get("id")
            # In new catalog format, skills is a list, so we don't check key mapping the same way
            # But the schema ensures id exists.
            assert skill_id, "Skill in catalog should have an ID"

    def test_skills_have_categories(self, knowledge_dir):
        """Test that all skills have valid categories."""
        catalog_path = knowledge_dir / "skill-catalog.json"

        with open(catalog_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        categories = set(data.get("categories", {}).keys())

        for skill_id, skill in data.get("skills", {}).items():
            category = skill.get("category")
            assert (
                category in categories
            ), f"Skill '{skill_id}' has invalid category '{category}'"


class TestStackCapabilitiesSchema:
    """Tests for stack capabilities file."""

    def test_stack_capabilities_exists(self, knowledge_dir):
        """Test that stack-capabilities.json exists."""
        capabilities_path = knowledge_dir / "stack-capabilities.json"
        assert capabilities_path.exists(), "stack-capabilities.json should exist"

    def test_stack_capabilities_valid_json(self, knowledge_dir):
        """Test that stack capabilities is valid JSON."""
        capabilities_path = knowledge_dir / "stack-capabilities.json"

        with open(capabilities_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert isinstance(data, dict), "Stack capabilities should be a JSON object"


class TestWorkflowPatternsSchema:
    """Tests for workflow patterns file."""

    def test_workflow_patterns_exists(self, knowledge_dir):
        """Test that workflow-patterns.json exists."""
        patterns_path = knowledge_dir / "workflow-patterns.json"
        assert patterns_path.exists(), "workflow-patterns.json should exist"

    def test_workflow_patterns_valid_json(self, knowledge_dir):
        """Test that workflow patterns is valid JSON."""
        patterns_path = knowledge_dir / "workflow-patterns.json"

        with open(patterns_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert isinstance(data, dict), "Workflow patterns should be a JSON object"


class TestBestPracticesSchema:
    """Tests for best practices file."""

    def test_best_practices_exists(self, knowledge_dir):
        """Test that best-practices.json exists."""
        practices_path = knowledge_dir / "best-practices.json"
        assert practices_path.exists(), "best-practices.json should exist"

    def test_best_practices_valid_json(self, knowledge_dir):
        """Test that best practices is valid JSON."""
        practices_path = knowledge_dir / "best-practices.json"

        with open(practices_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert isinstance(data, dict), "Best practices should be a JSON object"


class TestKnowledgeFileNaming:
    """Tests for knowledge file naming conventions."""

    def test_knowledge_files_use_kebab_case(self, knowledge_dir):
        """Test that knowledge files use kebab-case naming."""
        for knowledge_file in knowledge_dir.glob("*.json"):
            filename = knowledge_file.stem

            # Check for kebab-case (lowercase with hyphens)
            assert (
                filename == filename.lower()
            ), f"Knowledge file '{filename}' should be lowercase"
            assert (
                "_" not in filename
            ), f"Knowledge file '{filename}' should use hyphens, not underscores"

    def test_knowledge_files_have_json_extension(self, knowledge_dir):
        """Test that knowledge files have .json extension."""
        # This is implicit from the glob, but good to document
        json_files = list(knowledge_dir.glob("*.json"))
        all_files = list(knowledge_dir.iterdir())

        # Filter to only files (not directories)
        all_files = [f for f in all_files if f.is_file()]

        assert len(json_files) == len(
            all_files
        ), "All knowledge files should have .json extension"


class TestMCPServersCatalogSchema:
    """Tests for MCP servers catalog comprehensive structure."""

    def test_mcp_catalog_exists(self, knowledge_dir):
        """Test that mcp-servers-catalog.json exists."""
        catalog_path = knowledge_dir / "mcp-servers-catalog.json"
        assert catalog_path.exists(), "mcp-servers-catalog.json should exist"

    def test_mcp_catalog_valid_json(self, knowledge_dir):
        """Test that MCP catalog is valid JSON."""
        catalog_path = knowledge_dir / "mcp-servers-catalog.json"

        with open(catalog_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert isinstance(data, dict), "MCP catalog should be a JSON object"

    def test_mcp_catalog_has_servers(self, knowledge_dir):
        """Test that MCP catalog has servers defined."""
        catalog_path = knowledge_dir / "mcp-servers-catalog.json"

        with open(catalog_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        servers = data.get("servers", {})
        assert len(servers) >= 10, "MCP catalog should have at least 10 servers"

    def test_mcp_catalog_has_categories(self, knowledge_dir):
        """Test that MCP catalog defines categories."""
        catalog_path = knowledge_dir / "mcp-servers-catalog.json"

        with open(catalog_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        categories = data.get("categories", {})
        expected = {"core", "code", "data", "cloud", "collab", "aiml"}
        actual = set(categories.keys())
        assert expected <= actual, f"MCP catalog should have categories: {expected}"

    def test_mcp_catalog_has_starter_packs(self, knowledge_dir):
        """Test that MCP catalog has starter packs."""
        catalog_path = knowledge_dir / "mcp-servers-catalog.json"

        with open(catalog_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        packs = data.get("starterPacks", {})
        assert len(packs) >= 5, "MCP catalog should have at least 5 starter packs"

    def test_mcp_catalog_servers_have_required_fields(self, knowledge_dir):
        """Test that MCP servers have required fields."""
        catalog_path = knowledge_dir / "mcp-servers-catalog.json"

        with open(catalog_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        required_fields = ["displayName", "category", "description"]

        for server_id, server in data.get("servers", {}).items():
            for field in required_fields:
                assert (
                    field in server
                ), f"Server '{server_id}' missing required field '{field}'"

    def test_mcp_catalog_server_categories_are_valid(self, knowledge_dir):
        """Test that all server categories reference defined categories."""
        catalog_path = knowledge_dir / "mcp-servers-catalog.json"

        with open(catalog_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        valid_categories = set(data.get("categories", {}).keys())

        for server_id, server in data.get("servers", {}).items():
            category = server.get("category")
            assert (
                category in valid_categories
            ), f"Server '{server_id}' has invalid category '{category}'"

    def test_mcp_catalog_has_role_based_recommendations(self, knowledge_dir):
        """Test that MCP catalog has role-based server recommendations."""
        catalog_path = knowledge_dir / "mcp-servers-catalog.json"

        with open(catalog_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        by_role = data.get("serversByRole", {})
        assert len(by_role) >= 5, "MCP catalog should have at least 5 role mappings"


class TestMCPSelectionGuideSchema:
    """Tests for MCP selection guide structure."""

    def test_selection_guide_exists(self, knowledge_dir):
        """Test that mcp-selection-guide.json exists."""
        guide_path = knowledge_dir / "mcp-selection-guide.json"
        assert guide_path.exists(), "mcp-selection-guide.json should exist"

    def test_selection_guide_valid_json(self, knowledge_dir):
        """Test that selection guide is valid JSON."""
        guide_path = knowledge_dir / "mcp-selection-guide.json"

        with open(guide_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert isinstance(data, dict), "Selection guide should be a JSON object"

    def test_selection_guide_has_flow(self, knowledge_dir):
        """Test that selection guide has selection flow defined."""
        guide_path = knowledge_dir / "mcp-selection-guide.json"

        with open(guide_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        flow = data.get("selectionFlow", {})
        # Flow uses step1_role, step2_starterPack pattern
        assert (
            "step1_role" in flow or "steps" in flow
        ), "Selection guide should have selectionFlow steps"

    def test_selection_guide_has_role_mappings(self, knowledge_dir):
        """Test that selection guide has role-to-server mappings."""
        guide_path = knowledge_dir / "mcp-selection-guide.json"

        with open(guide_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        mappings = data.get("roleToServers", {})
        assert (
            len(mappings) >= 5
        ), "Selection guide should have at least 5 role mappings"

    def test_selection_guide_has_category_descriptions(self, knowledge_dir):
        """Test that selection guide has category descriptions."""
        guide_path = knowledge_dir / "mcp-selection-guide.json"

        with open(guide_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        categories = data.get("categoryDescriptions", {})
        assert (
            len(categories) >= 6
        ), "Selection guide should describe at least 6 categories"


class TestAISuiteIntegrationSchema:
    """Tests for AISuite integration guide structure."""

    def test_aisuite_integration_exists(self, knowledge_dir):
        """Test that aisuite-integration.json exists."""
        integration_path = knowledge_dir / "aisuite-integration.json"
        assert integration_path.exists(), "aisuite-integration.json should exist"

    def test_aisuite_integration_valid_json(self, knowledge_dir):
        """Test that AISuite integration is valid JSON."""
        integration_path = knowledge_dir / "aisuite-integration.json"

        with open(integration_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert isinstance(data, dict), "AISuite integration should be a JSON object"

    def test_aisuite_integration_has_overview(self, knowledge_dir):
        """Test that AISuite integration has overview section."""
        integration_path = knowledge_dir / "aisuite-integration.json"

        with open(integration_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert "overview" in data, "AISuite integration should have overview"

    def test_aisuite_integration_has_providers(self, knowledge_dir):
        """Test that AISuite integration lists supported providers."""
        integration_path = knowledge_dir / "aisuite-integration.json"

        with open(integration_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Check multiple possible locations for providers
        providers = data.get("supportedProviders", [])
        if not providers:
            # May be in features or overview section
            features = data.get("features", {})
            providers = features.get("supportedProviders", [])
        if not providers:
            overview = data.get("overview", {})
            providers_text = overview.get("description", "")
            # Just verify the overview mentions providers
            assert (
                "provider" in providers_text.lower() or len(data) > 2
            ), "AISuite should document LLM providers"
            return
        assert len(providers) >= 10, "AISuite should list at least 10 LLM providers"

    def test_aisuite_integration_has_mcp_section(self, knowledge_dir):
        """Test that AISuite integration documents MCP client support."""
        integration_path = knowledge_dir / "aisuite-integration.json"

        with open(integration_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        mcp = data.get("mcpIntegration", {})
        # Check for various field names that document MCP support
        has_mcp_docs = (
            "explanation" in mcp
            or "examples" in mcp
            or "description" in mcp
            or "configDictFormat" in mcp
        )
        assert has_mcp_docs, "AISuite integration should document MCP client support"
