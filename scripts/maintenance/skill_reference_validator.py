#!/usr/bin/env python3
"""
skill_reference_validator.py
Automated auditor for .agent/skills/ reference integrity.
Verifies that all scripts referenced in skills exist on the filesystem.
"""

import os
import re
import sys
from pathlib import Path


def validate_skills(root_dir):
    skills_dir = Path(root_dir) / ".agent" / "skills"
    scripts_dir = Path(root_dir) / "scripts"

    if not skills_dir.exists():
        print(f"Error: Skills directory not found at {skills_dir}")
        return False

    broken_refs = []
    total_skills = 0
    total_refs = 0

    # Pattern for script references in tools and Best Commands sections
    # Matches: scripts/path/to/script.py or script_name.py
    script_pattern = re.compile(r"scripts/[\w/-]+\.py|[\w-]+\.py")

    for skill_file in skills_dir.rglob("*.md"):
        total_skills += 1
        with open(skill_file, "r", encoding="utf-8") as f:
            content = f.read()

            # Find all potential script references
            matches = script_pattern.findall(content)
            for match in matches:
                total_refs += 1
                # Normalize path
                if match.startswith("scripts/"):
                    script_path = Path(root_dir) / match
                else:
                    # Search for the script in the scripts directory if only filename provided
                    # This is a bit looser but common in "commands" sections
                    search_results = list(scripts_dir.rglob(match))
                    if search_results:
                        script_path = search_results[0]
                    else:
                        script_path = (
                            scripts_dir / match
                        )  # Placeholder for error reporting

                if not script_path.exists():
                    broken_refs.append(
                        {
                            "skill": str(skill_file.relative_to(root_dir)),
                            "reference": match,
                            "line": content.count("\n", 0, content.find(match)) + 1,
                        }
                    )

    # Report results
    print("--- Skill Reference Audit ---")
    print(f"Skills Scanned: {total_skills}")
    print(f"References Checked: {total_refs}")

    if broken_refs:
        print(f"\nFound {len(broken_refs)} Broken References:")
        for ref in broken_refs:
            print(
                f"  [!] {ref['skill']}:{ref['line']} -> {ref['reference']} (NOT FOUND)"
            )
        return False
    else:
        print("\n[+] All skill references are valid.")
        return True


if __name__ == "__main__":
    root = Path(__file__).parent.parent.parent
    success = validate_skills(root)
    sys.exit(0 if success else 1)
