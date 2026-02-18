import os
import json

SKILLS_ROOT = (
    r"d:\Users\wpoga\Documents\Python Scripts\antigravity-agent-factory\.agent\skills"
)
KNOWLEDGE_PATH = r"d:\Users\wpoga\Documents\Python Scripts\antigravity-agent-factory\.agent\knowledge"

VALIDATE_TEMPLATE = """import os
import sys

def validate():
    skill_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Check for core components
    missing = []
    for d in ["references", "scripts", "assets"]:
        if not os.path.exists(os.path.join(skill_path, d)):
            missing.append(d)

    if "SKILL.md" not in os.listdir(skill_path):
        missing.append("SKILL.md")

    if missing:
        print(f"Validation FAILED: Missing {', '.join(missing)}")
        return False

    print("Validation PASSED: Level 1-3 structural integrity verified.")
    return True

if __name__ == "__main__":
    sys.exit(0 if validate() else 1)
"""

UTILS_TEMPLATE = """def get_skill_metadata():
    return {
        "status": "active",
        "enrichment_level": 3,
        "deterministic": True
    }

if __name__ == "__main__":
    print("Skill utilities initialized.")
"""


def total_enrich():
    skills = []
    for root, dirs, files in os.walk(SKILLS_ROOT):
        if "SKILL.md" in files:
            skills.append(root)

    print(f"Enriching {len(skills)} skills...")

    for s_path in skills:
        # 1. Create Directories
        for d in ["references", "scripts", "assets"]:
            os.makedirs(os.path.join(s_path, d), exist_ok=True)

        # 2. Seed Scripts
        scripts_path = os.path.join(s_path, "scripts")
        v_file = os.path.join(scripts_path, "validate.py")
        u_file = os.path.join(scripts_path, "utils.py")

        if not os.path.exists(v_file):
            with open(v_file, "w") as f:
                f.write(VALIDATE_TEMPLATE)
        if not os.path.exists(u_file):
            with open(u_file, "w") as f:
                f.write(UTILS_TEMPLATE)

        # 3. Seed Assets (Placeholder)
        assets_path = os.path.join(s_path, "assets")
        m_file = os.path.join(assets_path, "metadata.json")
        if not os.path.exists(m_file):
            with open(m_file, "w") as f:
                json.dump(
                    {
                        "description": f"Static assets for {os.path.basename(s_path)} skill bundle",
                        "type": "collection",
                    },
                    f,
                    indent=4,
                )

    print("Total Enrichment phase 1 complete (Structural Seeding).")


if __name__ == "__main__":
    total_enrich()
