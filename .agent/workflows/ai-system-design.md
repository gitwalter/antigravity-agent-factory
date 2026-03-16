---
description: Comprehensive workflow for designing AI systems including requirements
  analysis, architecture selection, cost estimation, and detailed design documentation.
version: 1.0.0
tags:
- ai
- system
- design
- standardized
---


# /ai-designing-ai-systems Workflow

**Version:** 1.0.0


**Goal:** Transform approved requirements (PRD) into a robust, scalable, and cost-effective AI system architecture.

## Phases

### Phase 1: Requirements Decomposition
- **Goal**: Analyze the PRD and NFRs to establish technical constraints.
- **Agent**: `python-ai-specialist`
- **Skills**: analyzing-code
- **Tools**: view_file
- **Actions**:
    - Use `python-ai-specialist` to extract entities and constraints from `docs/sdlc/prd.md`.

### Phase 2: Architecture Selection
- **Goal**: Choose the optimal stack (agents, MCPs, models, databases).
- **Agent**: `system-architecture-specialist`
- **Skills**: architecture-selection
- **Tools**: mcp_memory_search_nodes
- **Actions**:
    - Invoke the `/ai-designing-ai-systems` routing pattern to select between `chain`, `parallel`, or `orchestrator-workers` patterns.

### Phase 3: Interface & API Definition
- **Goal**: Define interaction protocols and data schemas.
- **Agent**: `python-ai-specialist`
- **Skills**: designing-apis
- **Tools**: write_to_file
- **Actions**:
    - Trigger `.agent/skills/parallel/designing-apis/SKILL.md` to generate OpenAPI/JSON Schema definitions.

### Phase 4: Technical Design Documentation
- **Goal**: Formalize the architecture into a human-and-machine-readable document.
- **Agent**: `system-architecture-specialist`
- **Skills**: generating-documentation
- **Tools**: write_to_file
- **Actions**:
    - Render `knowledge/templates/ai-design.md` using the collected data.
    - Output to `docs/sdlc/ai-design.md`.

### Phase 5: Transition to Build
- **Goal**: Hand over to the development phase.
- **Agent**: `project-operations-specialist`
- **Skills**: managing-plane-tasks
- **Tools**: notify_user
- **Actions**:
    - Prompt user to run `/developing-ai-agents` for the next Phase (Build).


## Trigger Conditions
- Triggered by user context or meta-orchestrator.


## Trigger Examples:
- "Execute this workflow."


## Best Practices
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.


## Related
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
