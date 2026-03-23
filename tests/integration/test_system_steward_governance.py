import json
from pathlib import Path


def test_system_steward_metadata():
    """Integration test checking system-steward ability and knowledge integration."""
    root = Path(__file__).parent.parent.parent
    knowledge_dir = root / ".agent" / "knowledge"
    registry_path = knowledge_dir / "agents" / "agent-team-registry.json"

    with open(registry_path, "r", encoding="utf-8") as f:
        registry = json.load(f)

    steward = next(
        (a for a in registry["agents"] if a["agent_id"] == "system-steward"), None
    )
    assert steward is not None
    assert "governing-repositories" in steward["skills"]
    assert "registry-clerk" in steward["delegation_to"]

    clerk = next(
        (a for a in registry["agents"] if a["agent_id"] == "registry-clerk"), None
    )
    assert clerk is not None
    assert "registering-systems" in clerk["skills"]


def test_maintenance_script_availability():
    """Ensures the core script used by the steward is where it should be."""
    root = Path(__file__).parent.parent.parent
    knowledge_dir = root / ".agent" / "knowledge"
    feed_path = knowledge_dir / "integration" / "factory-updates.json"
    script_path = root / "scripts" / "maintenance" / "audit" / "link_checker.py"

    assert feed_path.exists()
    assert script_path.exists()
