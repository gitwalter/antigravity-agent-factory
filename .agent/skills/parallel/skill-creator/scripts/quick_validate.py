import os
import re
import yaml
import sys


def validate_skill(skill_path):
    skill_md_path = os.path.join(skill_path, "SKILL.md")
    if not os.path.exists(skill_md_path):
        return False, f"Missing SKILL.md in {skill_path}"

    with open(skill_md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check for YAML frontmatter
    match = re.search(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return False, "Missing or invalid YAML frontmatter"

    try:
        frontmatter = yaml.safe_load(match.group(1))
    except yaml.YAMLError as e:
        return False, f"YAML parse error: {e}"

    # Validate Name
    name = frontmatter.get("name")
    if not name:
        return False, "Missing 'name' in frontmatter"
    if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", name):
        return False, f"Invalid name format '{name}'. Must be hyphen-case."
    if len(name) > 64:
        return False, f"Name '{name}' exceeds 64 characters."

    # Validate Description
    description = frontmatter.get("description")
    if not description:
        return False, "Missing 'description' in frontmatter"
    if len(description) > 1024:
        return False, "Description exceeds 1024 characters."
    if "<" in description or ">" in description:
        return False, "Description contains prohibited angle brackets."

    # Validate Body Length (Level 2)
    body = content[match.end() :]
    lines = body.splitlines()
    if len(lines) > 500:
        return False, f"SKILL.md body exceeds 500 line limit ({len(lines)} lines)."

    return True, "Skill structure is valid."


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python quick_validate.py <skill_directory_path>")
        sys.exit(1)

    success, msg = validate_skill(sys.argv[1])
    print(msg)
    sys.exit(0 if success else 1)
