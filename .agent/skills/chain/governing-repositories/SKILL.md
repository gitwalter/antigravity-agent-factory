---
description: Comprehensive skill for link verification, file organization, artifact
  syncing, and README automation.
name: governing-repositories
type: skill
---

# Repository Governance Skill

This skill provides unified capabilities for maintaining repository health, documentation integrity, and artifact synchronization.

## When to Use
- Before releases or major commits.
- During scheduled repository maintenance.
- After moving or renaming files to update references.
- To synchronize counts and indices across documentation.

## Prerequisites
- Python 3.10+
- `aiohttp` (for external link checking)
- `scripts/maintenance/link_checker.py`
- `scripts/validation/update_index.py`
- `scripts/validation/validate_readme_structure.py`
- `scripts/validation/sync_manifest_versions.py`

## Process
The following process ensures robust repository health and documentation integrity.

### 1. Link Verification & Repair
- **Scan**: `python scripts/maintenance/link_checker.py --external`
- **Fix**: Identify broken relative paths and update them. Prefer kebab-case and relative paths.

### 2. Repository Cleaning & Organization
- **Move Files**: Misplaced files (docs, scripts, patterns) should be moved to their logical subdirectories (e.g., `docs/`, `scripts/maintenance/`, `.agent/patterns/`).
- **Update References**: Use `link_checker.py` to find and fix broken references after moves.
- **Cleanup**: Remove temporary logs, redundant manifests, and non-conforming files.

### 3. Artifact Synchronization
- **Update Index**: Rebuild the artifact index cache:
  ```powershell
  python scripts/validation/update_index.py --full
  ```
- **Sync Versions**: Ensure version numbers are consistent across all files:
  ```powershell
  python scripts/validation/sync_manifest_versions.py --sync
  ```

### 4. README Automation
- **Validate/Update Counts**: Sync the counts in README.md with the actual filesystem:
  ```powershell
  python scripts/validation/validate_readme_structure.py --update
  ```

## Best Practices
- **Portability**: ALWAYS use relative paths for internal documentation links.
- **Naming**: Enforce kebab-case for all filenames to avoid cross-platform issues.
- **Atomic Operations**: Update references immediately after moving a file to avoid stale documentation.
- **Truth Source**: CHANGELOG.md is the source of truth for version numbers.
