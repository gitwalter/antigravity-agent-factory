import os
import shutil
import json
import re

KNOWLEDGE_PATH = r"d:\Users\wpoga\Documents\Python Scripts\antigravity-agent-factory\.agent\knowledge"
SKILLS_ROOT = (
    r"d:\Users\wpoga\Documents\Python Scripts\antigravity-agent-factory\.agent\skills"
)


def aggressive_migrate():
    knowledge_files = [f for f in os.listdir(KNOWLEDGE_PATH) if f.endswith(".json")]
    skills = []
    for root, dirs, files in os.walk(SKILLS_ROOT):
        if "SKILL.md" in files:
            skills.append((root, os.path.basename(root)))

    migrations = 0

    # Process knowledge mapping
    for k_file in knowledge_files:
        # Normalize knowledge name: remove extension, common suffixes, etc.
        k_norm = k_file.replace(".json", "").lower()
        k_norm = re.sub(
            r"(-patterns|-knowledge|-reference|-patterns-2026|-best-practices)$",
            "",
            k_norm,
        )
        k_norm = k_norm.replace("-", "")

        for s_path, skill in skills:
            # Normalize skill name
            s_norm = skill.lower()
            s_norm = re.sub(
                r"(-development|-management|-integration|-usage|-ops|-engineering)$",
                "",
                s_norm,
            )
            s_norm = s_norm.replace("-", "")
            s_norm = re.sub(r"s$", "", s_norm)  # Plural

            # Match logic: substring or reverse substring
            if k_norm in s_norm or s_norm in k_norm:
                src = os.path.join(KNOWLEDGE_PATH, k_file)
                dst_dir = os.path.join(s_path, "references")
                os.makedirs(dst_dir, exist_ok=True)
                dst = os.path.join(dst_dir, k_file)
                if not os.path.exists(dst):
                    print(f"Migrating {k_file} -> {skill}")
                    shutil.copy2(src, dst)
                    migrations += 1

    # Second pass: Category based migration for specific known globas
    category_map = {
        "sap": ["sap-", "cds-", "rap-", "fiori-"],
        "dotnet": ["dotnet-", "ef-core", "blazor"],
        "python": ["python-", "fastapi", "sqlalchemy"],
        "agent": ["agent-", "workflow-", "mcp-"],
    }

    for category, prefixes in category_map.items():
        for k_file in knowledge_files:
            if any(k_file.startswith(p) for p in prefixes):
                for s_path, skill in skills:
                    if category in s_path.lower():
                        dst_dir = os.path.join(s_path, "references")
                        os.makedirs(dst_dir, exist_ok=True)
                        dst = os.path.join(dst_dir, k_file)
                        if not os.path.exists(dst):
                            shutil.copy2(os.path.join(KNOWLEDGE_PATH, k_file), dst)
                            migrations += 1

    print(f"Aggressive Migration complete: {migrations} total files localized.")


if __name__ == "__main__":
    aggressive_migrate()
