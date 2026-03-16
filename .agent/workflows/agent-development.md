---
description: Multi-step workflow for developing AI agents from design through deployment.
version: 1.0.0
tags:
- agent
- development
- standardized
---


# /developing-ai-agents Workflow (SDLC Phase 4)

**Version:** 1.0.0
**Created:** 2026-03-06
**Agent:** `project-operations-specialist`

**Goal:** Implement the approved AI System Design, ensuring all code and agent logic are production-ready.

## Trigger Conditions

This workflow is activated when:
- Phase 3 (Architecture) is marked complete.
- A user explicitly requests to build an agent based on the AI design.
- The `sdlc-meta-orchestrator` transitions to Phase 4.

## Trigger Examples:
- "Start agent development based on the design."
- "Build the feature agent."
- "Execute Phase 4 of SDLC."

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

## Phase Gate (Build):
- Mandatory generation of `walkthrough.md`.
- Code must pass initial "Green" verification.


## Best Practices
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.


## Related
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
