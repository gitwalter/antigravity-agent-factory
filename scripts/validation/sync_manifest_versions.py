#!/usr/bin/env python3
"""
Sync Factory versions across all files from CHANGELOG.md (source of truth).

Source of Truth:
- Factory version → CHANGELOG.md's latest version header [X.X.X]
- File versions → Each knowledge/*.json file's "version" field

Synced Locations:
- knowledge/manifest.json → factory_version
- README.md → Footer (*Antigravity Agent Factory vX.X.X*)
- docs/GETTING_STARTED.md → Footer (*Antigravity Agent Factory vX.X.X*)
- docs/ONBOARDING_GUIDE.md → Footer (*Antigravity Agent Factory vX.X.X*)
- scripts/core/generate_project.py → Comment (# Factory Version: X.X.X)
- templates/factory/agentrules-template.md → Header (**Version**: X.X)
- templates/knowledge/guardian-protocol.json.tmpl → source_factory_version
- .agentrules → Footer (*Antigravity Agent Factory vX.X.X*)

Usage:
    python scripts/validation/sync_manifest_versions.py          # Check only
    python scripts/validation/sync_manifest_versions.py --sync   # Auto-fix
"""

import json
import re
import sys
from pathlib import Path
from typing import Callable, Optional

def get_changelog_version() -> str:
    """Extract latest version from CHANGELOG.md (source of truth for factory version)."""
    changelog_path = Path('CHANGELOG.md')
    if not changelog_path.exists():
        return "0.0.0"
    changelog = changelog_path.read_text(encoding='utf-8')
    match = re.search(r'^## \[(\d+\.\d+\.\d+)\]', changelog, re.MULTILINE)
    if match:
        return match.group(1)
    return "0.0.0"


# =============================================================================
# VERSION SYNC DEFINITIONS
# 
# HOW TO EXTEND: When you find a file with a Factory version reference, add:
#   {
#       "file": "path/to/file.ext",           # Relative to repo root
#       "name": "descriptive name",            # For logging
#       "pattern": r'regex with (\d+\.\d+\.\d+)',  # Capture group for version
#       "replacement": lambda v: f'text with {v}',  # How to insert new version
#   }
#
# The pattern must have exactly ONE capture group for the version number.
# Source of truth: CHANGELOG.md's latest ## [X.Y.Z] header
# =============================================================================

VERSION_LOCATIONS = [
    {
        "file": "README.md",
        "name": "README.md footer",
        "pattern": r'\*Antigravity Agent Factory v(\d+\.\d+\.\d+)\*',
        "replacement": lambda v: f'*Antigravity Agent Factory v{v}*',
    },
    {
        "file": "docs/USER_GUIDE.md",
        "name": "USER_GUIDE.md footer",
        "pattern": r'\*Antigravity Agent Factory v[\d.]+\*',
        "replacement": lambda v: f'*Antigravity Agent Factory v{v}*',
        "extract_pattern": r'\*Antigravity Agent Factory v([\d.]+)\*',
    },
    {
        "file": "docs/PORTING_GUIDE.md",
        "name": "PORTING_GUIDE.md footer",
        "pattern": r'\*Antigravity Agent Factory v[\d.]+\*',
        "replacement": lambda v: f'*Antigravity Agent Factory v{v}*',
        "extract_pattern": r'\*Antigravity Agent Factory v([\d.]+)\*',
    },
    {
        "file": "scripts/core/generate_project.py",
        "name": "generate_project.py comment",
        "pattern": r'# Factory Version: [\d.]+',
        "replacement": lambda v: f'# Factory Version: {v}',
        "extract_pattern": r'# Factory Version: ([\d.]+)',
    },
    {
        "file": "templates/factory/agentrules-template.md",
        "name": "agentrules-template.md header",
        "pattern": r'\*\*Version\*\*: [\d.]+ \(5-Layer',
        "replacement": lambda v: f'**Version**: {v} (5-Layer',
        "extract_pattern": r'\*\*Version\*\*: ([\d.]+)',
    },
    {
        "file": "templates/knowledge/guardian-protocol.json.tmpl",
        "name": "guardian-protocol.json.tmpl",
        "pattern": r'"source_factory_version": "[\d.]+"',
        "replacement": lambda v: f'"source_factory_version": "{v}"',
        "extract_pattern": r'"source_factory_version": "([\d.]+)"',
    },
    {
        "file": ".agentrules",
        "name": ".agentrules footer",
        "pattern": r'\*Antigravity Agent Factory v[\d.]+\*',
        "replacement": lambda v: f'*Antigravity Agent Factory v{v}*',
        "extract_pattern": r'\*Antigravity Agent Factory v([\d.]+)\*',
    },
]


