import os
import re
from pathlib import Path

# Mapping: {OriginalBasename: NewBasename}
RENAME_MAP = {
    # VERY IMPORTANT (KEEP UPPERCASE)
    "asp-value-proposition.md": "asp-value-proposition.md",
    "blueprint-version-management.md": "blueprint-version-management.md",
    "configuration.md": "configuration.md",
    "extension-guide.md": "extension-guide.md",
    "getting-started.md": "getting-started.md",
    "installation.md": "installation.md",
    "quickstart.md": "quickstart.md",
    "system-blueprint.md": "system-blueprint.md",
    "testing.md": "testing.md",
    "test-catalog.md": "test-catalog.md",
    "troubleshooting.md": "troubleshooting.md",
    "user-guide.md": "user-guide.md",
    "CHANGELOG.md": "CHANGELOG.md",
    "README.md": "README.md",
    
    # STANDARD (KEBAB-CASE)
    "google-agent-sdk.md": "google-agent-sdk.md",
    "mcp-installation-guide.md": "mcp-installation-guide.md",   # Keep as is
}

ROOT_DIR = Path("d:/Users/wpoga/Documents/Python Scripts/antigravity-agent-factory")
DOCS_DIR = ROOT_DIR / "docs"

def to_kebab_case(name):
    # If it's already in our "Important" list, don't change it to kebab
    if name in RENAME_MAP and RENAME_MAP[name].isupper():
        return RENAME_MAP[name]
    
    # Otherwise, convert to kebab-case
    s = name.replace("_", "-").replace(" ", "-")
    s = re.sub(r'([A-Z])', r'-\1', s).strip('-').lower()
    s = re.sub(r'-+', '-', s)
    if not s.endswith(".md") and name.endswith(".md"):
        s += ".md"
    return s

def build_full_map():
    full_map = {}
    for root, _, files in os.walk(DOCS_DIR):
        for f in files:
            if f.endswith(".md"):
                if f in RENAME_MAP:
                    full_map[f] = RENAME_MAP[f]
                else:
                    full_map[f] = to_kebab_case(f)
    return full_map

def rename_files(full_map):
    print("Renaming files in docs/...")
    for root, _, files in os.walk(DOCS_DIR):
        for f in files:
            if f in full_map and f != full_map[f]:
                old_path = Path(root) / f
                new_path = Path(root) / full_map[f]
                print(f"  {f} -> {full_map[f]}")
                os.rename(old_path, new_path)

def update_references(full_map):
    print("Updating references across repository...")
    # Extensions to scan for references
    extensions = {".md", ".json", ".yaml", ".yml", ".py", ".js", ".ts"}
    ignore_dirs = {".git", ".venv", "node_modules", ".pytest_cache", ".ruff_cache", "__pycache__", "tmp", ".gemini"}
    
    for root, dirs, files in os.walk(ROOT_DIR):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for f in files:
            if os.path.splitext(f)[1] in extensions:
                file_path = Path(root) / f
                try:
                    content = file_path.read_text(encoding="utf-8", errors="ignore")
                    modified = False
                    for old, new in full_map.items():
                        if old != new and old in content:
                            # Use regex to avoid partial matches (e.g., matching 'DOC.md' in 'MYDOC.md')
                            # Look for standard markdown link format or just the filename
                            pattern = rf'(?<![a-zA-Z0-9_/]){re.escape(old)}'
                            if re.search(pattern, content):
                                content = re.sub(pattern, new, content)
                                modified = True
                    
                    if modified:
                        print(f"  Fixed refs in {file_path.relative_to(ROOT_DIR)}")
                        file_path.write_text(content, encoding="utf-8")
                except Exception as e:
                    print(f"  Error processing {f}: {e}")

if __name__ == "__main__":
    m = build_full_map()
    # Log the full mapping for verification
    print("Full Renaming Map:")
    for k, v in m.items():
        if k != v:
            print(f"  {k} -> {v}")
    
    # Execute
    rename_files(m)
    update_references(m)
