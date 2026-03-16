---
agents:
- '@Architect'
blueprints:
- universal
description: Antigravity workflow for poc-orchestration-workflow. Standardized for
  IDX Visual Editor.
domain: universal
name: poc-orchestration-workflow
steps:
- actions:
  - '**Lead Agent**: `SYARCH`'
  - '**Rule**: `agent-definition.md`'
  - '**Exit Criteria**: `requirements.json` generated and specialists assigned.'
  - Read `agent-staffing.json` to authorize tool access.
  agents:
  - '@Architect'
  goal: ''
  name: Strategic Decomposition
  skills: []
  tools: []
- actions:
  - '**Lead Agent**: `KNOPS`'
  - '**Logic**: Consult `orchestration-engine.json` for RAG vs. Graph priority.'
  - '**Tool**: `@mcp_antigravity-rag_search_library` or `@mcp_memory_read_graph`.'
  - '**Exit Criteria**: Context injected into the agent''s scratchpad.'
  agents:
  - '@Architect'
  goal: ''
  name: Contextual Harvesting
  skills: []
  tools: []
- actions:
  - '**Lead Agent**: `PAIS` (for Python) / `FSWS` (for Web)'
  - '**Constraint**: Must only use tools listed in `authorized_mcp_servers` for the
    role.'
  - '**Gate**: Check `technical-standards.md` before commit.'
  - '**Exit Criteria**: Implementation artifacts (code/docs) created.'
  agents:
  - '@Architect'
  goal: ''
  name: Operational Implementation
  skills: []
  tools: []
- actions:
  - '**Lead Agent**: `WQSS`'
  - '**Constraint**: Must verify `required_output_artifact` presence as per `workflow-catalog.json`.'
  - '**Promotion**: Follow `memory_promotion_protocols` in `orchestration-engine.json`.'
  - '**Exit Criteria**: Walkthrough finalized and session promoted.'
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - '@Architect'
  goal: ''
  name: Integrity Verification & Promotion
  skills: []
  tools: []
tags: []
type: sequential
version: 1.0.0
---

# System Integration POC Orchestration

**Version:** 1.0.0

## Overview
Antigravity workflow for orchestrating system integration Proof of Concepts (POCs). Standardized for IDX Visual Editor.

## Trigger Conditions
- Need to validate a new system integration or architectural approach via a POC.
- Requirement for cross-agent coordination to prove feasibility of a solution.
- User request: `/poc-orchestration`.

**Trigger Examples:**
- "Orchestrate a POC for integrating our RAG pipeline with the SAP backend."
- "Prove the feasibility of using LangGraph for multi-agent negotiation in our POC."

## Phases

### 1. Strategic Decomposition
- **Agents**: `@Architect`
- **Lead Agent**: `SYARCH`
- **Rule**: `agent-definition.md`
- **Exit Criteria**: `requirements.json` generated and specialists assigned.
- Read `agent-staffing.json` to authorize tool access.

### 2. Contextual Harvesting
- **Agents**: `@Architect`
- **Lead Agent**: `KNOPS`
- **Logic**: Consult `orchestration-engine.json` for RAG vs. Graph priority.
- **Tool**: `@mcp_antigravity-rag_search_library` or `@mcp_memory_read_graph`.
- **Exit Criteria**: Context injected into the agent's scratchpad.

### 3. Operational Implementation
- **Agents**: `@Architect`
- **Lead Agent**: `PAIS` (for Python) / `FSWS` (for Web)
- **Constraint**: Must only use tools listed in `authorized_mcp_servers` for the role.
- **Gate**: Check `technical-standards.md` before commit.
- **Exit Criteria**: Implementation artifacts (code/docs) created.

### 4. Integrity Verification & Promotion
- **Agents**: `@Architect`
- **Lead Agent**: `WQSS`
- **Constraint**: Must verify `required_output_artifact` presence as per `workflow-catalog.json`.
- **Promotion**: Follow `memory_promotion_protocols` in `orchestration-engine.json`.
- **Exit Criteria**: Walkthrough finalized and session promoted.
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
