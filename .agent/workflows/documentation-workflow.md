---
name: documentation-workflow
description: Phase 6 SDLC workflow for generating and maintaining comprehensive project documentation.
version: 2.0.0
type: pipeline
domain: universal
agents:
  - project-operations-specialist
blueprints:
  - standard-sdlc
steps:
  - name: Discovery
    description: Identify component and existing documentation state.
  - name: Drafting
    description: Generate the required documentation artifacts.
  - name: Validation
    description: Run structural and link checks on new docs.
  - name: Induction
    description: Sync docs with Plane and the Memory MCP graph.
---

# Global Documentation Workflow (SDLC Phase 6)

**Version:** 2.0.0

**Goal:** Ensure every phase of work is documented with high fidelity, maintaining a single source of truth for the project's architecture, requirements, and history.

## Trigger Conditions
- Completion of an SDLC phase.
- Explicit request: "Document the [system/feature]", "Generate API docs".
- Before a release or repository audit.

**Trigger Examples:**
- "Document the new RAG module."
- "Generate API documentation for the agent factory."
- "Execute the documentation workflow for the current phase."
- "Update the README and walkthrough for the latest feature."

## Phases

### 1. Discovery & Mapping
Identify which SDLC phase or component is being documented.
- **Agent**: `project-operations-specialist`
- **Skill**: Mandatory use of `.agent/skills/routing/managing-plane-tasks/SKILL.md` for issue discovery.
- **Action**: Check `task.md` or Plane issue sequence to map requirements.
- **Tool**: `deepwiki-read_wiki_structure` to find existing docs.

### 2. Artifact Drafting
Invoke the `documentation-generation` skill to create the artifact.
- **For Features**: Focus on `walkthrough.md` and `README.md`.
- **For SDLC Gates**: Focus on `prd.md`, `ai-design.md`, or `eval-report.md`.
- **For Releases**: Update `CHANGELOG.md` and `release-notes.md`.

### 3. Structural Validation
Ensure the documentation adheres to factory standards.
- **Logic**: Use `scripts/validation/validate_readme_structure.py` or equivalent.
- **Link Check**: Run `python scripts/maintenance/audit/link_checker.py --target <new_file>`.

### 4. Induction & Sync
Integrate the document into the system context.
- **Agent**: `project-operations-specialist`
- **Skill**: Mandatory use of `.agent/skills/routing/managing-plane-tasks/SKILL.md` for Plane synchronization.
- **Plane Sync**: Post the document content or a summarized link to the corresponding Plane issue.
- **Memory Induction**: If the doc introduces new patterns, update `knowledge-manifest.json` via the `managing-memory-bank` skill.

## Best Practices
- **No Stubs**: Never create empty placeholder files.
- **Relative Pathing**: Use `file:///` URIs relative to the root for all links.
- **Tone**: Professional, technical, and proactive.

## Related Workflows
- `sdlc-meta-orchestrator.md` - Context for phase documentation.
- `release-management.md` - Context for version documentation.
