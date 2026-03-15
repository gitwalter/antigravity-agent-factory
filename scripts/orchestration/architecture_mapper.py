import os
import json
import re


def parse_markdown_metadata(filepath):
    """Simple parser to extract metadata from PRD/NFR."""
    if not os.path.exists(filepath):
        return {}

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    metadata = {}
    # Find agents
    agents_match = re.search(r"- \*\*Agents\*\*: (.*)", content)
    if agents_match:
        metadata["agents"] = [a.strip(" `") for a in agents_match.group(1).split(",")]

    # Find functional requirements
    fr_matches = re.findall(r"- \[FR\d+\]: (.*)", content)
    metadata["functional_requirements"] = fr_matches

    return metadata


def generate_architecture_graph():
    """Generates the sdlc-architecture-graph.json based on requirements."""
    print("[MAPPER] Generating Architecture Graph...")

    prd_data = parse_markdown_metadata("knowledge/prd.md")
    nfr_data = parse_markdown_metadata("knowledge/nfr.md")

    graph = {
        "nodes": [
            {
                "id": "REQ-1",
                "type": "requirement",
                "label": "SDLC Phase 3 Core",
                "source": "knowledge/prd.md",
            },
            {
                "id": "COMP-1",
                "type": "component",
                "label": "Architecture Mapper",
                "agent": "workflow-architect",
            },
        ],
        "edges": [
            {"from": "REQ-1", "to": "COMP-1", "label": "implemented_by"},
        ],
        "metadata": {
            "agents": prd_data.get("agents", []),
            "functional_coverage": len(prd_data.get("functional_requirements", [])),
        },
    }

    output_path = "knowledge/sdlc-architecture-graph.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(graph, f, indent=2)

    print(f"[SUCCESS] Architecture Graph written to {output_path}")


if __name__ == "__main__":
    generate_architecture_graph()
