import os
import yaml
import json
import re

SKILLS_DIR = (
    r"d:\Users\wpoga\Documents\Python Scripts\antigravity-agent-factory\.agent\skills"
)
KNOWLEDGE_DIR = r"d:\Users\wpoga\Documents\Python Scripts\antigravity-agent-factory\.agent\knowledge"


def get_knowledge_files():
    k_files = []
    for f in os.listdir(KNOWLEDGE_DIR):
        if f.endswith(".json"):
            k_files.append(f)
    return k_files


def map_knowledge_to_skills():
    k_files = get_knowledge_files()
    skill_to_knowledge = {}

    for root, dirs, files in os.walk(SKILLS_DIR):
        if "SKILL.md" in files:
            skill_path = os.path.join(root, "SKILL.md")
            with open(skill_path, "r", encoding="utf-8") as f:
                content = f.read()

            parts = content.split("---")
            if len(parts) >= 3:
                try:
                    metadata = yaml.safe_load(parts[1])
                    skill_name = metadata.get("name")
                    if not skill_name:
                        continue

                    found_k = []
                    # Heuristic: split skill name into keywords, match against knowledge filename
                    keywords = re.split(r"[- _]", skill_name)
                    keywords = [
                        kw for kw in keywords if len(kw) > 3
                    ]  # semi-ignore short words

                    for kf in k_files:
                        match_count = sum(1 for kw in keywords if kw in kf)
                        if match_count >= 1:
                            found_k.append(kf)

                    if found_k:
                        skill_to_knowledge[skill_name] = found_k
                except Exception:
                    pass
    return skill_to_knowledge


if __name__ == "__main__":
    mapping = map_knowledge_to_skills()
    print(json.dumps(mapping, indent=2))
