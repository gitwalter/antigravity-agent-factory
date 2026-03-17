---
agents:
- '@Architect'
blueprints:
- universal
description: Antigravity workflow for master-system-orchestration. Standardized for
  IDX Visual Editor.
domain: universal
name: master-system-orchestration
steps:
- actions:
  - Deconstruct the request into **Functional**, **Structural**, and **Factual** requirements.
  - Search the Knowledge Base (`.agent/knowledge/`) for existing patterns that match
    the objective.
  - Identity the "Critical Path" (the sequence of actions that must succeed for the
    goal to be met).
  - '**Truth**: Are the requirements unambiguous?'
  - '**Beauty**: Is the proposed plan minimal and coherent?'
  agents:
  - '@Architect'
  goal: ''
  name: Strategic Decomposition & Goal Rooting
  skills: []
  tools: []
- actions:
  - Consult `agent-staffing.json` to resolve roles (e.g., Architect, Engineer, Guardian).
  - '**Delegation Logic**:'
  - 'If the task requires architectural changes: Assign `system-architecture-specialist`.'
  - 'If the task requires LLM app implementation: Assign `python-ai-specialist`.'
  - 'If the task requires structural repair: Assign `IntegrityGuardian`.'
  - '**Gap Detection**: If no agent matches the specialty, immediately trigger the
    `Agent Development` SOP.'
  agents:
  - '@Architect'
  goal: ''
  name: Tactical Staffing & Dependency Binding
  skills: []
  tools: []
- actions:
  - '**Parallelism**: Execute `python-ai-specialist` and `workflow-quality-specialist`
    tasks concurrently where possible.'
  - '**Handoffs**: Use `verified-communication` for data transfer between agents.'
  - '**State Maintenance**: Update `task.md` after every milestone.'
  agents:
  - '@Architect'
  goal: ''
  name: Synchronized Execution Flows
  skills: []
  tools: []
- actions:
  - 100% pass rate in relevant regression suites.
  - All new links verified via `link_checker.py --deep`.
  - '`walkthrough.md` provides proof of work with evidence (screenshots/logs).'
  - '**Love**: Does the result solve the user''s *actual* problem with care?'
  - '**Truth**: Is the implementation accurate and fully documented?'
  - '**Insufficient Tools**: If needed skills don''t exist, pivot to the **Skill Enrichment**
    workflow.'
  - '**Architectural Shift**: If implementation reveals design flaws, SAS must update
    the `implementation_plan.md`.'
  - '**Registry**: `.agent/knowledge/agent-staffing.json`'
  - '**SOP**: `Standard Feature Delivery Cycle` (SFDC)'
  - '**SOP**: `Agent Development`'
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  agents:
  - '@Architect'
  goal: ''
  name: Quality Governance & Final Convergence
  skills: []
  tools: []
tags: []
type: sequential
version: 1.0.0
---

# Master System Orchestration (MSO)

**Version:** 1.0.0

## Overview
Antigravity workflow for high-level system orchestration and complex task decomposition. Standardized for IDX Visual Editor.

## Trigger Conditions
- Received a complex, multi-step system requirement or architectural change.
- Need to orchestrate multiple specialized agents for a large-scale project.
- User request: `/master-system-orchestration`.

**Trigger Examples:**
- "Orchestrate the development of a multi-module ERP integration system."
- "Deconstruct and plan the architecture for our next-generation AI platform."

## Phases

### 1. Strategic Decomposition & Goal Rooting
- **Agents**: `@Architect`
- Deconstruct the request into **Functional**, **Structural**, and **Factual** requirements.
- Search the Knowledge Base (`.agent/knowledge/`) for existing patterns that match the objective.
- Identity the "Critical Path" (the sequence of actions that must succeed for the goal to be met).
- **Truth**: Are the requirements unambiguous?
- **Beauty**: Is the proposed plan minimal and coherent?

### 2. Tactical Staffing & Dependency Binding
- **Agents**: `@Architect`
- Consult `agent-staffing.json` to resolve roles (e.g., Architect, Engineer, Guardian).
- **Delegation Logic**:
- If the task requires architectural changes: Assign `system-architecture-specialist`.
- If the task requires LLM app implementation: Assign `python-ai-specialist`.
- If the task requires structural repair: Assign `IntegrityGuardian`.
- **Gap Detection**: If no agent matches the specialty, immediately trigger the `Agent Development` SOP.

### 3. Synchronized Execution Flows
- **Agents**: `@Architect`
- **Parallelism**: Execute `python-ai-specialist` and `workflow-quality-specialist` tasks concurrently where possible.
- **Handoffs**: Use `verified-communication` for data transfer between agents.
- **State Maintenance**: Update `task.md` after every milestone.

### 4. Quality Governance & Final Convergence
- **Agents**: `@Architect`
- 100% pass rate in relevant regression suites.
- All new links verified via `link_checker.py --deep`.
- `walkthrough.md` provides proof of work with evidence (screenshots/logs).
- **Love**: Does the result solve the user's *actual* problem with care?
- **Truth**: Is the implementation accurate and fully documented?
- **Insufficient Tools**: If needed skills don't exist, pivot to the **Skill Enrichment** workflow.
- **Architectural Shift**: If implementation reveals design flaws, SAS must update the `implementation_plan.md`.
- **Registry**: `.agent/knowledge/agent-staffing.json`
- **SOP**: `Standard Feature Delivery Cycle` (SFDC)
- **SOP**: `Agent Development`
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
