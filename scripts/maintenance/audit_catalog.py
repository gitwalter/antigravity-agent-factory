import os
import json

SKILLS_ROOT = (
    r"d:\Users\wpoga\Documents\Python Scripts\antigravity-agent-factory\.agent\skills"
)
CATALOG_PATH = r"d:\Users\wpoga\Documents\Python Scripts\antigravity-agent-factory\.agent\knowledge\skill-catalog.json"


def audit_catalog():
    with open(CATALOG_PATH, "r") as f:
        catalog = json.load(f)

    catalog_skills = catalog.get("skills", {})
    all_registered = []
    for cat in catalog_skills.values():
        if isinstance(cat, dict) and "id" in cat:
            all_registered.append(cat["id"])
        elif isinstance(cat, dict):
            all_registered.extend(cat.keys())

    missing_in_catalog = []
    for root, dirs, files in os.walk(SKILLS_ROOT):
        if "SKILL.md" in files:
            skill_id = os.path.basename(root)
            if skill_id not in all_registered:
                missing_in_catalog.append((skill_id, root))

    print(
        f"Total skills on disk: {len([r for r,d,f in os.walk(SKILLS_ROOT) if 'SKILL.md' in f])}"
    )
    print(f"Total skills in catalog: {len(all_registered)}")
    print(f"Skills on disk BUT NOT in catalog: {len(missing_in_catalog)}")
    for s_id, path in missing_in_catalog:
        print(f"MISSING: {s_id} ({path})")


if __name__ == "__main__":
    audit_catalog()