def get_file_version_generic(filepath: Path, pattern: str) -> Optional[str]:
    """Extract version from a file using a regex pattern."""
    if not filepath.exists():
        return None
    content = filepath.read_text(encoding='utf-8')
    match = re.search(pattern, content)
    if match:
        return match.group(1)
    return None


def sync_file_version(
    filepath: Path, 
    pattern: str, 
    replacement_func: Callable[[str], str],
    target_version: str,
    dry_run: bool = True
) -> bool:
    """
    Sync a file's version to target version.
    
    Returns:
        True if sync was performed (or would be performed if dry_run)
    """
    if not filepath.exists():
        return False
    
    content = filepath.read_text(encoding='utf-8')
    
    if not re.search(pattern, content):
        return False
    
    if not dry_run:
        new_content = re.sub(pattern, replacement_func(target_version), content)
        filepath.write_text(new_content, encoding='utf-8')
    
    return True

def get_file_version(filepath: Path) -> Optional[str]:
    """Extract version from a knowledge JSON file."""
    try:
        data = json.loads(filepath.read_text(encoding='utf-8'))
        return data.get('version')
    except (json.JSONDecodeError, FileNotFoundError):
        return None

def sync_manifest(dry_run: bool = True) -> tuple[bool, list[str]]:
    """
    Sync all versions from source of truth (CHANGELOG.md).
    
    Returns:
        (all_synced, list of changes)
    """
    manifest_path = Path('knowledge/manifest.json')
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    
    changes = []
    manifest_changed = False
    
    # Get source of truth version
    changelog_version = get_changelog_version()
    
    # 1. Sync manifest.json factory_version
    if manifest.get('factory_version') != changelog_version:
        changes.append(f"manifest.json factory_version: {manifest.get('factory_version')} -> {changelog_version}")
        if not dry_run:
            manifest['factory_version'] = changelog_version
            manifest_changed = True
    
    # 2. Sync all VERSION_LOCATIONS
    for loc in VERSION_LOCATIONS:
        filepath = Path(loc["file"])
        extract_pattern = loc.get("extract_pattern", loc["pattern"])
        
        current_version = get_file_version_generic(filepath, extract_pattern)
        
        if current_version and current_version != changelog_version:
            changes.append(f"{loc['name']}: {current_version} -> {changelog_version}")
            if not dry_run:
                sync_file_version(
                    filepath,
                    loc["pattern"],
                    loc["replacement"],
                    changelog_version,
                    dry_run=False
                )
    
    # 3. Sync each knowledge file's version in manifest from actual file
    knowledge_dir = Path('knowledge')
    for filename, entry in manifest.get('files', {}).items():
        filepath = knowledge_dir / filename
        if filepath.exists():
            actual_version = get_file_version(filepath)
            manifest_version = entry.get('version')
            
            if actual_version and actual_version != manifest_version:
                changes.append(f"manifest[{filename}]: {manifest_version} -> {actual_version}")
                if not dry_run:
                    entry['version'] = actual_version
                    manifest_changed = True
    
    # 4. Write updated manifest if changed
    if not dry_run and manifest_changed:
        manifest_path.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + '\n',
            encoding='utf-8'
        )
    
    return len(changes) == 0, changes

def main():
    sync = '--sync' in sys.argv
    
    all_synced, changes = sync_manifest(dry_run=not sync)
    
    if all_synced:
        print("[OK] All versions are in sync")
        return 0
    
    if sync:
        print(f"[SYNCED] {len(changes)} version(s):")
        for change in changes:
            print(f"  - {change}")
        return 0
    else:
        print(f"[OUT OF SYNC] {len(changes)} version(s):")
        for change in changes:
            print(f"  - {change}")
        print("\nRun with --sync to fix")
        return 1

if __name__ == '__main__':
    sys.exit(main())
