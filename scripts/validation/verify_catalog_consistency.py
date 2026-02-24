import json
from pathlib import Path


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def verify_consistency():
    root = Path(".")
    agent_staffing_path = root / ".agent/knowledge/agent-staffing.json"
    workflow_catalog_path = root / ".agent/knowledge/workflow-catalog.json"
    mcp_catalog_path = root / ".agent/knowledge/mcp-servers-catalog.json"
    evolution_protocol_path = root / ".agent/knowledge/evolution-protocol.json"

    issues = []

    # 1. Load data
    staffing = load_json(agent_staffing_path)
    workflows = load_json(workflow_catalog_path)
    mcp = load_json(mcp_catalog_path)
    evolution = load_json(evolution_protocol_path)

    specialist_ids = [s["id"] for s in staffing["specialists"].values()]
    mcp_server_ids = list(mcp["servers"].keys())

    # 2. Verify Specialists
    for key, spec in staffing["specialists"].items():
        # Verify agent file exists
        agent_path = root / ".agent/agents" / spec["agent"]
        if not agent_path.exists():
            issues.append(
                f"Specialist {key}: Agent file {spec['agent']} does not exist."
            )

        # Verify MCP servers exist
        for srv in spec.get("authorized_mcp_servers", []):
            if srv not in mcp_server_ids and srv not in [
                "pms",
                "google-workspace",
                "azure",
                "sap-btp",
            ]:  # Some are logical/external
                issues.append(
                    f"Specialist {key}: Authorized MCP server {srv} not in catalog."
                )

    # 3. Verify Workflows
    for wf in workflows["content"]["workflows"]:
        if "location" in wf:
            wf_path = root / wf["location"]
            if not wf_path.exists():
                issues.append(
                    f"Workflow {wf['id']}: Location {wf['location']} does not exist."
                )

        # Verify phases
        for phase in wf.get("phases", []):
            if phase["lead_specialist"] not in specialist_ids:
                issues.append(
                    f"Workflow {wf['id']}, Phase {phase['name']}: Lead specialist {phase['lead_specialist']} not in agent-staffing."
                )

    if issues:
        print("FAIL: Consistency issues found:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("PASS: Cross-catalog consistency verified.")


if __name__ == "__main__":
    verify_consistency()
