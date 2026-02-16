import os
import json
import re

SKILLS_ROOT = (
    r"d:\Users\wpoga\Documents\Python Scripts\antigravity-agent-factory\.agent\skills"
)
CATALOG_PATH = r"d:\Users\wpoga\Documents\Python Scripts\antigravity-agent-factory\.agent\knowledge\skill-catalog.json"


def reconstruct_catalog():
    with open(CATALOG_PATH, "r") as f:
        catalog = json.load(f)

    new_skills = {}

    # Walk skills directory
    for root, dirs, files in os.walk(SKILLS_ROOT):
        if "SKILL.md" in files:
            skill_id = os.path.basename(root)
            pattern = os.path.basename(os.path.dirname(root))  # chain, parallel etc

            # Read SKILL.md for metadata
            skill_md_path = os.path.join(root, "SKILL.md")
            with open(skill_md_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Try to extract Name and Description from YAML or H1
            name = skill_id.replace("-", " ").title()
            description = f"Specialized skill for {name}"
            category = "core"  # Default

            # Simple regex extraction for YAML frontmatter
            match = re.search(r"---(.*?)---", content, re.DOTALL)
            if match:
                yaml_content = match.group(1)
                name_match = re.search(r"name:\s*(.*)", yaml_content)
                if name_match:
                    name = name_match.group(1).strip().strip('"')
                desc_match = re.search(r"description:\s*(.*)", yaml_content)
                if desc_match:
                    description = desc_match.group(1).strip().strip('"')
                cat_match = re.search(r"category:\s*(.*)", yaml_content)
                if cat_match:
                    category = cat_match.group(1).strip().strip('"')

            new_skills[skill_id] = {
                "id": skill_id,
                "name": name,
                "category": category,
                "description": description,
                "factorySkill": f"{{directories.skills}}/{pattern}/{skill_id}/SKILL.md",
                "pattern_type": pattern,
            }

    catalog["skills"] = new_skills
    with open(CATALOG_PATH, "w") as f:
        json.dump(catalog, f, indent=4)

    print(f"Reconstructed catalog with {len(new_skills)} skills.")


if __name__ == "__main__":
    reconstruct_catalog()
