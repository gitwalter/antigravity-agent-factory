---
agents:
- system-architecture-specialist
- project-operations-specialist
- python-ai-specialist
blueprints:
- universal
description: Antigravity workflow for ai-system-design. Standardized for IDX Visual
  Editor.
domain: universal
name: ai-system-design
steps:
- actions:
  - 'Actions:'
  - Use `python-ai-specialist` to extract entities and constraints from `docs/sdlc/prd.md`.
  - Memory Hook: Call `mcp_memory_open_nodes` for `TASK:[IssueKey]` and `SOP:ai-system-design`.
  - Save-on-Discover: Register missing SOP/SKILL nodes if found in local filesystem.
  agents:
  - python-ai-specialist
  goal: Analyze the PRD and NFRs to establish technical constraints.
  name: Requirements Decomposition
  skills:
  - analyzing-code
  tools:
  - view_file
- actions:
  - 'Actions:'
  - Invoke the `/ai-designing-ai-systems` routing pattern to select between `chain`,
    `parallel`, or `orchestrator-workers` patterns.
  agents:
  - system-architecture-specialist
  goal: Choose the optimal stack (agents, MCPs, models, databases).
  name: Architecture Selection
  skills:
  - architecture-selection
  tools:
  - mcp_memory_search_nodes
- actions:
  - 'Actions:'
  - Trigger `.agent/skills/parallel/designing-apis/SKILL.md` to generate OpenAPI/JSON
    Schema definitions.
  agents:
  - python-ai-specialist
  goal: Define interaction protocols and data schemas.
  name: Interface & API Definition
  skills:
  - designing-apis
  tools:
  - write_to_file
- actions:
  - 'Actions:'
  - Render `knowledge/templates/ai-design.md` using the collected data.
  - Output to `docs/sdlc/ai-design.md`.
  agents:
  - system-architecture-specialist
  goal: Formalize the architecture into a human-and-machine-readable document.
  name: Technical Design Documentation
  skills:
  - generating-documentation
  tools:
  - write_to_file
- actions:
  - 'Actions:'
  - Prompt user to run `/developing-ai-agents` for the next Phase (Build).
  - Memory Hook: Synthesize logical architecture into a `KI:` node and link to the
      `TASK:`.
  - Triggered by user context or meta-orchestrator.
  - '"Execute this workflow."'
  - 'Axiomatic Alignment: Ensure Truth, Beauty, and Love.'
  - 'Memory First: Check context before execution.'
  - 'Verifiability: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - project-operations-specialist
  goal: Hand over to the development phase.
  name: Transition to Build
  skills:
  - managing-plane-tasks
  tools:
  - notify_user
tags: []
type: sequential
version: 2.0.0
---
# /ai-designing-ai-systems Workflow

**Version:** 1.0.0

## Overview
This workflow defines the structural and architectural design process for AI systems, ensuring alignment with the 5-layer architecture and strategic goals.

## Trigger Conditions
- New system architectual requirement.
- Need to redesign existing agentic flows.
- Evaluation of new technological components for the stack.

**Trigger Examples:**
- "Design a multi-agent system for autonomous data processing."
- "Evaluate the transition from a chain to an orchestrator-worker pattern."

## Phases

### Phase 1: Requirements Decomposition
- **Goal**: Analyze the PRD and NFRs to establish technical constraints.
- **Agents**: `python-ai-specialist`
- **Skills**: analyzing-code
- **Tools**: view_file
- **Actions**:
- Use `python-ai-specialist` to extract entities and constraints from `docs/sdlc/prd.md`.
- **Memory Hook**: Call `mcp_memory_open_nodes` for `TASK:[IssueKey]` and `SOP:ai-system-design`.
- **Save-on-Discover**: Register missing SOP/SKILL nodes if found in local filesystem.

### Phase 2: Architecture Selection
- **Goal**: Choose the optimal stack (agents, MCPs, models, databases).
- **Agents**: `system-architecture-specialist`
- **Skills**: architecture-selection
- **Tools**: mcp_memory_search_nodes
- **Actions**:
- Invoke the `/ai-designing-ai-systems` routing pattern to select between `chain`, `parallel`, or `orchestrator-workers` patterns.

### Phase 3: Interface & API Definition
- **Goal**: Define interaction protocols and data schemas.
- **Agents**: `python-ai-specialist`
- **Skills**: designing-apis
- **Tools**: write_to_file
- **Actions**:
- Trigger `.agent/skills/parallel/designing-apis/SKILL.md` to generate OpenAPI/JSON Schema definitions.

### Phase 4: Technical Design Documentation
- **Goal**: Formalize the architecture into a human-and-machine-readable document.
- **Agents**: `system-architecture-specialist`
- **Skills**: generating-documentation
- **Tools**: write_to_file
- **Actions**:
- Render `knowledge/templates/ai-design.md` using the collected data.
- Output to `docs/sdlc/ai-design.md`.

### Phase 5: Transition to Build
- **Goal**: Hand over to the development phase.
- **Agents**: `project-operations-specialist`
- **Skills**: managing-plane-tasks
- **Tools**: notify_user
- **Actions**:
- Prompt user to run `/developing-ai-agents` for the next Phase (Build).
- **Memory Hook**: Synthesize logical architecture into a `KI:` node and link to the `TASK:`.
- Triggered by user context or meta-orchestrator.
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)

## Best Practices
- Prioritize modularity and clear separation of concerns.
- Document all decision tradeoffs in a Decision Log.
- Validate all schemas against industrial standards.

## Related
- [/agent-development](file:///.agent/workflows/agent-development.md)
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
