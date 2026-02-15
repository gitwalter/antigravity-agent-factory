"""
Unit tests for PM adapter JSON files.

Tests cover:
- Adapter interface structure validation
- Adapter-specific mappings (GitHub, Jira, Azure DevOps, Linear)
- Cross-adapter consistency checks
"""

import json
import sys
from pathlib import Path

import pytest

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


@pytest.fixture
def adapters_dir(factory_root):
    """Get the PM adapters directory.

    Args:
        factory_root: Factory root directory fixture.

    Returns:
        Path to PM adapters directory.
    """
    return factory_root / ".agent" / "patterns" / "products" / "pm-system" / "adapters"


@pytest.fixture
def adapter_interface_path(adapters_dir):
    """Get the adapter interface JSON file path.

    Args:
        adapters_dir: Adapters directory fixture.

    Returns:
        Path to adapter-interface.json.
    """
    return adapters_dir / "adapter-interface.json"


@pytest.fixture
def github_adapter_path(adapters_dir):
    """Get the GitHub adapter JSON file path."""
    return adapters_dir / "github-adapter.json"


@pytest.fixture
def jira_adapter_path(adapters_dir):
    """Get the Jira adapter JSON file path."""
    return adapters_dir / "jira-adapter.json"


@pytest.fixture
def azure_devops_adapter_path(adapters_dir):
    """Get the Azure DevOps adapter JSON file path."""
    return adapters_dir / "azure-devops-adapter.json"


@pytest.fixture
def linear_adapter_path(adapters_dir):
    """Get the Linear adapter JSON file path."""
    return adapters_dir / "linear-adapter.json"


