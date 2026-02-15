import os
import re
from pathlib import Path

ROOT_DIR = Path("d:/Users/wpoga/Documents/Python Scripts/antigravity-agent-factory")
DOCS_DIR = ROOT_DIR / "docs"

# Definitive Repair Map: {CurrentFunnyName: CorrectName}
REPAIR_MAP = {
    # Squashed names to proper kebab-case
    "factory-automation.md": "factory-automation.md",
    "society-integration-guide.md": "society-integration-guide.md",
    "trust-tier-selection.md": "trust-tier-selection.md",
    "external-resources.md": "external-resources.md",
    "factory-components.md": "factory-components.md",
    "generated-output.md": "generated-output.md",
    "guardian-coordination.md": "guardian-coordination.md",
    "knowledge-files.md": "knowledge-files.md",
    "workflow-patterns.md": "workflow-patterns.md",
    # Ensure high-level ones remain/become CAPITAL_CASE
    "BLUEPRINTS.md": "BLUEPRINTS.md",
    "CATALOG.md": "CATALOG.md",
    "PATTERNS.md": "PATTERNS.md",
    "TEMPLATES.md": "TEMPLATES.md",
    "google-agent-sdk.md": "google-agent-sdk.md",
    "mcp-installation-guide.md": "mcp-installation-guide.md",
}

# Add Lesson files mappings
for i in range(1, 19):
    REPAIR_MAP[f"l{i}.md"] = (
        f"l{i}.md"  # placeholder if needed, but they are already kebab-ish
    )


def rename_and_sync():
    # 1. Collect all .md files in docs/ and build the final mapping
    final_rename_map = {}

    # Pre-populate with our explicit repairs
    for k, v in REPAIR_MAP.items():
        final_rename_map[k] = v

    print("Executing final renaming and sync...")

    # Renaming execution
    for root, _, files in os.walk(DOCS_DIR):
        for f in files:
            if f in final_rename_map:
                old_path = Path(root) / f
                new_path = Path(root) / final_rename_map[f]
                if old_path != new_path:
                    print(f"  RENAME: {f} -> {final_rename_map[f]}")
                    if os.path.exists(new_path):
                        os.remove(new_path)  # Avoid conflict
                    os.rename(old_path, new_path)

    # Reference synchronization
    extensions = {".md", ".json", ".yaml", ".yml", ".py", ".js", ".ts"}
    ignore_dirs = {
        ".git",
        ".venv",
        "node_modules",
        ".pytest_cache",
        ".ruff_cache",
        "__pycache__",
        "tmp",
        ".gemini",
    }

    print("Updating all references across codebase...")
    for root, dirs, files in os.walk(ROOT_DIR):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for f in files:
            if os.path.splitext(f)[1] in extensions:
                file_path = Path(root) / f
                try:
                    content = file_path.read_text(encoding="utf-8", errors="ignore")
                    modified = False
                    for old, new in final_rename_map.items():
                        if old != new and old in content:
                            # Use word boundaries and ensure we aren't matching inside a larger word
                            pattern = rf"(?<![a-zA-Z0-9_\-/]){re.escape(old)}"
                            if re.search(pattern, content):
                                content = re.sub(pattern, new, content)
                                modified = True

                    if modified:
                        print(f"    FIXED: {file_path.relative_to(ROOT_DIR)}")
                        file_path.write_text(content, encoding="utf-8")
                except Exception as e:
                    print(f"    ERROR: {f}: {e}")


if __name__ == "__main__":
    rename_and_sync()
