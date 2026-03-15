import json
import os

CATALOG_PATH = r"d:\Users\wpoga\Documents\Python Scripts\antigravity-agent-factory\.agent\knowledge\skill-catalog.json"
SKILLS_ROOT = (
    r"d:\Users\wpoga\Documents\Python Scripts\antigravity-agent-factory\.agent\skills"
)


def sync_catalog():
    if not os.path.exists(CATALOG_PATH):
        print(f"ERROR: Catalog not found at {CATALOG_PATH}")
        return

    with open(CATALOG_PATH, "r") as f:
        catalog = json.load(f)

    # Map physical skills
    physical_map = {}
    for pattern in os.listdir(SKILLS_ROOT):
        pattern_path = os.path.join(SKILLS_ROOT, pattern)
        if not os.path.isdir(pattern_path):
            continue
        for skill in os.listdir(pattern_path):
            physical_map[skill] = f"{pattern}/{skill}"

    # Update catalog
    updated = 0
    if "skills" in catalog:
        for skill_id, skill_meta in catalog["skills"].items():
            if skill_id in physical_map:
                new_path = f"{{directories.skills}}/{physical_map[skill_id]}/SKILL.md"
                # Update both factorySkill and factoryPattern as both are used for pathing
                if (
                    "factorySkill" in skill_meta
                    and skill_meta["factorySkill"] != new_path
                ):
                    skill_meta["factorySkill"] = new_path
                    updated += 1
                if (
                    "factoryPattern" in skill_meta
                    and skill_meta["factoryPattern"] != new_path
                ):
                    skill_meta["factoryPattern"] = new_path
                    updated += 1

    with open(CATALOG_PATH, "w") as f:
        json.dump(catalog, f, indent=4)

    print(f"Catalog synchronization complete: {updated} paths updated.")


if __name__ == "__main__":
    sync_catalog()
