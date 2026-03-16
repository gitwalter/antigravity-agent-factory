---
agents:
- system-architecture-specialist
- project-operations-specialist
blueprints:
- universal
description: Antigravity workflow for agent-development. Standardized for IDX Visual
  Editor.
domain: universal
name: agent-development
steps:
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Use `managing-plane-tasks` to create an `AGENT` or `FEATURE` issue.
  - Use `create_task.py` with the Jinja2 template and task schema.
  agents:
  - project-operations-specialist
  goal: Establish tracking and metadata for the development task.
  name: Project Initiation
  skills:
  - managing-plane-tasks
  tools:
  - create_task.py
- actions:
  - '**Agents**: `project-operations-specialist`, `system-architecture-specialist`'
  - '**Actions**:'
  - Load `knowledge/ai-design.md` and `knowledge/prd.md`.
  - Trigger `.agent/skills/chain/generating-agents/SKILL.md`.
  agents:
  - project-operations-specialist
  - system-architecture-specialist
  goal: Research requirements and generate initial agent logic/code structure.
  name: Design & Generation
  skills:
  - generating-agents
  - analyzing-code
  tools:
  - view_file
  - write_to_file
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Iterate on implementation based on `implementation_plan.md`.
  - Generate `walkthrough.md` using the `generating-documentation` skill.
  agents:
  - project-operations-specialist
  goal: Build the feature iteratively and document the proof of work.
  name: Iterative Implementation
  skills:
  - developing-ai-agents
  - generating-documentation
  tools:
  - multi_replace_file_content
  - walkthrough-generator
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Write implementation to the repository and ensure technical docs are updated.
  - Prompt user to run `/agent-testing-agents`.
  - Close the Plane issue via `managing-plane-tasks.py` using the Jinja2 solution
    template.
  - Mandatory generation of `walkthrough.md`.
  - Code must pass initial "Green" verification.
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - project-operations-specialist
  goal: Update repository state and close tracking issues.
  name: Closure & Handoff
  skills:
  - committing-releases
  - managing-plane-tasks
  tools:
  - managing-plane-tasks.py
tags: []
type: sequential
version: 1.0.0
---

# /developing-ai-agents Workflow (SDLC Phase 4)

**Version:** 1.0.0

## Overview
This workflow governs the development and refinement of AI agents within the Antigravity Agent Factory, ensuring adherence to the 5-layer architecture and axiomatic alignments.

## Trigger Conditions
- New agent requirement identified.
- Existing agent logic needs refinement or bug fixes.
- Architectural change requiring agent-level updates.

**Trigger Examples:**
- "Develop a new backend specialist agent."
- "Refactor the SYARCH persona for better multi-agent coordination."

## Phases

### Phase 1: Project Initiation
- **Goal**: Establish tracking and metadata for the development task.
- **Agents**: `project-operations-specialist`
- **Skills**: managing-plane-tasks
- **Tools**: create_task.py
- **Actions**:
- Use `managing-plane-tasks` to create an `AGENT` or `FEATURE` issue.
- Use `create_task.py` with the Jinja2 template and task schema.

### Phase 2: Design & Generation
- **Goal**: Research requirements and generate initial agent logic/code structure.
- **Agents**: `project-operations-specialist`, `system-architecture-specialist`
- **Skills**: generating-agents, analyzing-code
- **Tools**: view_file, write_to_file
- **Actions**:
- Load `knowledge/ai-design.md` and `knowledge/prd.md`.
- Trigger `.agent/skills/chain/generating-agents/SKILL.md`.

### Phase 3: Iterative Implementation
- **Goal**: Build the feature iteratively and document the proof of work.
- **Agents**: `project-operations-specialist`
- **Skills**: developing-ai-agents, generating-documentation
- **Tools**: multi_replace_file_content, walkthrough-generator
- **Actions**:
- Iterate on implementation based on `implementation_plan.md`.
- Generate `walkthrough.md` using the `generating-documentation` skill.

### Phase 4: Closure & Handoff
- **Goal**: Update repository state and close tracking issues.
- **Agents**: `project-operations-specialist`
- **Skills**: committing-releases, managing-plane-tasks
- **Tools**: managing-plane-tasks.py
- **Actions**:
- Write implementation to the repository and ensure technical docs are updated.
- Prompt user to run `/agent-testing-agents`.
- Close the Plane issue via `managing-plane-tasks.py` using the Jinja2 solution template.
- Mandatory generation of `walkthrough.md`.
- Code must pass initial "Green" verification.
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)

## Best Practices
- Always create an `implementation_plan.md` before significant changes.
- Ensure all tool calls are verified against current schemas.
- Use `@Architect` persona for architectural reviews.

## Related
- [/agent-testing](file:///.agent/workflows/agent-testing.md)
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
