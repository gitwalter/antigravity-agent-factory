import re
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = PROJECT_ROOT / ".agent" / "knowledge"
AGENTS_DIR = PROJECT_ROOT / ".agent" / "agents"
SKILLS_DIR = PROJECT_ROOT / ".agent" / "skills"
RULES_DIR = PROJECT_ROOT / ".agent" / "rules"
WORKFLOWS_DIR = PROJECT_ROOT / ".agent" / "workflows"


def to_kebab_case(name: str) -> str:
    # Remove file extension for processin
    stem = Path(name).stem
    suffix = Path(name).suffix

    # Lowercase
    stem = stem.lower()
    # Replace any non-alphanumeric character with -
    stem = re.sub(r"[^a-z0-9]+", "-", stem)
    # Strip leading/trailing dashes
    stem = stem.strip("-")

    return f"{stem}{suffix}"


def main():
    if not KNOWLEDGE_DIR.exists():
        logger.error(f"Knowledge directory not found: {KNOWLEDGE_DIR}")
        return

    logger.info("Scanning knowledge files...")

    renames = {}

    # 1. Rename files
    for file_path in KNOWLEDGE_DIR.glob("*.json"):
        old_name = file_path.name
        new_name = to_kebab_case(old_name)

        if old_name != new_name:
            new_path = KNOWLEDGE_DIR / new_name

            if new_path.exists():
                logger.warning(
                    f"Target file {new_name} already exists. Overwriting with {old_name}..."
                )
                new_path.unlink()  # Delete existing target

            logger.info(f"Renaming: {old_name} -> {new_name}")
            try:
                file_path.rename(new_path)
                renames[old_name] = new_name
            except Exception as e:
                logger.error(f"Failed to rename {old_name}: {e}")

    if not renames:
        logger.info("No knowledge files needed renaming.")

    # 1b. Rename Rules
    if RULES_DIR.exists():
        logger.info("Scanning rules...")
        for file_path in RULES_DIR.glob("*"):
            if (
                file_path.suffix in [".json", ".yaml", ".md"]
                and file_path.name != "README.md"
            ):
                old_name = file_path.name
                new_name = to_kebab_case(old_name)
                if old_name != new_name:
                    new_path = RULES_DIR / new_name
                    if new_path.exists():
                        new_path.unlink()
                    logger.info(f"Renaming rule: {old_name} -> {new_name}")
                    file_path.rename(new_path)

    # 1c. Rename Workflows
    if WORKFLOWS_DIR.exists():
        logger.info("Scanning workflows...")
        for file_path in WORKFLOWS_DIR.glob("*"):
            if file_path.suffix in [".json", ".yaml", ".md"]:
                old_name = file_path.name
                new_name = to_kebab_case(old_name)
                if old_name != new_name:
                    new_path = WORKFLOWS_DIR / new_name
                    if new_path.exists():
                        new_path.unlink()
                    logger.info(f"Renaming workflow: {old_name} -> {new_name}")
                    file_path.rename(new_path)

    logger.info(f"Renamed {len(renames)} files. Updating references...")

    # 2. Update Agents
    if AGENTS_DIR.exists():
        for agent_file in AGENTS_DIR.glob("*.md"):
            try:
                content = agent_file.read_text(encoding="utf-8")
                new_content = content
                modified = False

                for old_name, new_name in renames.items():
                    # Check for direct filename references in links
                    # Pattern: **Label**
                    # or just Old Name.json in text

                    if old_name in new_content:
                        new_content = new_content.replace(old_name, new_name)
                        modified = True

                if modified:
                    logger.info(f"Updating references in agent: {agent_file.name}")
                    agent_file.write_text(new_content, encoding="utf-8")
            except Exception as e:
                logger.error(f"Failed to update agent {agent_file.name}: {e}")

    # 3. Update Skills (less likely but possible)
    if SKILLS_DIR.exists():
        for skill_file in SKILLS_DIR.glob("**/SKILL.md"):
            try:
                content = skill_file.read_text(encoding="utf-8")
                new_content = content
                modified = False

                for old_name, new_name in renames.items():
                    if old_name in new_content:
                        new_content = new_content.replace(old_name, new_name)
                        modified = True

                if modified:
                    logger.info(
                        f"Updating references in skill: {skill_file.relative_to(SKILLS_DIR)}"
                    )
                    skill_file.write_text(new_content, encoding="utf-8")
            except Exception as e:
                logger.error(f"Failed to update skill {skill_file.name}: {e}")

    logger.info("Fix complete.")


if __name__ == "__main__":
    main()
