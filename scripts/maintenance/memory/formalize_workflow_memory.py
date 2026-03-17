import os
import yaml
import re
import json
from pathlib import Path
from typing import List, Dict, Set

# --- Configuration ---
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
WORKFLOWS_DIR = ROOT_DIR / ".agent" / "workflows"
OUTPUT_JSON = ROOT_DIR / ".agent" / "knowledge" / "workflow-structural-patterns.json"


class MemoryFormalizer:
    def __init__(self):
        self.entities = []
        self.relations = []
        self.local_patterns = {}

    def parse_workflow(self, file_path: Path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        wf_name = file_path.stem

        # Extract version/description from frontmatter
        version = "1.0.0"
        description = ""
        if content.startswith("---"):
            try:
                fm = yaml.safe_load(content.split("---")[1])
                version = fm.get("version", "1.0.0")
                description = fm.get("description", "")
            except Exception:
                pass

        # Create Workflow Entity
        self.entities.append(
            {
                "name": wf_name,
                "entityType": "Workflow",
                "observations": [
                    f"Description: {description}",
                    f"Version: {version}",
                    f"File: {file_path.name}",
                ],
            }
        )

        # Extract Phases
        phases = re.findall(r"###\s*\d*\.?\s*(.+)", content)
        for phase in phases:
            phase_name = f"{wf_name}: {phase.strip()}"
            self.entities.append(
                {
                    "name": phase_name,
                    "entityType": "WorkflowPhase",
                    "observations": [f"Part of workflow {wf_name}"],
                }
            )
            self.relations.append(
                {"from": wf_name, "to": phase_name, "relationType": "contains_phase"}
            )

        # Extract Agents & Skills (Basic Extraction)
        # Agent: CODE
        agent_matches = re.findall(
            r"\b(?:Agent|agent|@persona):\s*[`]?([A-Z][A-Z0-9_\-]+)\b", content
        )
        for agent in set(agent_matches):
            self.relations.append(
                {"from": wf_name, "to": agent, "relationType": "executed_by"}
            )

        # Skill: name
        skill_matches = re.findall(
            r"(?:Skill|skill|uses):\s*[`]?([a-z0-9_\-]+)[`]?", content
        )
        skill_matches += re.findall(r"\[\[([a-z0-9_\-]+)\]\]", content)
        for skill in set(skill_matches):
            if skill not in ["name", "skill", "none", "patterns"]:
                self.relations.append(
                    {"from": wf_name, "to": skill, "relationType": "utilizes_skill"}
                )

        # Store in local pattern format
        self.local_patterns[wf_name] = {
            "phases": phases,
            "agents": list(set(agent_matches)),
            "skills": list(set(skill_matches)),
        }

    def run(self):
        print(f"--- Formalizing Memory (Workflows Path: {WORKFLOWS_DIR}) ---")

        workflows = list(WORKFLOWS_DIR.glob("*.md"))
        for wf_path in workflows:
            self.parse_workflow(wf_path)

        # Build final local pattern file
        result = {
            "id": "workflow-structural-patterns",
            "name": "Workflow Structural Patterns",
            "version": "1.0.0",
            "category": "Methodology",
            "description": "Formalized taxonomy of workflow phases, agents, and skills.",
            "patterns": self.local_patterns,
            "mcp_entities": self.entities,
            "mcp_relations": self.relations,
        }

        # Ensure directory exists
        OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)

        with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

        print(f"Formalized structural knowledge for {len(workflows)} workflows.")
        print(f"Saved to: {OUTPUT_JSON}")
        print(f"Total Entities: {len(self.entities)}, Relations: {len(self.relations)}")


if __name__ == "__main__":
    formalizer = MemoryFormalizer()
    formalizer.run()
