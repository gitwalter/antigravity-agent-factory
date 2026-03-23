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
  - '**Agents**: `system-architecture-specialist`'
  - '**Actions**:'
  - **Brainstorming Phase**: Use the `brainstorming` skill to refine project intent.
  - **Clarify**: Ask one question at a time.
  - **Propose**: 2-3 approaches with trade-offs.
  - **Hard Gate**: Present design and get USER approval.
  - **Design Doc**: Save to `docs/designs/YYYY-MM-DD-<topic>.md`.
  agents:
  - system-architecture-specialist
  goal: Ensure a solid, user-approved design before any planning or code.
  name: Brainstorming & Design Approval
  skills:
  - brainstorming
  tools:
  - write_to_file
- actions:
  - '**Agents**: `project-operations-specialist`, `system-architecture-specialist`'
  - '**Actions**:'
  - Load `knowledge/ai-design.md` and `knowledge/prd.md`.
  - **Planning Phase**: Use the `writing-plans` skill to decompose the design.
  - **Granularity**: Ensure tasks are 2-5 minute chunks.
  - **Refinement**: Each task must include a RED (fail) and GREEN (pass) verification step.
  - Generate `implementation_plan.md` using the factory template.
  - Use `notify_user` to request review and approval.
  agents:
  - project-operations-specialist
  - system-architecture-specialist
  goal: Create a detailed, bite-sized implementation roadmap.
  name: Structural Planning
  skills:
  - writing-plans
  tools:
  - write_to_file
  - notify_user
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - **Execution Phase**: Use the `subagent-driven-development` skill.
  - **RED**: Verify a failing test for each task.
  - **GREEN**: Implement minimal code and verify pass.
  - **Evidence**: Save verification output to `tmp/verification_<task_id>.log`.
  - **Documentation**: Generate `walkthrough.md` incrementally.
  agents:
  - project-operations-specialist
  goal: Build the feature with maximum rigor and evidence.
  name: Rigorous Implementation
  skills:
  - subagent-driven-development
  - tdd-rigor
  - verification-before-completion
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
version: 2.0.0
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
