---
description: Systematic workflow for managing software releases including version bumping, changelog generation, tagging, and depl...
version: 1.0.0
---

# /release-management Workflow (SDLC Phase 6)

**Version:** 1.0.0


**Goal:** Coordinate the deployment of verified features into production, including versioning and formal release notes.

## Steps:
1. **Target**: Load `knowledge/eval-report.md` and `knowledge/walkthrough.md`.
2. **Execute**: Trigger `.agent/skills/releases/committing-releases/SKILL.md` (if existing, else use generic release skill).
3. **Link Audit**: Execute `python scripts/maintenance/link_checker.py --external` to ensure repo integrity.
4. **Notes**: Generate `release-notes.md` using `knowledge/templates/release-notes.md`.
5. **Output**: Update `CHANGELOG.md` and tag the repository.
6. **Follow-up**: Prompt user to run `/monitor` (Phase 7) to verify production health.

## Phase Gate (Deploy):
- Mandatory generation of `release-notes.md`.
- Successful merge and tagging.
- Human review of the release candidate.


## Trigger Conditions
- Triggered by user context or meta-orchestrator.


## Trigger Examples:
- "Execute this workflow."
