import os
import sys


def init_skill_bundle(skill_name, category):
    base_path = r"d:\Users\wpoga\Documents\Python Scripts\antigravity-agent-factory\.agent\skills"
    skill_path = os.path.join(base_path, category, skill_name)

    if os.path.exists(skill_path):
        print(f"ERROR: Skill {skill_name} already exists in {category}.")
        return False

    # Create structure
    os.makedirs(skill_path)
    for d in ["scripts", "references", "assets"]:
        os.makedirs(os.path.join(skill_path, d))

    # Create SKILL.md template
    md_content = f"""---
name: {skill_name}
description: Specialized skill for {skill_name.replace('-', ' ')}
type: skill
version: 1.0.0
category: {category}
agents: [ai-app-developer]
knowledge: [best-practices.json]
tools: ["none"]
related_skills: [skill-generation]
templates: ["none"]
---
# {skill_name.replace('-', ' ').title()}

## When to Use
- Describe scenarios here.

## Process
1. Step 1...
2. Step 2...
"""
    with open(os.path.join(skill_path, "SKILL.md"), "w") as f:
        f.write(md_content)

    print(f"Skill bundle '{skill_name}' initialized successfully in {category}.")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python init_skill.py <skill-name> <category>")
        sys.exit(1)
    init_skill_bundle(sys.argv[1], sys.argv[2])
