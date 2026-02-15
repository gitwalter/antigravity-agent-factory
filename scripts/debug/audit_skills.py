import re
import yaml
from pathlib import Path


def extract_frontmatter(content):
    if content.startswith("---"):
        try:
            end = content.find("---", 3)
            if end != -1:
                return content[3:end]
        except ValueError:
            pass
    return None


def audit_skills():
    root = Path(".agent/skills")
    if not root.exists():
        print(f"Skills root {root} does not exist!")
        return

    print(f"Auditing skills in {root}...\n")

    for skill_dir in root.iterdir():
        if not skill_dir.is_dir():
            continue

        # Check kebab-case
        if not re.match(r"^[a-z0-9-]+$", skill_dir.name):
            print(f"[DIR NAME] {skill_dir.name}: Invalid name (must be kebab-case)")

        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            print(f"[MISSING] {skill_dir.name}: SKILL.md not found")
            continue

        content = skill_file.read_text(encoding="utf-8")
        frontmatter = extract_frontmatter(content)

        if not frontmatter:
            print(f"[FRONTMATTER] {skill_dir.name}: Missing YAML frontmatter")
            continue

        try:
            data = yaml.safe_load(frontmatter)

            # Check required fields
            if "name" not in data:
                print(f"[FIELD] {skill_dir.name}: Missing 'name'")
            elif data["name"] != skill_dir.name:
                # Handle nested exception if needed, but for now simple check
                print(
                    f"[NAME MISMATCH] {skill_dir.name}: Frontmatter name '{data['name']}' != directory '{skill_dir.name}'"
                )

            if "type" not in data:
                print(f"[FIELD] {skill_dir.name}: Missing 'type'")
            elif data["type"] != "skill":
                print(
                    f"[TYPE] {skill_dir.name}: Type is '{data['type']}', expected 'skill'"
                )

            if "description" not in data:
                print(f"[FIELD] {skill_dir.name}: Missing 'description'")

        except yaml.YAMLError as e:
            print(f"[YAML] {skill_dir.name}: Invalid YAML - {e}")


if __name__ == "__main__":
    audit_skills()
