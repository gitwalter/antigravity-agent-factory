import json
import os
from pathlib import Path


def test_agent_registry_consistency():
    """Verifies that all registered agents have consistent metadata and existing skill references."""
    root = Path(__file__).parent.parent.parent
    registry_path = root / ".agent" / "knowledge" / "agent-team-registry.json"
    skill_catalog_path = root / ".agent" / "knowledge" / "skill-catalog.json"

    with open(registry_path, "r", encoding="utf-8") as f:
        registry = json.load(f)
    with open(skill_catalog_path, "r", encoding="utf-8") as f:
        catalog_data = json.load(f)
        # Handle both old flat structure and new nested structure
        skills_list = catalog_data.get("skills", [])
        if not skills_list and "content" in catalog_data:
            skills_list = catalog_data["content"].get("skills", [])

        # Convert to dict for lookup
        skill_catalog = {s["id"]: s for s in skills_list}

    for agent in registry["agents"]:
        # Check DID format
        assert agent["did"].startswith(
            "did:agent:"
        ), f"Invalid DID for {agent['agent_id']}"

        # Check if skills exist in catalog
        for skill_id in agent["skills"]:
            # Handle both bare IDs and prefixed IDs in agent skills list
            bare_skill_id = skill_id.split(":", 1)[1] if ":" in skill_id else skill_id
            assert (
                bare_skill_id in skill_catalog
            ), f"Agent {agent['agent_id']} references unregistered skill: {skill_id}"

        # Check if agent definition file exists (optional, as some registry entries are logical)
        if "path" in agent:
            path_str = agent["path"].replace("/", os.sep).replace("\\", os.sep)
            agent_path = root / path_str
            assert (
                agent_path.exists()
            ), f"Agent definition file missing for {agent['agent_id']}: {agent_path}"


def test_skill_catalog_paths():
    """Verifies that all skill definitions exist at their declared paths."""
    root = Path(__file__).parent.parent.parent
    skill_catalog_path = root / ".agent" / "knowledge" / "skill-catalog.json"

    with open(skill_catalog_path, "r", encoding="utf-8") as f:
        catalog_data = json.load(f)
        # Handle both old flat structure and new nested structure
        skills_list = catalog_data.get("skills", [])
        if not skills_list and "content" in catalog_data:
            skills_list = catalog_data["content"].get("skills", [])

        # Convert to dict for iteration
        skill_catalog = {s["id"]: s for s in skills_list}

    for skill_id, skill in skill_catalog.items():
        # Skill might have 'factorySkill' or 'factoryPattern'
        path_key = "factorySkill" if "factorySkill" in skill else "factoryPattern"

        # If the skill is not implemented in Factory, skip path check
        if path_key not in skill or not skill[path_key]:
            continue

        path_str = (
            skill[path_key]
            .replace("{directories.skills}", ".agent/skills")
            .replace("{directories.patterns}", ".agent/patterns")
        )
        path_str = path_str.replace("/", os.sep).replace("\\", os.sep)
        skill_path = root / path_str
        assert (
            skill_path.exists()
        ), f"Skill definition missing for {skill_id}: {skill_path} (from {path_key})"


def test_graph_integrity():
    """Verifies that the dependency graph nodes exist and edges point to valid nodes."""
    root = Path(__file__).parent.parent.parent
    graph_path = root / ".agent" / "knowledge" / "dependency-graph.json"

    with open(graph_path, "r", encoding="utf-8") as f:
        graph = json.load(f)

    nodes = graph["nodes"]
    for edge in graph["edges"]:
        # Standardize node lookup for 'from' and 'to'
        for key in ["from", "to"]:
            node_id = edge[key]
            ignored_targets = [
                "template:",
                "pattern:",
                "skill:",
                "agent:",
                "knowledge:",
            ]

            # Check if direct match
            if node_id in nodes:
                continue

            # Check if bare ID match
            bare_id = node_id.split(":", 1)[1] if ":" in node_id else node_id
            if bare_id in nodes:
                continue

            # Allow certain prefixes to be ignored if they are external or templates
            if any(node_id.startswith(prefix) for prefix in ignored_targets):
                continue

            assert node_id in nodes, f"Edge {key} unknown node/target: {node_id}"
