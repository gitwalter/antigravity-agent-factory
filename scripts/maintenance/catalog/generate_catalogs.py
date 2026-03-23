import os
import json
import re

ROOT_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
KNOWLEDGE_DIR = os.path.join(ROOT_DIR, ".agent", "knowledge")
SKILLS_DIR = os.path.join(ROOT_DIR, ".agent", "skills")
PATTERNS_DIR = os.path.join(ROOT_DIR, ".agent", "patterns")
TEMPLATES_DIR = os.path.join(ROOT_DIR, ".agent", "templates")
BLUEPRINTS_DIR = os.path.join(ROOT_DIR, ".agent", "blueprints")
WORKFLOWS_DIR = os.path.join(ROOT_DIR, ".agent", "workflows")
RULES_DIR = os.path.join(ROOT_DIR, ".agent", "rules")


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

    with open(os.path.join(KNOWLEDGE_DIR, "core", "skill-catalog.json"), "w") as f:
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

    with open(os.path.join(KNOWLEDGE_DIR, "core", "pattern-catalog.json"), "w") as f:
        json.dump(catalog, f, indent=2)
    print(f"Generated pattern-catalog.json with {len(patterns)} patterns")


def generate_template_catalog():
    templates = []
    if os.path.exists(TEMPLATES_DIR):
        for root, dirs, files in os.walk(TEMPLATES_DIR):
            for file in files:
                if file.endswith(".tmpl") or file.endswith(".j2"):
                    # Check if template.json exists in the same directory for metadata
                    template_id = file
                    template_name = (
                        file.replace(".tmpl", "")
                        .replace(".j2", "")
                        .replace("-", " ")
                        .title()
                    )
                    description = "Template file"

                    if "template.json" in files:
                        try:
                            with open(os.path.join(root, "template.json"), "r") as f:
                                data = json.load(f)
                                template_id = data.get("name", template_id)
                                template_name = data.get("title", template_name)
                                description = data.get("description", description)
                        except Exception:
                            pass

                    templates.append(
                        {
                            "id": template_id,
                            "name": template_name,
                            "description": description,
                            "location": os.path.relpath(
                                os.path.join(root, file), ROOT_DIR
                            ).replace("\\", "/"),
                        }
                    )

    catalog = {
        "$schema": "../../schemas/catalog.schema.json",
        "version": "1.0.0",
        "category": "catalogs",
        "title": "Template Catalog",
        "description": "Auto-generated catalog of all templates",
        "metadata": {"generated": "2026-02-18"},
        "content": {"templates": templates},
    }

    with open(os.path.join(KNOWLEDGE_DIR, "core", "template-catalog.json"), "w") as f:
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

    with open(
        os.path.join(KNOWLEDGE_DIR, "integration", "blueprint-catalog.json"), "w"
    ) as f:
        json.dump(catalog, f, indent=2)
    print(f"Generated blueprint-catalog.json with {len(blueprints)} blueprints")


def generate_workflow_catalog():
    workflows = []
    if os.path.exists(WORKFLOWS_DIR):
        for root, dirs, files in os.walk(WORKFLOWS_DIR):
            for file in files:
                if file.endswith(".md"):
                    workflow_id = file.replace(".md", "")
                    # Extract description from frontmatter or first line
                    desc = extract_metadata_from_md(os.path.join(root, file))
                    workflows.append(
                        {
                            "id": workflow_id,
                            "name": workflow_id.replace("-", " ").title(),
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
        "title": "Workflow Catalog",
        "description": "Auto-generated catalog of all system workflows",
        "metadata": {"generated": "2026-02-18"},
        "content": {"workflows": workflows},
    }

    with open(os.path.join(KNOWLEDGE_DIR, "core", "workflow-catalog.json"), "w") as f:
        json.dump(catalog, f, indent=2)
    print(f"Generated workflow-catalog.json with {len(workflows)} workflows")


def generate_rule_catalog():
    rules = []
    if os.path.exists(RULES_DIR):
        for root, dirs, files in os.walk(RULES_DIR):
            for file in files:
                if file.endswith(".md"):
                    rule_id = file.replace(".md", "")
                    desc = extract_metadata_from_md(os.path.join(root, file))
                    rules.append(
                        {
                            "id": rule_id,
                            "name": rule_id.replace("-", " ").title(),
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
        "title": "Rule Catalog",
        "description": "Auto-generated catalog of all system rules",
        "metadata": {"generated": "2026-02-18"},
        "content": {"rules": rules},
    }

    with open(os.path.join(KNOWLEDGE_DIR, "core", "rule-catalog.json"), "w") as f:
        json.dump(catalog, f, indent=2)
    print(f"Generated rule-catalog.json with {len(rules)} rules")


if __name__ == "__main__":
    generate_skill_catalog()
    generate_pattern_catalog()
    generate_template_catalog()
    generate_blueprint_catalog()
    generate_workflow_catalog()
    generate_rule_catalog()
