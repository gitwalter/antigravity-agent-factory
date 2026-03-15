import os
import yaml
import json
from pathlib import Path

SKILLS_DIR = Path(
    "d:/Users/wpoga/Documents/Python Scripts/antigravity-agent-factory/.agent/skills"
)


def fill_gaps():
    updated_count = 0
    for skill_md in SKILLS_DIR.rglob("SKILL.md"):
        try:
            with open(skill_md, "r", encoding="utf-8") as f:
                content = f.read()

            parts = content.split("---")
            if len(parts) < 3:
                continue

            metadata = yaml.safe_load(parts[1])
            changed = False

            # Fill agents gap
            if (
                "agents" not in metadata
                or not metadata["agents"]
                or metadata["agents"] == ["none"]
                or metadata["agents"] == [None]
            ):
                metadata["agents"] = ["python-ai-specialist"]
                changed = True

            # Fill knowledge gap
            if (
                "knowledge" not in metadata
                or not metadata["knowledge"]
                or metadata["knowledge"] == [None]
            ):
                metadata["knowledge"] = ["none"]
                changed = True

            # Fill templates gap
            if (
                "templates" not in metadata
                or not metadata["templates"]
                or metadata["templates"] == [None]
            ):
                metadata["templates"] = ["none"]
                changed = True

            # Fill related_skills gap
            if (
                "related_skills" not in metadata
                or not metadata["related_skills"]
                or metadata["related_skills"] == [None]
            ):
                metadata["related_skills"] = [
                    "managing-plane-tasks",
                    "orchestrating-mcp",
                ]
                changed = True

            if changed:
                # Re-write the frontmatter
                # We do not use default_flow_style=False blindly because we want lists to be either block or flow depending on how yaml dumps it natively, usually block is fine.
                new_frontmatter = yaml.dump(
                    metadata, sort_keys=False, default_flow_style=False
                )
                new_content = f"---\n{new_frontmatter}---" + "".join(parts[2:])

                with open(skill_md, "w", encoding="utf-8") as f:
                    f.write(new_content)
                updated_count += 1
                print(f"Filled gaps for {skill_md.relative_to(SKILLS_DIR)}")

        except Exception as e:
            print(f"Error processing {skill_md}: {e}")

    print(f"\nTotal skills updated: {updated_count}")


if __name__ == "__main__":
    fill_gaps()
