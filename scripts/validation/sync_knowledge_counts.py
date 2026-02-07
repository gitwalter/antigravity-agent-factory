#!/usr/bin/env python3
"""
Sync knowledge file counts across manifest.json and KNOWLEDGE_FILES.md.

This script counts actual JSON files in the knowledge/ directory and updates:
- knowledge/manifest.json -> statistics.total_files
- docs/reference/KNOWLEDGE_FILES.md -> "includes **X knowledge files**"

Usage:
    python scripts/validation/sync_knowledge_counts.py          # Check only
    python scripts/validation/sync_knowledge_counts.py --sync   # Auto-fix
"""

import json
import re
import sys
from pathlib import Path
from typing import NamedTuple


class KnowledgeCounts(NamedTuple):
    """Knowledge file counts."""
    total: int
    manifest_count: int
    docs_count: int


def count_knowledge_files() -> int:
    """Count actual JSON files in knowledge/ directory."""
    knowledge_dir = Path("knowledge")
    if not knowledge_dir.exists():
        return 0
    
    # Count .json files, excluding schema files, manifest.json, and subdirectories
    # manifest.json is a meta-file that tracks knowledge files, not a knowledge file itself
    json_files = [
        f for f in knowledge_dir.glob("*.json")
        if f.is_file() and not f.name.startswith("_") and f.name != "manifest.json"
    ]
    return len(json_files)


def get_manifest_count() -> int:
    """Extract total_files from manifest.json."""
    manifest_path = Path("knowledge/manifest.json")
    if not manifest_path.exists():
        return 0
    
    try:
        data = json.loads(manifest_path.read_text(encoding='utf-8'))
        return data.get("statistics", {}).get("total_files", 0)
    except (json.JSONDecodeError, KeyError):
        return 0


def get_docs_count() -> int:
    """Extract knowledge file count from KNOWLEDGE_FILES.md."""
    docs_path = Path("docs/reference/KNOWLEDGE_FILES.md")
    if not docs_path.exists():
        return 0
    
    content = docs_path.read_text(encoding='utf-8')
    
    # Pattern: "includes **72 knowledge files**" or "currently includes **72 knowledge files**"
    match = re.search(r'includes \*\*(\d+) knowledge files?\*\*', content)
    if match:
        return int(match.group(1))
    
    return 0


def update_manifest(actual_count: int, dry_run: bool = True) -> bool:
    """
    Update manifest.json with actual knowledge file count.
    
    Returns:
        True if update was needed (or would be needed)
    """
    manifest_path = Path("knowledge/manifest.json")
    if not manifest_path.exists():
        return False
    
    try:
        data = json.loads(manifest_path.read_text(encoding='utf-8'))
        current_count = data.get("statistics", {}).get("total_files", 0)
        
        if current_count == actual_count:
            return False
        
        if not dry_run:
            if "statistics" not in data:
                data["statistics"] = {}
            data["statistics"]["total_files"] = actual_count
            
            manifest_path.write_text(
                json.dumps(data, indent=2, ensure_ascii=False) + '\n',
                encoding='utf-8'
            )
        
        return True
    except json.JSONDecodeError:
        return False


def update_docs(actual_count: int, dry_run: bool = True) -> bool:
    """
    Update KNOWLEDGE_FILES.md with actual knowledge file count.
    
    Returns:
        True if update was needed (or would be needed)
    """
    docs_path = Path("docs/reference/KNOWLEDGE_FILES.md")
    if not docs_path.exists():
        return False
    
    content = docs_path.read_text(encoding='utf-8')
    
    # Check if count matches
    match = re.search(r'includes \*\*(\d+) knowledge files?\*\*', content)
    if not match:
        return False
    
    current_count = int(match.group(1))
    if current_count == actual_count:
        return False
    
    if not dry_run:
        # Update the count
        new_content = re.sub(
            r'includes \*\*\d+ knowledge files?\*\*',
            f'includes **{actual_count} knowledge files**',
            content
        )
        docs_path.write_text(new_content, encoding='utf-8')
    
    return True


def sync_knowledge_counts(dry_run: bool = True) -> tuple[bool, list[str]]:
    """
    Sync knowledge file counts across all locations.
    
    Returns:
        (all_synced, list of changes)
    """
    actual_count = count_knowledge_files()
    manifest_count = get_manifest_count()
    docs_count = get_docs_count()
    
    changes = []
    
    if manifest_count != actual_count:
        changes.append(f"manifest.json statistics.total_files: {manifest_count} -> {actual_count}")
        if not dry_run:
            update_manifest(actual_count, dry_run=False)
    
    if docs_count != actual_count:
        changes.append(f"KNOWLEDGE_FILES.md count: {docs_count} -> {actual_count}")
        if not dry_run:
            update_docs(actual_count, dry_run=False)
    
    return len(changes) == 0, changes


def main():
    """Main entry point."""
    sync = '--sync' in sys.argv
    
    actual_count = count_knowledge_files()
    manifest_count = get_manifest_count()
    docs_count = get_docs_count()
    
    print(f"Knowledge file counts:")
    print(f"  Actual files:    {actual_count}")
    print(f"  manifest.json:   {manifest_count}")
    print(f"  KNOWLEDGE_FILES: {docs_count}")
    print()
    
    all_synced, changes = sync_knowledge_counts(dry_run=not sync)
    
    if all_synced:
        print("[OK] Knowledge file counts are in sync")
        return 0
    
    if sync:
        print(f"[SYNCED] {len(changes)} count(s) updated:")
        for change in changes:
            print(f"  - {change}")
        return 0
    else:
        print(f"[OUT OF SYNC] {len(changes)} count(s) differ:")
        for change in changes:
            print(f"  - {change}")
        print("\nRun with --sync to fix")
        return 1


if __name__ == '__main__':
    sys.exit(main())
