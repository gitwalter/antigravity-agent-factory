import yaml
from pathlib import Path


def extract_frontmatter(content):
    if content.startswith("---"):
        try:
            end = content.find("---", 3)
            if end != -1:
                return content[3:end], content[end + 3 :]
        except ValueError:
            pass
    return None, content


def fix_skills():
    root = Path(".agent/skills")
    if not root.exists():
        print(f"Skills root {root} does not exist!")
        return

    print(f"Fixing skills in {root}...\n")

    fixed_count = 0

    for skill_dir in root.iterdir():
        if not skill_dir.is_dir():
            continue

        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue

        content = skill_file.read_text(encoding="utf-8")
        frontmatter_str, body = extract_frontmatter(content)

        data = {}
        if frontmatter_str:
            try:
                data = yaml.safe_load(frontmatter_str) or {}
            except yaml.YAMLError:
                print(f"[SKIP] {skill_dir.name}: Invalid existing YAML")
                continue

        modified = False

        # Fix name
        if "name" not in data or data["name"] != skill_dir.name:
            data["name"] = skill_dir.name
            modified = True

        # Fix type
        if "type" not in data or data["type"] != "skill":
            data["type"] = "skill"
            modified = True

        # Fix description if missing
        if "description" not in data:
            data["description"] = (
                f"Skill for {skill_dir.name.replace('-', ' ').title()}"
            )
            modified = True

        if modified:
            new_frontmatter = yaml.dump(data, sort_keys=False).strip()
            new_content = f"---\n{new_frontmatter}\n---" + body
            skill_file.write_text(new_content, encoding="utf-8")
            print(f"[FIXED] {skill_dir.name}")
            fixed_count += 1

    print(f"\nFixed {fixed_count} skill files.")


if __name__ == "__main__":
    fix_skills()
