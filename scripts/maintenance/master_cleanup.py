import os
import re
from pathlib import Path

ROOT_DIR = Path("d:/Users/wpoga/Documents/Python Scripts/antigravity-agent-factory")
DOCS_DIR = ROOT_DIR / "docs"

IMPORTANT_DOCS = {
    "README.md",
    "QUICKSTART.md",
    "CHANGELOG.md",
    "LICENSE.md",
    "SYSTEM_BLUEPRINT.md",
    "BLUEPRINT_VERSION_MANAGEMENT.md",
    "GETTING_STARTED.md",
    "CONFIGURATION.md",
    "INSTALLATION.md",
    "TESTING.md",
    "USER_GUIDE.md",
    "TROUBLESHOOTING.md",
    "ASP_VALUE_PROPOSITION.md",
    "EXTENSION_GUIDE.md",
    "TEST_CATALOG.md",
}


def clean_name(name):
    base, ext = os.path.splitext(name)
    if ext != ".md":
        return name

    # 1. Handle aggressive hyphenation
    # Replace any sequence of a-b-c with abc
    # This also handles cases with underscores or multiple hyphens
    # Goal: society-integration-guide instead of s-o-c-i-e-t-y

    # Remove hyphens between single characters
    cleaned = base
    while True:
        # Match a single char, optional hyphen/underscore, single char
        # e.g. f-a or y-_-a
        match = re.search(r"([a-zA-Z])[-_]+([a-zA-Z])", cleaned)
        if not match:
            break

        # If it's single letter - single letter, join them
        # BUT wait, we need to know if it's a word boundary.
        # Let's just join ALL single letters.
        # "f-a-c-t-o-r-y" -> "factory"
        # "factory-automation" -> "factoryautomation" (oops, but we can fix that)

        # New approach: only join if it looks like a sequence
        if re.search(r"([a-zA-Z]-){2,}", cleaned):
            cleaned = re.sub(r"([a-zA-Z])-([a-zA-Z])", r"\1\2", cleaned)
        else:
            break

    # Remove underscores from previous script mess
    cleaned = cleaned.replace("_", "-")
    # Remove multiple hyphens
    cleaned = re.sub(r"-+", "-", cleaned).strip("-")

    # 2. Apply convention
    if cleaned.upper() + ext in (s.upper() for s in IMPORTANT_DOCS):
        # Find the exact original casing if possible, or just use UPPER
        return cleaned.upper() + ext

    # Turn everything else into proper kebab-case
    # "FactoryAutomation" -> "factory-automation"
    kebab = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", cleaned)
    kebab = kebab.lower().replace("_", "-")
    kebab = re.sub(r"-+", "-", kebab).strip("-")

    return kebab + ext


# Mapping for the known bad ones to be safe
MANUAL_FIXES = {
    "factory-automation.md": "factory-automation.md",
    "society-integration-guide.md": "society-integration-guide.md",
    "trust-tier-selection.md": "trust-tier-selection.md",
    "externalresources.md": "external-resources.md",
    "factorycomponents.md": "factory-components.md",
    "generatedoutput.md": "generated-output.md",
    "guardiancoordination.md": "guardian-coordination.md",
    "knowledgefiles.md": "knowledge-files.md",
    "workflowpatterns.md": "workflow-patterns.md",
}


def master_repair():
    full_rename_map = {}

    print("Scanning for files to repair...")
    # 1. Check DOCS_DIR
    for root, _, files in os.walk(DOCS_DIR):
        for f in files:
            if not f.endswith(".md"):
                continue
            target = clean_name(f)
            if f in MANUAL_FIXES:
                target = MANUAL_FIXES[f]
            if f != target:
                full_rename_map[os.path.join(root, f)] = os.path.join(root, target)

    # 2. Check ROOT_DIR for root-specific special files
    # We want these to be exactly like this
    ROOT_CAPS = {"README.md", "CHANGELOG.md", "LICENSE", ".agentrules"}
    for f in os.listdir(ROOT_DIR):
        if f.upper() in {s.upper() for s in ROOT_CAPS}:
            target = next(s for s in ROOT_CAPS if s.upper() == f.upper())
            if f != target:
                full_rename_map[os.path.join(ROOT_DIR, f)] = os.path.join(
                    ROOT_DIR, target
                )

    if not full_rename_map:
        print("No files found that need renaming.")
    else:
        print(f"Executing {len(full_rename_map)} renames...")
        for old, new in full_rename_map.items():
            old_p, new_p = Path(old), Path(new)
            if old_p.name.lower() == new_p.name.lower() and old_p.name != new_p.name:
                # Case-only rename on Windows
                temp = os.path.join(os.path.dirname(old), old_p.name + ".tmp_rename")
                if os.path.exists(temp):
                    os.remove(temp)
                os.rename(old, temp)
                os.rename(temp, new)
                print(f"  {old_p.name} -> {new_p.name} (case-only)")
            else:
                print(f"  {old_p.name} -> {new_p.name}")
                if os.path.exists(new) and old != new:
                    os.remove(new)
                os.rename(old, new)

    # Global reference update
    sync_map = {
        "factory-automation.md": "factory-automation.md",
        "society-integration-guide.md": "society-integration-guide.md",
        "trust-tier-selection.md": "trust-tier-selection.md",
        "factory-automation.md": "factory-automation.md",
        "society-integration-guide.md": "society-integration-guide.md",
        "trust-tier-selection.md": "trust-tier-selection.md",
    }

    # Add all renames we just performed to the sync map (basename only)
    for old, new in full_rename_map.items():
        sync_map[os.path.basename(old)] = os.path.basename(new)

    print("Updating references repository-wide...")
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

    # Pre-process sync_map to avoid circularity and prioritize longest
    sorted_items = sorted(sync_map.items(), key=lambda x: len(x[0]), reverse=True)

    for root, dirs, files in os.walk(ROOT_DIR):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for f in files:
            if os.path.splitext(f)[1] in extensions:
                file_path = Path(root) / f
                try:
                    content = file_path.read_text(encoding="utf-8", errors="ignore")
                    modified = False
                    for old, new in sorted_items:
                        if old != new and old in content:
                            content = content.replace(old, new)
                            modified = True
                    if modified:
                        print(f"    Synced: {file_path.relative_to(ROOT_DIR)}")
                        file_path.write_text(content, encoding="utf-8")
                except Exception as e:
                    print(f"    Error: {f}: {e}")


if __name__ == "__main__":
    master_repair()
