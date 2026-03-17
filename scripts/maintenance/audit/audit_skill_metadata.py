import os
import yaml
import json
from pathlib import Path

SKILLS_DIR = Path(__file__).resolve().parent.parent.parent.parent / ".agent" / "skills"


def audit_skills():
    audit_results = []

    for root, dirs, files in os.walk(SKILLS_DIR):
        if "SKILL.md" in files:
            skill_path = os.path.join(root, "SKILL.md")
            with open(skill_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Basic YAML frontmatter extraction
            parts = content.split("---")
            if len(parts) >= 3:
                try:
                    metadata = yaml.safe_load(parts[1])
                    rel_path = os.path.relpath(skill_path, SKILLS_DIR)

                    gaps = []
                    fields_to_check = [
                        "agents",
                        "knowledge",
                        "templates",
                        "related_skills",
                        "references",
                        "settings",
                    ]

                    for field in fields_to_check:
                        val = metadata.get(field)
                        if val is None or (isinstance(val, list) and len(val) == 0):
                            gaps.append(field)

                    if gaps:
                        audit_results.append(
                            {
                                "path": rel_path,
                                "name": metadata.get("name", "unknown"),
                                "gaps": gaps,
                            }
                        )
                except Exception as e:
                    print(f"Error parsing {skill_path}: {e}")

    return audit_results


if __name__ == "__main__":
    results = audit_skills()
    print(json.dumps(results, indent=2))
