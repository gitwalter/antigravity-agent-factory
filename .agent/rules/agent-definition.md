# Rule: Agent Definition

## Context
Standardizes how agents and personas are defined and specialized in `.agent/agents/`.

## Requirements
- **Persona Format**: Every agent MUST have a markdown definition file in `.agent/agents/`.
- **Mission First**: Definitions MUST start with a clear Mission Statement and Backstory.
- **Capability Mapping**:
    - Bind specific skills from `.agent/skills/`.
    - Define tool access and limitations.
- **Axiom Continuity**:
    - Agent behavior MUST align with `.agentrules`.
    - Agents MUST respect Axiom A2 (User Primacy).

## Process
1. Identify missing specialization.
2. Design persona and backstory (Phase 1 of `agent-development` workflow).
3. Draft agent definition file.
4. Bind required skills and knowledge.
5. Register in `agent-catalog.json`.
