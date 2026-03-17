---
agents:
- '@Architect'
blueprints:
- universal
description: Antigravity workflow for repository-maintenance. Standardized for IDX
  Visual Editor.
domain: universal
name: repository-maintenance
steps:
- actions:
  - '**Verification**: Ensure no files remain in the root that shouldn''t be there.'
  - Move misplaced files to correct subdirectories and enforce kebab-case naming.
  agents:
  - '@Architect'
  goal: ''
  name: Structural Audit & Cleaning
  skills: []
  tools: []
- actions:
  - '**Standard**: Follow [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
    and Semantic Versioning.'
  - Update `CHANGELOG.md` with all changes since the last release.
  agents:
  - '@Architect'
  goal: ''
  name: Changelog Documentation
  skills: []
  tools: []
- actions:
  - '**Command**: `python scripts/maintenance/audit/link_checker.py --external`'
  - Identify all broken internal references and dead external URLs.
  agents:
  - '@Architect'
  goal: Maintain 100% link integrity across all documentation.
  name: Full Link Verification
  skills: []
  tools: []
- actions:
  - '**Focus**: Prioritize index files and root-level documentation.'
  - Fix broken relative paths using the `system-steward`'s capabilities.
  agents:
  - '@Architect'
  goal: ''
  name: Reference Remediation
  skills: []
  tools: []
- actions:
  - '**Requirement**: Must include proof of testing-agents and a summary of key architectural
    changes.'
  - Create or update `walkthrough.md` in the brain directory for the current session.
  agents:
  - '@Architect'
  goal: ''
  name: Artifact Documentation (Proof of Work)
  skills: []
  tools: []
- actions:
  - '**Command**: `python scripts/validation/update_index.py --full`'
  - Rebuild the artifact index cache used for fast validation.
  agents:
  - '@Architect'
  goal: ''
  name: Artifact Cache Synchronization
  skills: []
  tools: []
- actions:
  - '**Command**: `python scripts/validation/sync_manifest_versions.py --sync`'
  - Synchronize version numbers from `CHANGELOG.md` to all manifest and documentation
    footers.
  agents:
  - '@Architect'
  goal: ''
  name: Version Registry Sync
  skills: []
  tools: []
- actions:
  - '**Command**: `python scripts/validation/validate_readme_structure.py --update`'
  - Update artifact counts and structural descriptions in `README.md`.
  agents:
  - '@Architect'
  goal: ''
  name: README Automation
  skills: []
  tools: []
- actions:
  - '**Command**: `python -m pre-commit run --all-files`'
  - Run linting (`ruff`), type-checking (`mypy`), and structural checks.
  agents:
  - '@Architect'
  goal: 100% pass before the final commit.
  name: Pre-commit Validation
  skills: []
  tools: []
- actions:
  - '**Command**: `python scripts/maintenance/knowledge_audit.py`'
  - Detect knowledge debt, verify link integrity, and generate a health report.
  agents:
  - '@Architect'
  goal: Maintain high documentation quality and structural integrity.
  name: Knowledge Health Audit
  skills: []
  tools: []
- actions:
  - Is the requirement clear?
  - Are the tests passing?
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  - Generate a summary of actions taken and current system health status.
  agents:
  - '@Architect'
  goal: ''
  name: Maintenance Report
  skills: []
  tools: []
tags: []
type: sequential
version: 2.0.0
---
# Repository Maintenance

**Version:** 1.0.0

## Overview
Antigravity workflow for routine repository maintenance, structural auditing, and health checks. Standardized for IDX Visual Editor.

## Trigger Conditions
- Regular maintenance schedule (weekly/monthly).
- After major refactoring or large batch of changes.
- User request: `/repository-maintenance`.

**Trigger Examples:**
- "Perform a full structural audit and link verification of the repository."
- "Execute repository maintenance to sync versions and rebuild the artifact cache."

## Phases

### 1. Structural Audit & Cleaning
- **Agents**: `@Architect`
- **Verification**: Ensure no files remain in the root that shouldn't be there.
- Move misplaced files to correct subdirectories and enforce kebab-case naming.

### 2. Changelog Documentation
- **Agents**: `@Architect`
- **Standard**: Follow [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and Semantic Versioning.
- Update `CHANGELOG.md` with all changes since the last release.

### 3. Full Link Verification
- **Goal**: Maintain 100% link integrity across all documentation.
- **Agents**: `@Architect`
- **Command**: `python scripts/maintenance/audit/link_checker.py --external`
- Identify all broken internal references and dead external URLs.

### 4. Reference Remediation
- **Agents**: `@Architect`
- **Focus**: Prioritize index files and root-level documentation.
- Fix broken relative paths using the `system-steward`'s capabilities.

### 5. Artifact Documentation (Proof of Work)
- **Agents**: `@Architect`
- **Requirement**: Must include proof of testing-agents and a summary of key architectural changes.
- Create or update `walkthrough.md` in the brain directory for the current session.

### 6. Artifact Cache Synchronization
- **Agents**: `@Architect`
- **Command**: `python scripts/validation/update_index.py --full`
- Rebuild the artifact index cache used for fast validation.

### 7. Version Registry Sync
- **Agents**: `@Architect`
- **Command**: `python scripts/validation/sync_manifest_versions.py --sync`
- Synchronize version numbers from `CHANGELOG.md` to all manifest and documentation footers.

### 8. README Automation
- **Agents**: `@Architect`
- **Command**: `python scripts/validation/validate_readme_structure.py --update`
- Update artifact counts and structural descriptions in `README.md`.

### 9. Pre-commit Validation
- **Goal**: 100% pass before the final commit.
- **Agents**: `@Architect`
- **Command**: `python -m pre-commit run --all-files`
- Run linting (`ruff`), type-checking (`mypy`), and structural checks.

### 10. Knowledge Health Audit
- **Goal**: Maintain high documentation quality and structural integrity.
- **Agents**: `@Architect`
- **Command**: `python scripts/maintenance/knowledge_audit.py`
- Detect knowledge debt, verify link integrity, and generate a health report.

### 11. Maintenance Report
- **Agents**: `@Architect`
- Is the requirement clear?
- Are the tests passing?
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
- Generate a summary of actions taken and current system health status.
