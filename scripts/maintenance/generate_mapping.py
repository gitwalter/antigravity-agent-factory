import os

KNOWLEDGE_PATH = r"d:\Users\wpoga\Documents\Python Scripts\antigravity-agent-factory\.agent\knowledge"
SKILLS_ROOT = (
    r"d:\Users\wpoga\Documents\Python Scripts\antigravity-agent-factory\.agent\skills"
)


def get_mapping():
    knowledge_files = [f for f in os.listdir(KNOWLEDGE_PATH) if f.endswith(".json")]
    skills = []
    for root, dirs, files in os.walk(SKILLS_ROOT):
        if "SKILL.md" in files:
            skills.append((root, os.path.basename(root)))

    mapping = {}
    for k_file in knowledge_files:
        k_base = (
            k_file.replace(".json", "")
            .replace("-patterns", "")
            .replace("-knowledge", "")
            .replace("-patterns-2026", "")
            .lower()
        )
        # Basic fuzzy match
        for s_path, skill in skills:
            s_name = (
                skill.lower()
                .replace("-development", "")
                .replace("-management", "")
                .replace("-integration", "")
                .replace("-usage", "")
            )
            if k_base in s_name or s_name in k_base:
                if s_path not in mapping:
                    mapping[s_path] = []
                mapping[s_path].append(k_file)

    # Sort by number of files found to see gaps
    for s_path in sorted(mapping.keys()):
        print(f"Skill: {os.path.basename(s_path)} -> {mapping[s_path]}")

    # Identify gaps
    all_skill_paths = [s[0] for s in skills]
    gaps = [s for s in all_skill_paths if s not in mapping]
    print(f"\nFound {len(gaps)} skills with no matching knowledge file.")
    for g in gaps:
        print(f"GAP: {os.path.basename(g)}")


if __name__ == "__main__":
    get_mapping()
