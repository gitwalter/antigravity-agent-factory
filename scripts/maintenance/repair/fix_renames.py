import os
import re
from pathlib import Path

ROOT_DIR = Path("d:/Users/wpoga/Documents/Python Scripts/antigravity-agent-factory")
DOCS_DIR = ROOT_DIR / "docs"


def fix_hyphenation(name):
    base, ext = os.path.splitext(name)
    if ext != ".md":
        return name

    # Check if it looks like "b-l-u-e-p-r-i-n-t-s"
    # Pattern: a hyphen between single letters repeatedly
    if re.search(r"[a-z]-[a-z]-[a-z]", base):
        # Remove hyphens that are between single letters
        # but keep hyphens that were intended as word separators?
        # Actually, if it's all "a-b-c", just remove all hyphens.
        # But wait, SOCIETY_INTEGRATION became society-integration-guide (with single letter hyphens)
        # It's safer to just remove ALL hyphens that are between single characters.

        # This regex finds a hyphen preceded by exactly one char and followed by exactly one char
        # but we need to do it repeatedly.
        new_base = base
        while True:
            updated = re.sub(
                r"(^|(?<=[^a-z]))([a-z])-([a-z])((?=[^a-z])|$)", r"\1\2\3\4", new_base
            )
            if updated == new_base:
                break
            new_base = updated

        # After removing single hyphens, we might have words.
        # If it was "society-integration", it might have been "s-o-c-i-e-t-y-i-n-t-e-g-r-a-t-i-o-n"
        # which becomes "societyintegration". This is not ideal but better than broken links.
        # Actually, the previous script made it "s-o-c-i-e-t-y-i-n-t-e-g-r-a-t-i-o-n-g-u-i-d-e"

        # Let's try to be smarter.
        # If the original was BLUEPRINTS, it became b-l-u-e-p-r-i-n-t-s.
        # So b-l-u-e-p-r-i-n-t-s -> blueprints
        # If there are NO multi-character words, just join everything.
        parts = base.split("-")
        if all(len(p) == 1 for p in parts):
            return "".join(parts) + ext

        # If there are some words, it's mixed.
        # Just replace all single-letter-hyphen-single-letter with both letters.
        return re.sub(r"([a-z])-([a-z])", r"\1\2", base) + ext
        # Wait, the above would turn "society-integration" (if it was two words) into "societyintegration".
        # But in my case, the hyphens were EVERYWHERE.

    return name


def build_fix_map():
    fix_map = {}
    for root, _, files in os.walk(DOCS_DIR):
        for f in files:
            fixed = fix_hyphenation(f)
            if fixed != f:
                fix_map[f] = fixed
    return fix_map


def rename_and_update(full_map):
    print(f"Fixing {len(full_map)} broken filenames...")
    for old, new in full_map.items():
        # Find the file first
        found_file = None
        for root, _, files in os.walk(DOCS_DIR):
            if old in files:
                found_file = Path(root) / old
                new_path = Path(root) / new
                print(f"  {old} -> {new}")
                os.rename(found_file, new_path)
                break

    print("Updating references to fixed names...")
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

    for root, dirs, files in os.walk(ROOT_DIR):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for f in files:
            if os.path.splitext(f)[1] in extensions:
                file_path = Path(root) / f
                try:
                    content = file_path.read_text(encoding="utf-8", errors="ignore")
                    modified = False
                    for old, new in full_map.items():
                        if old in content:
                            content = content.replace(old, new)
                            modified = True
                    if modified:
                        print(f"    Updated {file_path.relative_to(ROOT_DIR)}")
                        file_path.write_text(content, encoding="utf-8")
                except Exception as e:
                    print(f"    Error in {f}: {e}")


if __name__ == "__main__":
    m = build_fix_map()
    if not m:
        print("No hyphenated files found to fix.")
    else:
        print("Mapping to fix:")
        for k, v in m.items():
            print(f"  {k} -> {v}")
        rename_and_update(m)
