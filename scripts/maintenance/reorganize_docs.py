import os
from pathlib import Path

ROOT_DIR = Path("d:/Users/wpoga/Documents/Python Scripts/antigravity-agent-factory")
DOCS_DIR = ROOT_DIR / "docs"

# Define the move map (current basename -> new relative path from docs/)
MOVE_MAP = {
    "asp-value-proposition.md": "architecture/asp-value-proposition.md",
    "blueprint-version-management.md": "architecture/blueprint-version-management.md",
    "system-blueprint.md": "architecture/system-blueprint.md",
    "google-agent-sdk.md": "architecture/google-agent-sdk.md",
    "configuration.md": "setup/configuration.md",
    "installation.md": "setup/installation.md",
    "mcp-installation-guide.md": "setup/mcp-installation-guide.md",
    "extension-guide.md": "guides/extension-guide.md",
    "getting-started.md": "guides/getting-started.md",
    "quickstart.md": "guides/quickstart.md",
    "troubleshooting.md": "guides/troubleshooting.md",
    "user-guide.md": "guides/user-guide.md",
    "test-catalog.md": "testing/test-catalog.md",
    "testing.md": "testing/testing.md",
}


def reorganize_docs():
    sync_map = {}  # old_path_from_root -> new_path_from_root (for string replacement)

    print("Preparing reorganization...")
    for filename, rel_target in MOVE_MAP.items():
        old_path = DOCS_DIR / filename
        if old_path.exists():
            new_path = DOCS_DIR / rel_target
            new_path.parent.mkdir(parents=True, exist_ok=True)

            # Record for sync
            old_rel = f"docs/{filename}"
            new_rel = f"docs/{rel_target}"
            sync_map[old_rel] = new_rel

            # Also record the variant without docs/ prefix for relative links if they exist
            sync_map[filename] = os.path.basename(
                rel_target
            )  # This is risky, only for basenames if it's unique

            print(f"  MOVE: {old_rel} -> {new_rel}")
            if os.path.exists(new_path):
                os.remove(new_path)
            os.rename(old_path, new_path)

    if not sync_map:
        print("No files to reorganize.")
        return

    print("Updating references repository-wide...")
    # Extensions to search in
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

    # Sort by length descending to avoid partial replacements
    sorted_items = sorted(sync_map.items(), key=lambda x: len(x[0]), reverse=True)

    for root, dirs, files in os.walk(ROOT_DIR):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for f in files:
            if os.path.splitext(f)[1] in extensions:
                file_path = Path(root) / f
                try:
                    content = file_path.read_text(encoding="utf-8", errors="ignore")
                    modified = False

                    # Special handling for local relative links in docs
                    # e.g. [Installation](../../docs/setup/installation.md) in quickstart.md
                    # If we moved both, we might need to adjust their relative depth

                    for old, new in sorted_items:
                        if old in content:
                            content = content.replace(old, new)
                            modified = True

                    if modified:
                        print(f"    Synced: {file_path.relative_to(ROOT_DIR)}")
                        file_path.write_text(content, encoding="utf-8")
                except Exception as e:
                    print(f"    Error: {f}: {e}")


if __name__ == "__main__":
    reorganize_docs()
