---
agents:
- workflow-quality-specialist
- project-operations-specialist
- knowledge-operations-specialist
blueprints:
- universal
description: Antigravity workflow for documentation-workflow. Standardized for IDX
  Visual Editor.
domain: universal
name: documentation-workflow
steps:
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Check `task.md` or Plane issue sequence to map requirements.
  - Identify component and existing documentation state.
  agents:
  - project-operations-specialist
  goal: Identify which SDLC phase or component is being documented and establish context.
  name: Discovery & Mapping
  skills:
  - managing-plane-tasks
  - deepwiki
  tools:
  - deepwiki-read_wiki_structure
- actions:
  - '**Agents**: `project-operations-specialist`, `knowledge-operations-specialist`'
  - '**Actions**:'
  - 'For Features: Focus on `walkthrough.md` and `README.md`.'
  - 'For SDLC Gates: Focus on `prd.md`, `ai-design.md`, or `eval-report.md`.'
  - 'For Releases: Update `CHANGELOG.md` and `release-notes.md`.'
  agents:
  - project-operations-specialist
  - knowledge-operations-specialist
  goal: Generate high-fidelity documentation artifacts based on the mapped context.
  name: Artifact Drafting
  skills:
  - generating-documentation
  - writing-prd
  tools:
  - write_to_file
  - jinja2-templates
- actions:
  - '**Agents**: `workflow-quality-specialist`'
  - '**Actions**:'
  - Use `scripts/validation/validate_readme_structure.py` or equivalent.
  - Run `python scripts/maintenance/audit/link_checker.py --target <new_file>`.
  agents:
  - workflow-quality-specialist
  goal: Ensure the documentation adheres to factory standards and has functional links.
  name: Structural Validation
  skills:
  - verifiying-links
  - code-review
  tools:
  - scripts/maintenance/audit/link_checker.py
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Post the document content or a summarized link to the corresponding Plane issue.
  - If the doc introduces new patterns, update `knowledge-manifest.json`.
  - '**No Stubs**: Never create empty placeholder files.'
  - '**Relative Pathing**: Use `file:///` URIs relative to the root for all links.'
  - '**Tone**: Professional, technical, and proactive.'
  - '`sdlc-meta-orchestrator.md` - Context for phase documentation.'
  - '`committing-releases.md` - Context for version documentation.'
  - '"Execute generating-documentation.md"'
  agents:
  - project-operations-specialist
  goal: Integrate the document into the system context and Plane tracking.
  name: Induction & Sync
  skills:
  - managing-plane-tasks
  - managing-memory-bank
  tools:
  - managing-plane-tasks.py
  - memory_mcp
tags: []
type: sequential
version: 1.0.0
---

# Global Documentation Workflow (SDLC Phase 6)

**Version:** 1.0.0

## Overview
Antigravity workflow for documentation-workflow. Standardized for IDX Visual Editor.

## Trigger Conditions
- New features or components requiring documentation.
- Release cycle requiring CHANGELOG and release notes updates.
- User request: `/documentation-workflow`.

**Trigger Examples:**
- "Generate documentation for the new API endpoints."
- "Update the README with the latest architectural changes."

## Phases

### 1. Discovery & Mapping
- **Goal**: Identify which SDLC phase or component is being documented and establish context.
- **Agents**: `project-operations-specialist`
- **Skills**: managing-plane-tasks, deepwiki
- **Tools**: deepwiki-read_wiki_structure
- **Agents**: `project-operations-specialist`
- **Actions**:
- Check `task.md` or Plane issue sequence to map requirements.
- Identify component and existing documentation state.

### 2. Artifact Drafting
- **Goal**: Generate high-fidelity documentation artifacts based on the mapped context.
- **Agents**: `project-operations-specialist`, `knowledge-operations-specialist`
- **Skills**: generating-documentation, writing-prd
- **Tools**: write_to_file, jinja2-templates
- **Agents**: `project-operations-specialist`, `knowledge-operations-specialist`
- **Actions**:
- For Features: Focus on `walkthrough.md` and `README.md`.
- For SDLC Gates: Focus on `prd.md`, `ai-design.md`, or `eval-report.md`.
- For Releases: Update `CHANGELOG.md` and `release-notes.md`.

### 3. Structural Validation
- **Goal**: Ensure the documentation adheres to factory standards and has functional links.
- **Agents**: `workflow-quality-specialist`
- **Skills**: verifiying-links, code-review
- **Tools**: scripts/maintenance/audit/link_checker.py
- **Agents**: `workflow-quality-specialist`
- **Actions**:
- Use `scripts/validation/validate_readme_structure.py` or equivalent.
- Run `python scripts/maintenance/audit/link_checker.py --target <new_file>`.

### 4. Induction & Sync
- **Goal**: Integrate the document into the system context and Plane tracking.
- **Agents**: `project-operations-specialist`
- **Skills**: managing-plane-tasks, managing-memory-bank
- **Tools**: managing-plane-tasks.py, memory_mcp
- **Agents**: `project-operations-specialist`
- **Actions**:
- Post the document content or a summarized link to the corresponding Plane issue.
- If the doc introduces new patterns, update `knowledge-manifest.json`.
- **No Stubs**: Never create empty placeholder files.
- **Relative Pathing**: Use `file:///` URIs relative to the root for all links.
- **Tone**: Professional, technical, and proactive.
- `sdlc-meta-orchestrator.md` - Context for phase documentation.
- `committing-releases.md` - Context for version documentation.
- "Execute generating-documentation.md"
