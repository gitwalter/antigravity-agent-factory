import os
from pathlib import Path

ROOT_DIR = Path("d:/Users/wpoga/Documents/Python Scripts/antigravity-agent-factory")

# Define all moves (current path from root -> new path from root)
MOVE_MAP = {
    # Docs reorganization (already done partially, but ensuring completeness)
    "docs/architecture/asp-value-proposition.md": "docs/architecture/asp-value-proposition.md",
    "docs/architecture/blueprint-version-management.md": "docs/architecture/blueprint-version-management.md",
    "docs/architecture/system-blueprint.md": "docs/architecture/system-blueprint.md",
    "docs/architecture/google-agent-sdk.md": "docs/architecture/google-agent-sdk.md",
    "docs/setup/configuration.md": "docs/setup/configuration.md",
    "docs/setup/installation.md": "docs/setup/installation.md",
    "docs/setup/mcp-installation-guide.md": "docs/setup/mcp-installation-guide.md",
    "docs/guides/extension-guide.md": "docs/guides/extension-guide.md",
    "docs/guides/getting-started.md": "docs/guides/getting-started.md",
    "docs/guides/quickstart.md": "docs/guides/quickstart.md",
    "docs/guides/troubleshooting.md": "docs/guides/troubleshooting.md",
    "docs/guides/user-guide.md": "docs/guides/user-guide.md",
    "docs/testing/test-catalog.md": "docs/testing/test-catalog.md",
    "docs/testing/testing.md": "docs/testing/testing.md",
    # Scripts reorganization
    "mcp/scripts/find_contact_email.py": "mcp/scripts/find_contact_email.py",
    "scripts/validation/fix_all_schemas.py": "scripts/validation/fix_all_schemas.py",
    "scripts/maintenance/fix_artifact_naming.py": "scripts/maintenance/fix_artifact_naming.py",
    "scripts/core/import_bundle.py": "scripts/core/import_bundle.py",
    "mcp/scripts/send_draft_email.py": "mcp/scripts/send_draft_email.py",
    "mcp/scripts/send_gmail.py": "mcp/scripts/send_gmail.py",
    "scripts/validation/verify_workflow_org.py": "scripts/validation/verify_workflow_org.py",
}


def reorganize_project():
    sync_map = {}  # old_string -> new_string

    print("Executing moves...")
    for old_rel, new_rel in MOVE_MAP.items():
        old_path = ROOT_DIR / old_rel
        new_path = ROOT_DIR / new_rel

        if old_path.exists() and old_path != new_path:
            new_path.parent.mkdir(parents=True, exist_ok=True)
            print(f"  MOVE: {old_rel} -> {new_rel}")
            if new_path.exists():
                os.remove(new_path)
            os.rename(old_path, new_path)

            # Map for string replacement
            sync_map[old_rel] = new_rel
            # Also map basename for some cases, but carefully
            old_base = os.path.basename(old_rel)
            new_base = os.path.basename(new_rel)
            if old_base != new_base:
                sync_map[old_base] = new_base
            # If it's a script, it might be called via 'python scripts/...'
            # We already have the full path covered.
        else:
            # Even if file doesn't exist (already moved), we want the sync mapping
            sync_map[old_rel] = new_rel

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
                        # Case 1: Full relative path from root
                        if old in content:
                            content = content.replace(old, new)
                            modified = True

                        # Case 2: Handle PowerShell backslashes if any
                        old_bs = old.replace("/", "\\")
                        new_bs = new.replace("/", "\\")
                        if old_bs in content:
                            content = content.replace(old_bs, new_bs)
                            modified = True

                    if modified:
                        print(f"    Synced: {file_path.relative_to(ROOT_DIR)}")
                        file_path.write_text(content, encoding="utf-8")
                except Exception as e:
                    print(f"    Error in {f}: {e}")


if __name__ == "__main__":
    reorganize_project()
