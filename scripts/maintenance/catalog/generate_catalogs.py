import os
import json
import re

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
KNOWLEDGE_DIR = os.path.join(ROOT_DIR, ".agent", "knowledge")
SKILLS_DIR = os.path.join(ROOT_DIR, ".agent", "skills")
PATTERNS_DIR = os.path.join(ROOT_DIR, ".agent", "patterns")
TEMPLATES_DIR = os.path.join(ROOT_DIR, ".agent", "templates")
BLUEPRINTS_DIR = os.path.join(ROOT_DIR, ".agent", "blueprints")


def extract_metadata_from_md(file_path):
    """Simple extraction of title and description from markdown frontmatter or content."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Try YAML frontmatter
        match = re.search(r"^---\s+(.*?)\s+---", content, re.DOTALL)
        if match:
            frontmatter = match.group(1)
            desc_match = re.search(r"description:\s*(.+)", frontmatter)
            description = (
                desc_match.group(1).strip() if desc_match else "No description provided"
            )
            return description

        return "No description provided"
    except Exception:
        return "Error reading file"


def generate_skill_catalog():
    skills = []
    if os.path.exists(SKILLS_DIR):
        for root, dirs, files in os.walk(SKILLS_DIR):
            if "SKILL.md" in files:
                skill_id = os.path.basename(root)
                desc = extract_metadata_from_md(os.path.join(root, "SKILL.md"))
                skills.append(
                    {
                        "id": skill_id,
                        "name": skill_id.replace("-", " ").title(),
                        "description": desc,
                        "location": f".agent/skills/{skill_id}/SKILL.md",
                    }
                )

    catalog = {
        "$schema": "../../schemas/catalog.schema.json",
        "version": "1.0.0",
        "category": "catalogs",
        "title": "Skill Catalog",
        "description": "Auto-generated catalog of all system skills",
        "metadata": {"generated": "2026-02-18"},
        "content": {"skills": skills},
    }

    with open(os.path.join(KNOWLEDGE_DIR, "skill-catalog.json"), "w") as f:
        json.dump(catalog, f, indent=2)
    print(f"Generated skill-catalog.json with {len(skills)} skills")


def generate_pattern_catalog():
    patterns = []
    if os.path.exists(PATTERNS_DIR):
        for root, dirs, files in os.walk(PATTERNS_DIR):
            for file in files:
                if file.endswith(".md"):
                    pattern_id = file.replace(".md", "")
                    desc = extract_metadata_from_md(os.path.join(root, file))
                    patterns.append(
                        {
                            "id": pattern_id,
                            "name": pattern_id.replace("-", " ").title(),
                            "description": desc,
                            "location": os.path.relpath(
                                os.path.join(root, file), ROOT_DIR
                            ).replace("\\", "/"),
                        }
                    )

    catalog = {
        "$schema": "../../schemas/catalog.schema.json",
        "version": "1.0.0",
        "category": "catalogs",
        "title": "Pattern Catalog",
        "description": "Auto-generated catalog of all system patterns",
        "metadata": {"generated": "2026-02-18"},
        "content": {"patterns": patterns},
    }

    with open(os.path.join(KNOWLEDGE_DIR, "pattern-catalog.json"), "w") as f:
        json.dump(catalog, f, indent=2)
    print(f"Generated pattern-catalog.json with {len(patterns)} patterns")


def generate_template_catalog():
    templates = []
    if os.path.exists(TEMPLATES_DIR):
        for root, dirs, files in os.walk(TEMPLATES_DIR):
            if "template.json" in files:
                try:
                    with open(os.path.join(root, "template.json"), "r") as f:
                        data = json.load(f)
                        templates.append(
                            {
                                "id": data.get("name", os.path.basename(root)),
                                "name": data.get("title", os.path.basename(root)),
                                "description": data.get(
                                    "description", "No description"
                                ),
                                "location": os.path.relpath(
                                    os.path.join(root, "template.json"), ROOT_DIR
                                ).replace("\\", "/"),
                            }
                        )
                except Exception:
                    continue

    catalog = {
        "$schema": "../../schemas/catalog.schema.json",
        "version": "1.0.0",
        "category": "catalogs",
        "title": "Template Catalog",
        "description": "Auto-generated catalog of all templates",
        "metadata": {"generated": "2026-02-18"},
        "content": {"templates": templates},
    }

    with open(os.path.join(KNOWLEDGE_DIR, "template-catalog.json"), "w") as f:
        json.dump(catalog, f, indent=2)
    print(f"Generated template-catalog.json with {len(templates)} templates")


def generate_blueprint_catalog():
    blueprints = []
    if os.path.exists(BLUEPRINTS_DIR):
        for root, dirs, files in os.walk(BLUEPRINTS_DIR):
            if "blueprint.json" in files:
                try:
                    with open(os.path.join(root, "blueprint.json"), "r") as f:
                        data = json.load(f)
                        blueprints.append(
                            {
                                "id": data.get("name", os.path.basename(root)),
                                "name": data.get("title", os.path.basename(root)),
                                "description": data.get(
                                    "description", "No description"
                                ),
                                "location": os.path.relpath(
                                    os.path.join(root, "blueprint.json"), ROOT_DIR
                                ).replace("\\", "/"),
                            }
                        )
                except Exception:
                    continue

    catalog = {
        "$schema": "../../schemas/catalog.schema.json",
        "version": "1.0.0",
        "category": "catalogs",
        "title": "Blueprint Catalog",
        "description": "Auto-generated catalog of all blueprints",
        "metadata": {"generated": "2026-02-18"},
        "content": {"blueprints": blueprints},
    }

    with open(os.path.join(KNOWLEDGE_DIR, "blueprint-catalog.json"), "w") as f:
        json.dump(catalog, f, indent=2)
    print(f"Generated blueprint-catalog.json with {len(blueprints)} blueprints")


if __name__ == "__main__":
    generate_skill_catalog()
    generate_pattern_catalog()
    generate_template_catalog()
    generate_blueprint_catalog()
