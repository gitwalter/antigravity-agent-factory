# Maintenance Procedures

This document outlines standard procedures for maintaining the Antigravity Agent Factory repository.

## Pre-Commit Synchronization

To keep documentation, artifacts, and counts in sync, the following scripts **MUST** be run before committing changes.

### 1. Version Synchronization
Ensures the factory version from `CHANGELOG.md` is propagated to all relevant files.
```powershell
python scripts/validation/sync_manifest_versions.py --sync
```

### 2. Knowledge Counts
Updates knowledge file counts in `manifest.json` and documentation.
```powershell
python scripts/validation/sync_knowledge_counts.py --sync
```

### 3. README Structure
Validates and updates the project structure and counts in `README.md`.
```powershell
python scripts/validation/validate_readme_structure.py --update
```

### 4. Unified Artifact Sync
Runs the configuration-driven sync system for various artifacts and tables.
```powershell
python scripts/validation/sync_artifacts.py --sync
```

### 5. Catalog Generation
Regenerates the `CATALOG.md` to include any new agents, skills, or blueprints.
```powershell
python scripts/generate_catalog.py
```

### 6. Artifact Index Update (Optional but recommended)
Updates the fast-lookup cache for artifacts.
```powershell
python scripts/validation/update_index.py --full
```

## Verification

After running these scripts, run `git status` to see if any files were modified. If so, include them in your commit.
