---
## Overview

description: Automated workflow for full repository audits, structural cleaning, and artifact synchronization.
---

# Repository Maintenance

Comprehensive workflow for maintaining repository health, documentation integrity, and artifact synchronization.

**Version:** 1.0.0
**Created:** 2026-02-13
**Agent**: `system-steward`

## Trigger Conditions

This workflow is activated when:
- Scheduled monthly/quarterly maintenance is due.
- Major repository restructuring is initiated.
- User requests a comprehensive health check.
- Verification after batch file operations is needed.

**Trigger Examples:**
- "Run repository maintenance"
- "Audit the system and fix links"
- "Sync all manifests and update README counts"
- "Clean up project structure and fix references"

## Steps

### 1. Structural Audit & Cleaning
- **Action**: Move misplaced files to correct subdirectories and enforce kebab-case naming.
- **Verification**: Ensure no files remain in the root that shouldn't be there.

### 2. Full Link Verification
- **Command**: `python scripts/maintenance/link_checker.py --external`
- **Action**: Identify all broken internal references and dead external URLs.
- **Goal**: Maintain 100% link integrity across all documentation.

### 3. Reference Remediation
- **Action**: Fix broken relative paths using the `system-steward`'s capabilities.
- **Focus**: Prioritize index files and root-level documentation.

### 4. Artifact Cache Synchronization
- **Command**: `python scripts/validation/update_index.py --full`
- **Action**: Rebuild the artifact index cache used for fast validation.

### 5. Version Registry Sync
- **Command**: `python scripts/validation/sync_manifest_versions.py --sync`
- **Action**: Synchronize version numbers from `CHANGELOG.md` to all manifest and documentation footers.

### 6. README Automation
- **Command**: `python scripts/validation/validate_readme_structure.py --update`
- **Action**: Update artifact counts and structural descriptions in `README.md`.

### 7. Maintenance Report
- **Action**: Generate a summary of actions taken and current system health status.


## Decision Points

- Is the requirement clear?
- Are the tests passing?


## Example Session

User: Run the workflow
Agent: Initiating workflow steps...
