---
name: generating-documentation
description: Phase 6 SDLC workflow for generating and maintaining comprehensive project
  documentation.
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
tags:
- documentation
- workflow
- standardized
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

### Phase 1: Discovery & Mapping
- **Goal**: Identify which SDLC phase or component is being documented and establish context.
- **Agents**: `project-operations-specialist`
- **Skills**: managing-plane-tasks, deepwiki
- **Tools**: deepwiki-read_wiki_structure
- **Actions**:
    - Check `task.md` or Plane issue sequence to map requirements.
    - Identify component and existing documentation state.

### Phase 2: Artifact Drafting
- **Goal**: Generate high-fidelity documentation artifacts based on the mapped context.
- **Agents**: `project-operations-specialist`, `knowledge-operations-specialist`
- **Skills**: generating-documentation, writing-prd
- **Tools**: write_to_file, jinja2-templates
- **Actions**:
    - For Features: Focus on `walkthrough.md` and `README.md`.
    - For SDLC Gates: Focus on `prd.md`, `ai-design.md`, or `eval-report.md`.
    - For Releases: Update `CHANGELOG.md` and `release-notes.md`.

### Phase 3: Structural Validation
- **Goal**: Ensure the documentation adheres to factory standards and has functional links.
- **Agents**: `workflow-quality-specialist`
- **Skills**: verifiying-links, code-review
- **Tools**: scripts/maintenance/audit/link_checker.py
- **Actions**:
    - Use `scripts/validation/validate_readme_structure.py` or equivalent.
    - Run `python scripts/maintenance/audit/link_checker.py --target <new_file>`.

### Phase 4: Induction & Sync
- **Goal**: Integrate the document into the system context and Plane tracking.
- **Agents**: `project-operations-specialist`
- **Skills**: managing-plane-tasks, managing-memory-bank
- **Tools**: managing-plane-tasks.py, memory_mcp
- **Actions**:
    - Post the document content or a summarized link to the corresponding Plane issue.
    - If the doc introduces new patterns, update `knowledge-manifest.json`.

## Best Practices
- **No Stubs**: Never create empty placeholder files.
- **Relative Pathing**: Use `file:///` URIs relative to the root for all links.
- **Tone**: Professional, technical, and proactive.

## Related Workflows
- `sdlc-meta-orchestrator.md` - Context for phase documentation.
- `committing-releases.md` - Context for version documentation.


## Trigger Examples
- "Execute generating-documentation.md"
