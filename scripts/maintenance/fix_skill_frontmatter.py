from pathlib import Path
import re
import yaml


def fix_skill_frontmatter(factory_root: Path):
    skills_dir = factory_root / ".agent" / "skills"
    if not skills_dir.exists():
        print(f"Skills directory not found: {skills_dir}")
        return

    frontmatter_pattern = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

    count = 0
    print(f"Scanning skills in {skills_dir}")

    for skill_file in skills_dir.rglob("SKILL.md"):
        content = skill_file.read_text(encoding="utf-8")
        match = frontmatter_pattern.match(content)

        dir_name = skill_file.parent.name

        if match:
            fm_content = match.group(1)
            try:
                data = yaml.safe_load(fm_content) or {}
            except yaml.YAMLError:
                print(f"Invalid YAML in {skill_file}")
                continue

            updated = False

            if "name" not in data:
                data["name"] = dir_name
                updated = True

            if "type" not in data:
                data["type"] = "skill"
                updated = True

            # If description missing? Leave it for now, or use dir name

            if updated:
                new_fm = yaml.dump(data, sort_keys=False).strip()
                new_content = f"---\n{new_fm}\n---\n" + content[match.end() :]
                skill_file.write_text(new_content, encoding="utf-8")
                count += 1
                print(f"Updated {skill_file.name} in {dir_name}")
        else:
            # No frontmatter, create it
            data = {
                "name": dir_name,
                "description": f"{dir_name.replace('-', ' ').title()} skill",
                "type": "skill",
            }
            new_fm = yaml.dump(data, sort_keys=False).strip()
            new_content = f"---\n{new_fm}\n---\n\n" + content
            skill_file.write_text(new_content, encoding="utf-8")
            count += 1
            print(f"Created frontmatter for {skill_file.name} in {dir_name}")

    print(f"Fixed {count} skill files.")


if __name__ == "__main__":
    fix_skill_frontmatter(Path(__file__).parent.parent.parent)
