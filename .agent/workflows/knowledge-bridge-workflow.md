---
description: Run the Success & Error Knowledge Bridge to synthesize new KIs
---

# Knowledge Bridge Workflow

**Version:** 1.0.0

## Overview
Antigravity workflow for the Success & Error Knowledge Bridge. Standardized for IDX Visual Editor.

## Trigger Conditions
- Run weekly or after the closure of a major Epic.
- User request: `/knowledge-bridge`.

**Trigger Examples:**
- "Run the knowledge bridge workflow."
- "Synthesize recent work into knowledge items using the bridge."

## Phases

### 1. Execute Synthesis Analysis
- **Goal**: Scan changelogs, ideas, and recent `walkthrough.md` files for missing patterns.
- **Agents**: `knowledge-operations-specialist`
- **Actions**:
  - Run the proactive synthesis script: `python scripts/maintenance/proactive_synthesis.py`
  - Review the drafted KIs generated in `tmp/`.

### 2. Verify and Refine Drafts
- **Goal**: Ensure drafted KIs are high quality and meet schema requirements.
- **Agents**: `workflow-quality-specialist`
- **Actions**:
  - Review the drafted JSONs in `tmp/`.
  - Expand `patterns`, `best_practices`, and `anti_patterns` with explicit code examples and rationale.
  - Test validation: Ensure the JSON matches `.agent/config/schemas/knowledge-file.schema.json`.

### 3. Consolidate into Memory
- **Goal**: Induct verified KIs into the active factory memory.
- **Agents**: `knowledge-operations-specialist`
- **Actions**:
  - Move the refined JSONs into `.agent/knowledge/`.
  - Update `knowledge-manifest.json` using `python scripts/maintenance/sync/sync_artifacts.py --sync`.
  - Commit the new KIs to the permanent ledger.
