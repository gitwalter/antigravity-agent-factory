---
description: Comprehensive workflow for designing AI systems including requirements analysis, architecture selection, cost estimation, and detailed design documentation.
version: 1.0.0
---

# /ai-system-design Workflow

**Version:** 1.0.0


**Goal:** Transform approved requirements (PRD) into a robust, scalable, and cost-effective AI system architecture.

## Phases

### 1. Requirements Decomposition
- **Goal**: Analyze the PRD and NFRs to establish technical constraints.
- **Action**: Use `python-ai-specialist` to extract entities and constraints from `docs/sdlc/prd.md`.
- **Reference**: `docs/sdlc/nfr.md` for performance and security targets.

### 2. Architecture Selection
- **Goal**: Choose the optimal stack (agents, MCPs, models, databases).
- **Action**: Invoke the `/ai-system-design` routing pattern to select between `chain`, `parallel`, or `orchestrator-workers` patterns.
- **Tool**: `mcp_memory_search_nodes` to find existing agents/skills that can be reused.

### 3. Interface & API Definition
- **Goal**: Define interaction protocols and data schemas.
- **Action**: Trigger `.agent/skills/parallel/designing-apis/SKILL.md` to generate OpenAPI/JSON Schema definitions.

### 4. Technical Design Documentation
- **Goal**: Formalize the architecture into a human-and-machine-readable document.
- **Tool**: Render `knowledge/templates/ai-design.md` using the collected data.
- **Output**: [ai-design.md](file:///docs/sdlc/ai-design.md).

### 5. Transition to Build
- **Goal**: Hand over to the development phase.
- **Action**: Prompt user to run `/agent-development` for the next Phase (Build).


## Trigger Conditions
- Triggered by user context or meta-orchestrator.


## Trigger Examples:
- "Execute this workflow."
