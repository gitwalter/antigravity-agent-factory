---
## Overview

description: Systematic workflow for managing software releases including version bumping, changelog generation, tagging, and depl...
---

# Release Management

Systematic workflow for managing software releases including version bumping, changelog generation, tagging, and deployment coordination.

**Version:** 1.0.0
**Created:** 2026-02-02
**Applies To:** All stacks

## Trigger Conditions

This workflow is activated when:

- Release preparation requested
- Version bump needed
- Changelog generation required
- Release deployment initiated

**Trigger Examples:**
- "Prepare release v2.0.0"
- "Create a new release"
- "Bump version to 1.2.0"
- "Generate release notes"

## Steps

### Verify Branch Status

### Run Quality Checks

### Link & Documentation Audit
- **Agent**: `system-steward`
- **Skill**: `governing-repositories`
- **Action**: Run `python scripts/maintenance/link_checker.py --external` and perform full repository sync.

### Determine Version

### Update Version Files

### Collect Changes

### Generate Changelog Entry


## Decision Points

- Is the requirement clear?
- Are the tests passing?


## Example Session

User: Run the workflow
Agent: Initiating workflow steps...