class TestAdapterInterface:
    """Tests for adapter-interface.json structure."""

    def test_interface_file_exists(self, adapter_interface_path):
        """Test that adapter-interface.json exists."""
        assert adapter_interface_path.exists()

    def test_interface_is_valid_json(self, adapter_interface_path):
        """Test that adapter-interface.json is valid JSON."""
        try:
            with open(adapter_interface_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            assert isinstance(data, dict)
        except json.JSONDecodeError as e:
            pytest.fail(f"Invalid JSON in {adapter_interface_path}: {e}")

    def test_interface_defines_work_item_operations(self, adapter_interface_path):
        """Test that interface defines work item operations."""
        with open(adapter_interface_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Check schema structure (JSON Schema file)
        assert "properties" in data, "Missing 'properties' in adapter-interface.json"
        assert (
            "interface" in data["properties"]
        ), "Missing 'interface' property in schema"
        interface_props = data["properties"]["interface"]["properties"]
        assert (
            "workItems" in interface_props
        ), "Missing 'workItems' in interface properties"

        work_items_props = interface_props["workItems"]["properties"]
        required_ops = [
            "createEpic",
            "createStory",
            "createTask",
            "createBug",
            "updateStatus",
            "assignItem",
            "getItem",
            "listItems",
        ]

        for op in required_ops:
            assert op in work_items_props, f"Missing '{op}' in workItems properties"

    def test_interface_defines_planning_operations(self, adapter_interface_path):
        """Test that interface defines planning operations."""
        with open(adapter_interface_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Check schema structure
        interface_props = data["properties"]["interface"]["properties"]
        assert (
            "planning" in interface_props
        ), "Missing 'planning' in interface properties"

        planning_props = interface_props["planning"]["properties"]
        required_ops = [
            "createSprint",
            "addToSprint",
            "closeSprint",
            "getSprint",
            "listSprints",
        ]

        for op in required_ops:
            assert op in planning_props, f"Missing '{op}' in planning properties"

    def test_interface_defines_board_operations(self, adapter_interface_path):
        """Test that interface defines board operations."""
        with open(adapter_interface_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Check schema structure
        interface_props = data["properties"]["interface"]["properties"]
        assert "boards" in interface_props, "Missing 'boards' in interface properties"

        boards_props = interface_props["boards"]["properties"]
        required_ops = ["getBoard", "moveCard", "getBoardColumns"]

        for op in required_ops:
            assert op in boards_props, f"Missing '{op}' in boards properties"

    def test_interface_defines_metrics_operations(self, adapter_interface_path):
        """Test that interface defines metrics operations."""
        with open(adapter_interface_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Check schema structure
        interface_props = data["properties"]["interface"]["properties"]
        assert "metrics" in interface_props, "Missing 'metrics' in interface properties"

        metrics_props = interface_props["metrics"]["properties"]
        required_ops = [
            "getVelocity",
            "getBurndown",
            "getCycleTime",
            "getLeadTime",
            "getWIP",
        ]

        for op in required_ops:
            assert op in metrics_props, f"Missing '{op}' in metrics properties"

    def test_interface_defines_documentation_operations(self, adapter_interface_path):
        """Test that interface defines documentation operations."""
        with open(adapter_interface_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Check schema structure
        interface_props = data["properties"]["interface"]["properties"]
        assert (
            "documentation" in interface_props
        ), "Missing 'documentation' in interface properties"

        documentation_props = interface_props["documentation"]["properties"]
        required_ops = ["createPage", "updatePage", "getPage", "linkToWorkItem"]

        for op in required_ops:
            assert (
                op in documentation_props
            ), f"Missing '{op}' in documentation properties"


class TestGitHubAdapter:
    """Tests for github-adapter.json mappings."""

    def test_github_adapter_exists(self, github_adapter_path):
        """Test that github-adapter.json exists."""
        assert github_adapter_path.exists()

    def test_github_adapter_is_valid_json(self, github_adapter_path):
        """Test that github-adapter.json is valid JSON."""
        try:
            with open(github_adapter_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            assert isinstance(data, dict)
        except json.JSONDecodeError as e:
            pytest.fail(f"Invalid JSON in {github_adapter_path}: {e}")

    def test_github_epic_mapping(self, github_adapter_path):
        """Test GitHub epic mapping (Epic → Issue with label)."""
        with open(github_adapter_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Check examples section for actual instance data
        assert "examples" in data, "Missing 'examples' in github-adapter.json"
        assert len(data["examples"]) > 0, "No examples found"

        example = data["examples"][0]
        assert "mappings" in example, "Missing 'mappings' in example"
        assert "concepts" in example["mappings"], "Missing 'concepts' in mappings"

        concepts = example["mappings"]["concepts"]
        assert "epic" in concepts, "Missing 'epic' concept mapping"
        assert (
            "issue" in concepts["epic"].lower() and "label" in concepts["epic"].lower()
        ), "Epic mapping should reference Issue with label"

        # Also check schema structure
        assert "properties" in data, "Missing 'properties' in schema"
        assert "mappings" in data["properties"], "Missing 'mappings' property"
        mappings_props = data["properties"]["mappings"]["properties"]
        assert "concepts" in mappings_props, "Missing 'concepts' in mappings properties"
        assert (
            "workItems" in mappings_props
        ), "Missing 'workItems' in mappings properties"

    def test_github_story_mapping(self, github_adapter_path):
        """Test GitHub story mapping."""
        with open(github_adapter_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Check schema structure
        mappings_props = data["properties"]["mappings"]["properties"]
        work_items_props = mappings_props["workItems"]["properties"]
        assert (
            "createStory" in work_items_props
        ), "Missing 'createStory' in workItems properties"

        # Verify createStory has mapping structure
        create_story_props = work_items_props["createStory"]["properties"]
        assert (
            "mapping" in create_story_props
        ), "Missing 'mapping' in createStory properties"

    def test_github_sprint_mapping(self, github_adapter_path):
        """Test GitHub sprint mapping (Sprint → Milestone)."""
        with open(github_adapter_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Check examples section
        example = data["examples"][0]
        concepts = example["mappings"]["concepts"]
        assert "sprint" in concepts, "Missing 'sprint' concept mapping"
        assert (
            "milestone" in concepts["sprint"].lower()
        ), "Sprint should map to Milestone"

        # Check schema structure
        mappings_props = data["properties"]["mappings"]["properties"]
        assert "planning" in mappings_props, "Missing 'planning' in mappings properties"
        planning_props = mappings_props["planning"]["properties"]
        assert (
            "createSprint" in planning_props
        ), "Missing 'createSprint' in planning properties"

    def test_github_board_mapping(self, github_adapter_path):
        """Test GitHub board mapping (Board → Project v2)."""
        with open(github_adapter_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Check examples section
        example = data["examples"][0]
        concepts = example["mappings"]["concepts"]
        assert "board" in concepts, "Missing 'board' concept mapping"
        assert "project" in concepts["board"].lower(), "Board should map to Project"

        # Check schema structure
        mappings_props = data["properties"]["mappings"]["properties"]
        assert "boards" in mappings_props, "Missing 'boards' in mappings properties"
        boards_props = mappings_props["boards"]["properties"]
        assert "getBoard" in boards_props, "Missing 'getBoard' in boards properties"


class TestJiraAdapter:
    """Tests for jira-adapter.json mappings."""

    def test_jira_adapter_exists(self, jira_adapter_path):
        """Test that jira-adapter.json exists."""
        assert jira_adapter_path.exists()

    def test_jira_adapter_is_valid_json(self, jira_adapter_path):
        """Test that jira-adapter.json is valid JSON."""
        try:
            with open(jira_adapter_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            assert isinstance(data, dict)
        except json.JSONDecodeError as e:
            pytest.fail(f"Invalid JSON in {jira_adapter_path}: {e}")

    def test_jira_epic_mapping(self, jira_adapter_path):
        """Test Jira epic mapping."""
        with open(jira_adapter_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Check examples section
        example = data["examples"][0]
        assert "mappings" in example, "Missing 'mappings' in example"
        assert "concepts" in example["mappings"], "Missing 'concepts' in mappings"
        assert (
            "epic" in example["mappings"]["concepts"]
        ), "Missing 'epic' concept mapping"

        # Check schema structure
        mappings_props = data["properties"]["mappings"]["properties"]
        work_items_props = mappings_props["workItems"]["properties"]
        assert (
            "createEpic" in work_items_props
        ), "Missing 'createEpic' in workItems properties"

    def test_jira_story_mapping(self, jira_adapter_path):
        """Test Jira story mapping."""
        with open(jira_adapter_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Check schema structure
        mappings_props = data["properties"]["mappings"]["properties"]
        work_items_props = mappings_props["workItems"]["properties"]
        assert (
            "createStory" in work_items_props
        ), "Missing 'createStory' in workItems properties"

        # Check that epicId mapping exists
        create_story_props = work_items_props["createStory"]["properties"]
        assert "mapping" in create_story_props, "Missing 'mapping' in createStory"
        mapping_props = create_story_props["mapping"]["properties"]
        assert "epicId" in mapping_props, "createStory mapping should support epicId"

    def test_jira_sprint_mapping(self, jira_adapter_path):
        """Test Jira sprint mapping."""
        with open(jira_adapter_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Check examples section
        example = data["examples"][0]
        concepts = example["mappings"]["concepts"]
        assert "sprint" in concepts, "Missing 'sprint' concept mapping"
        assert (
            "sprint" in concepts["sprint"].lower()
        ), "Sprint should map to Jira Sprint"

        # Check schema structure
        mappings_props = data["properties"]["mappings"]["properties"]
        assert "planning" in mappings_props, "Missing 'planning' in mappings properties"
        planning_props = mappings_props["planning"]["properties"]
        assert (
            "createSprint" in planning_props
        ), "Missing 'createSprint' in planning properties"

    def test_jira_has_jql_patterns(self, jira_adapter_path):
        """Test that Jira adapter has JQL patterns."""
        with open(jira_adapter_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Check schema structure
        mappings_props = data["properties"]["mappings"]["properties"]
        work_items_props = mappings_props["workItems"]["properties"]
        assert (
            "listItems" in work_items_props
        ), "Missing 'listItems' in workItems properties"

        list_items_props = work_items_props["listItems"]["properties"]
        assert (
            "jqlPatterns" in list_items_props
        ), "Missing 'jqlPatterns' in listItems properties"

        jql_patterns_props = list_items_props["jqlPatterns"]["properties"]
        assert isinstance(
            jql_patterns_props, dict
        ), "jqlPatterns properties should be an object"
        assert (
            len(jql_patterns_props) > 0
        ), "jqlPatterns should contain pattern definitions"


class TestAzureDevOpsAdapter:
    """Tests for azure-devops-adapter.json mappings."""

    def test_azure_adapter_exists(self, azure_devops_adapter_path):
        """Test that azure-devops-adapter.json exists."""
        assert azure_devops_adapter_path.exists()

    def test_azure_adapter_is_valid_json(self, azure_devops_adapter_path):
        """Test that azure-devops-adapter.json is valid JSON."""
        try:
            with open(azure_devops_adapter_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            assert isinstance(data, dict)
        except json.JSONDecodeError as e:
            pytest.fail(f"Invalid JSON in {azure_devops_adapter_path}: {e}")

    def test_azure_epic_mapping(self, azure_devops_adapter_path):
        """Test Azure DevOps epic mapping."""
        with open(azure_devops_adapter_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Check examples section
        example = data["examples"][0]
        assert "mappings" in example, "Missing 'mappings' in example"
        assert "concepts" in example["mappings"], "Missing 'concepts' in mappings"
        assert (
            "epic" in example["mappings"]["concepts"]
        ), "Missing 'epic' concept mapping"

        # Check schema structure
        mappings_props = data["properties"]["mappings"]["properties"]
        work_items_props = mappings_props["workItems"]["properties"]
        assert (
            "createEpic" in work_items_props
        ), "Missing 'createEpic' in workItems properties"

        create_epic_props = work_items_props["createEpic"]["properties"]
        assert (
            "apiEndpoint" in create_epic_props
        ), "Missing 'apiEndpoint' in createEpic properties"

    def test_azure_sprint_mapping(self, azure_devops_adapter_path):
        """Test Azure DevOps sprint mapping (Sprint → Iteration)."""
        with open(azure_devops_adapter_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Check examples section
        example = data["examples"][0]
        concepts = example["mappings"]["concepts"]
        assert "sprint" in concepts, "Missing 'sprint' concept mapping"
        assert (
            "iteration" in concepts["sprint"].lower()
        ), "Sprint should map to Iteration"

        # Check schema structure
        mappings_props = data["properties"]["mappings"]["properties"]
        assert "planning" in mappings_props, "Missing 'planning' in mappings properties"
        planning_props = mappings_props["planning"]["properties"]
        assert (
            "createSprint" in planning_props
        ), "Missing 'createSprint' in planning properties"

        create_sprint_props = planning_props["createSprint"]["properties"]
        assert (
            "apiEndpoint" in create_sprint_props
        ), "Missing 'apiEndpoint' in createSprint properties"

    def test_azure_has_wiql_patterns(self, azure_devops_adapter_path):
        """Test that Azure DevOps adapter has WIQL patterns."""
        with open(azure_devops_adapter_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Check schema structure
        mappings_props = data["properties"]["mappings"]["properties"]
        work_items_props = mappings_props["workItems"]["properties"]
        assert (
            "listItems" in work_items_props
        ), "Missing 'listItems' in workItems properties"

        list_items_props = work_items_props["listItems"]["properties"]
        assert (
            "wiqlPatterns" in list_items_props
        ), "Missing 'wiqlPatterns' in listItems properties"

        wiql_patterns_props = list_items_props["wiqlPatterns"]["properties"]
        assert isinstance(
            wiql_patterns_props, dict
        ), "wiqlPatterns properties should be an object"
        assert (
            len(wiql_patterns_props) > 0
        ), "wiqlPatterns should contain pattern definitions"


class TestLinearAdapter:
    """Tests for linear-adapter.json mappings."""

    def test_linear_adapter_exists(self, linear_adapter_path):
        """Test that linear-adapter.json exists."""
        assert linear_adapter_path.exists()

    def test_linear_adapter_is_valid_json(self, linear_adapter_path):
        """Test that linear-adapter.json is valid JSON."""
        try:
            with open(linear_adapter_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            assert isinstance(data, dict)
        except json.JSONDecodeError as e:
            pytest.fail(f"Invalid JSON in {linear_adapter_path}: {e}")

    def test_linear_epic_mapping(self, linear_adapter_path):
        """Test Linear epic mapping (Epic → Project)."""
        with open(linear_adapter_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Check examples section
        example = data["examples"][0]
        concepts = example["mappings"]["concepts"]
        assert "epic" in concepts, "Missing 'epic' concept mapping"
        assert "project" in concepts["epic"].lower(), "Epic should map to Project"

        # Check schema structure
        mappings_props = data["properties"]["mappings"]["properties"]
        work_items_props = mappings_props["workItems"]["properties"]
        assert (
            "createEpic" in work_items_props
        ), "Missing 'createEpic' in workItems properties"

        create_epic_props = work_items_props["createEpic"]["properties"]
        assert (
            "graphqlMutation" in create_epic_props
        ), "Missing 'graphqlMutation' in createEpic properties"

    def test_linear_sprint_mapping(self, linear_adapter_path):
        """Test Linear sprint mapping (Sprint → Cycle)."""
        with open(linear_adapter_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Check examples section
        example = data["examples"][0]
        concepts = example["mappings"]["concepts"]
        assert "sprint" in concepts, "Missing 'sprint' concept mapping"
        assert "cycle" in concepts["sprint"].lower(), "Sprint should map to Cycle"

        # Check schema structure
        mappings_props = data["properties"]["mappings"]["properties"]
        assert "planning" in mappings_props, "Missing 'planning' in mappings properties"
        planning_props = mappings_props["planning"]["properties"]
        assert (
            "createSprint" in planning_props
        ), "Missing 'createSprint' in planning properties"

        create_sprint_props = planning_props["createSprint"]["properties"]
        assert (
            "graphqlMutation" in create_sprint_props
        ), "Missing 'graphqlMutation' in createSprint properties"


class TestAdapterConsistency:
    """Cross-adapter consistency tests."""

    def test_all_adapters_implement_create_epic(self, adapters_dir):
        """Test that all adapters implement createEpic operation."""
        adapter_files = [
            "github-adapter.json",
            "jira-adapter.json",
            "azure-devops-adapter.json",
            "linear-adapter.json",
        ]

        for adapter_file in adapter_files:
            adapter_path = adapters_dir / adapter_file
            if not adapter_path.exists():
                continue

            with open(adapter_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Check schema structure
            assert "properties" in data, f"Missing 'properties' in {adapter_file}"
            assert (
                "mappings" in data["properties"]
            ), f"Missing 'mappings' property in {adapter_file}"
            mappings_props = data["properties"]["mappings"]["properties"]
            assert (
                "workItems" in mappings_props
            ), f"Missing 'workItems' in {adapter_file}"
            work_items_props = mappings_props["workItems"]["properties"]
            assert (
                "createEpic" in work_items_props
            ), f"Missing 'createEpic' in {adapter_file}"

    def test_all_adapters_implement_create_story(self, adapters_dir):
        """Test that all adapters implement createStory operation."""
        adapter_files = [
            "github-adapter.json",
            "jira-adapter.json",
            "azure-devops-adapter.json",
            "linear-adapter.json",
        ]

        for adapter_file in adapter_files:
            adapter_path = adapters_dir / adapter_file
            if not adapter_path.exists():
                continue

            with open(adapter_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Check schema structure
            mappings_props = data["properties"]["mappings"]["properties"]
            work_items_props = mappings_props["workItems"]["properties"]
            assert (
                "createStory" in work_items_props
            ), f"Missing 'createStory' in {adapter_file}"

    def test_all_adapters_implement_create_sprint(self, adapters_dir):
        """Test that all adapters implement createSprint operation."""
        adapter_files = [
            "github-adapter.json",
            "jira-adapter.json",
            "azure-devops-adapter.json",
            "linear-adapter.json",
        ]

        for adapter_file in adapter_files:
            adapter_path = adapters_dir / adapter_file
            if not adapter_path.exists():
                continue

            with open(adapter_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Check schema structure
            mappings_props = data["properties"]["mappings"]["properties"]
            assert "planning" in mappings_props, f"Missing 'planning' in {adapter_file}"
            planning_props = mappings_props["planning"]["properties"]
            assert (
                "createSprint" in planning_props
            ), f"Missing 'createSprint' in {adapter_file}"
